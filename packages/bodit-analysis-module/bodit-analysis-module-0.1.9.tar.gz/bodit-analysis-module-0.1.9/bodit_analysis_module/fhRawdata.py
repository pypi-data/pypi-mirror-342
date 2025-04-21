from .fhBasic import loadSectionTable
from .fhConst import RAWDATA_INPUT_SIZE, WINDOW_SHAPE, SAMPLE_INTERVAL
from .fhDatabase import DBLoader
from datetime import timedelta

import io
import boto3
import numpy as np
import pandas as pd


class FHRawdataException(Exception):
    """Rawdata 관련 예외를 처리하는 클래스
    
    Attributes:
        message (str): 예외 메시지
    """
    def __init__(self, message="This is a fhRawdata exception"):
        self.message = message
        super().__init__(self.message)


def get_rawdata_window(rawData: pd.DataFrame) -> np.ndarray:
    """Rawdata를 윈도우 단위로 처리하는 함수
    
    Args:
        rawData (pd.DataFrame): 처리할 rawdata 데이터프레임
        
    Returns:
        np.ndarray: 윈도우 처리된 데이터 배열
        
    Raises:
        FHRawdataException: 데이터 크기가 예상과 다른 경우 발생
    """
    # 주의: loadSectionTable() 함수에서 반환된 DataFrame에 'startIndex' 컬럼이 포함되어 있지 않다면
    # 나중에 데이터 인덱싱 부분에서 문제가 발생할 수 있으므로, 해당 부분을 반드시 확인해야 합니다.
    sectionTable = loadSectionTable()
    rawData = rawData[['ax','ay','az','gx','gy','gz']].to_numpy(dtype='float32')
    
    if len(rawData) != RAWDATA_INPUT_SIZE:
        err_msg = " ".join(
            [
                f"[{pd.Timestamp.now()}] Rawdata size error!",
                f"(Expected: {RAWDATA_INPUT_SIZE} Size: {len(rawData)})"
            ]
        )
        raise FHRawdataException(err_msg)

    rawDataWindow = np.lib.stride_tricks.sliding_window_view(rawData, WINDOW_SHAPE)
    rawDataWindow = rawDataWindow.reshape(-1, WINDOW_SHAPE[0], WINDOW_SHAPE[1])
    rawDataWindow = rawDataWindow[(sectionTable['startIndex']).to_numpy(), :, :]
    return rawDataWindow

def get_empty_list(rawDataWindow: np.ndarray) -> list:
    """빈 데이터가 있는 윈도우의 인덱스를 찾는 함수
    
    Args:
        rawDataWindow (np.ndarray): 윈도우 처리된 데이터 배열
        
    Returns:
        list: 빈 데이터가 있는 윈도우의 인덱스 리스트
    """
    emptyList = list(np.where((np.sum(rawDataWindow, axis=2) == 0).any(axis=1)))[0]
    return emptyList

class RawDataExtractor:
    """1시간 단위 파일에서 Rawdata를 추출하는 클래스
    
    Attributes:
        __cow_id (str): 소의 ID
        __date (str): 날짜
        __region (str): 지역 코드
        __s3 (boto3.client): S3 클라이언트
        __bucket_name (str): S3 버킷 이름
        __farm_id (str): 농장 ID
        __timezone (str): 시간대
        __country_code (str): 국가 코드
    """
    
    def __init__(self, cow_id: str, date: str, region: str):
        """RawDataExtractor 클래스의 생성자
        
        Args:
            cow_id (str): 소의 ID
            date (str): 날짜
            region (str): 지역 코드
        """
        self.__cow_id = cow_id
        self.__date = date
        self.__region = region
        self.__s3 = boto3.client('s3')
        self.__bucket_name = self.__get_bucket_name()
        self.__farm_id, self.__timezone, self.__country_code = self._get_farm_info()

    def extract_rawdata(self) -> pd.DataFrame:
        """Rawdata를 추출하고 전처리하는 메서드
        
        Returns:
            pd.DataFrame: 전처리된 rawdata 데이터프레임
        """
        rawdata = self._merge_rawdata() # 1. s3에서 1시간 rawdata를 읽어와 병합
        rawdata = self._clean_rawdata(rawdata) # 2. 이상 파일 제거
        rawdata = self._adjust_rawdata(rawdata) # 3. 샘플링 간격 조정 및 시간 재설정
        rawdata = self.__convert_to_local_time(rawdata) # 4. 로컬 시간으로 변환
        rawdata = rawdata.rename(columns={'measure_at': 'rawTimeStamp'}) # 5. rawTimeStamp 컬럼 이름 변경
        rawdata = self.__filter_date(rawdata) # 6. 날짜 필터링 (타겟 날짜만 선정)
        rawdata = self.__make_fulltime_rawdata(rawdata) # 7. 시간 시리즈 생성
        rawdata = rawdata[['rawTimeStamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz']] # 8. 최종 컬럼 선택
        return rawdata
    
    def __get_bucket_name(self) -> str:
        """지역 코드에 따른 S3 버킷 이름을 반환하는 메서드
        
        Returns:
            str: S3 버킷 이름
            
        Raises:
            FHRawdataException: 잘못된 지역 코드인 경우 발생
        """
        if self.__region == 'ap-northeast-2': # 한국
            return 'fh-iot-backend-prod-fhbucket-10r0tnnuhr5iu'
        elif self.__region == 'eu-west-1': # 케냐
            return 'fh-iot-backend-ireland-fhbucket-4kvozaioqpgj'
        elif self.__region == 'ap-southeast-2': # 호주, 뉴질랜드
            return 'fh-iot-backend-sydney-fhbucket-12nvm2km525lr'
        elif self.__region == 'ap-south-1': # 인도
            return 'fh-iot-backend-mumbai-fhbucket-igqqgvq1k1e6'
        else:
            raise FHRawdataException(f"잘못된 지역 설정입니다. (region: {self.__region})")
    
    def _get_farm_info(self) -> tuple:
        """소의 농장 정보를 조회하는 메서드
        
        Returns:
            tuple: (farm_id, timezone, country_code)
        """
        db = DBLoader(region=self.__region)

        query = f"""
        SELECT 
            Cow.farm_id,
            Farm.timezone,
            Farm.country_code
        FROM 
            Cow
        JOIN 
            Farm ON Cow.farm_id = Farm.id
        WHERE 
            Cow.id = '{self.__cow_id}';
        """
        df = db.get_db_table(query)
        if df.empty:
            raise FHRawdataException(f"소 정보를 찾을 수 없습니다. (cow_id: {self.__cow_id})")
        
        return df.iloc[0]['farm_id'], df.iloc[0]['timezone'], df.iloc[0]['country_code']
    
    def _merge_rawdata(self) -> pd.DataFrame:
        """S3에서 1시간 단위 rawdata 파일을 읽어와 병합하는 메서드
        
        Returns:
            pd.DataFrame: 병합된 rawdata 데이터프레임
        """
        datetime_range = self.__make_datetime_range()
        rawdata_list = []
        
        for dt in datetime_range:
            year = dt.strftime('%Y')
            month = dt.strftime('%m')
            day = dt.strftime('%d')
            hour = dt.strftime('%H')
            
            try:
                df = self.__read_file_from_s3(year, month, day, hour)
                rawdata_list.append(df)
            except FHRawdataException:
                continue
        
        if not rawdata_list:
            raise FHRawdataException(f"Rawdata를 찾을 수 없습니다. (cow_id: {self.__cow_id}, date: {self.__date})")
        
        return pd.concat(rawdata_list, axis=0, ignore_index=True)
    
    def __make_datetime_range(self) -> pd.DatetimeIndex:
        """날짜 범위를 생성하는 메서드
        
        Returns:
            pd.DatetimeIndex: 날짜 범위
        """
        date = pd.to_datetime(self.__date)
        start_date = date - timedelta(hours=1)
        end_date = date + timedelta(hours=1)
        
        return pd.date_range(start=start_date, end=end_date, freq='H')
    
    def __read_file_from_s3(self, year: str, month: str, day: str, hour: str) -> pd.DataFrame:
        """S3에서 rawdata 파일을 읽는 메서드
        
        Args:
            year (str): 년도
            month (str): 월
            day (str): 일
            hour (str): 시간
            
        Returns:
            pd.DataFrame: 읽어들인 rawdata 데이터프레임
            
        Raises:
            FHRawdataException: 파일이 존재하지 않거나 읽기 실패 시 발생
        """
        key = f"{self.__farm_id}/{year}/{month}/{day}/{hour}/rawdata.csv"
        
        try:
            response = self.__s3.get_object(Bucket=self.__bucket_name, Key=key)
            df = pd.read_csv(io.BytesIO(response['Body'].read()))
            return df
        except self.__s3.exceptions.NoSuchKey:
            raise FHRawdataException(f"파일이 존재하지 않습니다. (key: {key})")
        except Exception as e:
            raise FHRawdataException(f"파일 읽기 실패: {str(e)}")
    
    def _clean_rawdata(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rawdata에서 이상치를 제거하는 메서드
        
        Args:
            df (pd.DataFrame): 전처리할 rawdata 데이터프레임
            
        Returns:
            pd.DataFrame: 이상치가 제거된 데이터프레임
        """
        # 1. 결측값 제거
        df = df.dropna()
        
        # 2. 중복값 제거
        df = df.drop_duplicates()
        
        # 3. 시간순 정렬
        df = df.sort_values('measure_at')
        
        # 4. 이상치 제거
        for col in ['ax', 'ay', 'az', 'gx', 'gy', 'gz']:
            # Z-score 방식으로 이상치 제거
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            df = df[z_scores < 3]
        
        return df
    
    def _adjust_rawdata(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rawdata의 샘플링 간격을 조정하는 메서드
        
        Args:
            df (pd.DataFrame): 조정할 rawdata 데이터프레임
            
        Returns:
            pd.DataFrame: 샘플링 간격이 조정된 데이터프레임
        """
        # 1. 연속 데이터 조정
        df = self.__adjust_continuous_data(df)
        
        # 2. 불연속 데이터 조정
        data_seq_diff = df['measure_at'].diff()
        is_data_seq_discontinue = data_seq_diff > pd.Timedelta(seconds=SAMPLE_INTERVAL * 2)
        
        if is_data_seq_discontinue.any():
            df = self.__adjust_discontinuous_data(df, data_seq_diff, is_data_seq_discontinue)
        
        return df
    
    def __adjust_continuous_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """연속 데이터의 샘플링 간격을 조정하는 메서드
        
        Args:
            df (pd.DataFrame): 조정할 데이터프레임
            
        Returns:
            pd.DataFrame: 조정된 데이터프레임
        """
        df = df.set_index('measure_at')
        df = df.resample(SAMPLE_INTERVAL * pd.Timedelta(seconds=1)).mean()
        df = df.reset_index()
        return df
    
    def __adjust_discontinuous_data(self, df: pd.DataFrame, data_seq_diff: pd.Series, is_data_seq_discontinue: pd.Series) -> pd.DataFrame:
        """불연속 데이터의 샘플링 간격을 조정하는 메서드
        
        Args:
            df (pd.DataFrame): 조정할 데이터프레임
            data_seq_diff (pd.Series): 시간 차이 시리즈
            is_data_seq_discontinue (pd.Series): 불연속 지점 표시 시리즈
            
        Returns:
            pd.DataFrame: 조정된 데이터프레임
        """
        df = df.copy()
        df['is_discontinue'] = is_data_seq_discontinue
        
        # 불연속 지점에서 데이터 분할
        df_list = []
        start_idx = 0
        
        for idx in df[df['is_discontinue']].index:
            if idx > start_idx:
                df_list.append(df.iloc[start_idx:idx])
            start_idx = idx
        
        if start_idx < len(df):
            df_list.append(df.iloc[start_idx:])
        
        # 각 분할 데이터에 대해 샘플링 간격 조정
        adjusted_df_list = []
        for sub_df in df_list:
            if len(sub_df) > 1:
                adjusted_df = self.__adjust_continuous_data(sub_df)
                adjusted_df_list.append(adjusted_df)
        
        return pd.concat(adjusted_df_list, axis=0, ignore_index=True)
    
    def __convert_to_local_time(self, df: pd.DataFrame) -> pd.DataFrame:
        """UTC 시간을 로컬 시간으로 변환하는 메서드
        
        Args:
            df (pd.DataFrame): 변환할 데이터프레임
            
        Returns:
            pd.DataFrame: 로컬 시간으로 변환된 데이터프레임
        """
        df = df.copy()
        df['measure_at'] = pd.to_datetime(df['measure_at'])
        df['measure_at'] = df['measure_at'].dt.tz_localize('UTC').dt.tz_convert(self.__timezone)
        return df
    
    def __filter_date(self, rawdata: pd.DataFrame) -> pd.DataFrame:
        """특정 날짜의 데이터만 필터링하는 메서드
        
        Args:
            rawdata (pd.DataFrame): 필터링할 데이터프레임
            
        Returns:
            pd.DataFrame: 필터링된 데이터프레임
        """
        target_date = pd.to_datetime(self.__date).date()
        return rawdata[rawdata['measure_at'].dt.date == target_date]
    
    def __make_fulltime_rawdata(self, rawdata: pd.DataFrame) -> pd.DataFrame:
        """시간 시리즈를 생성하는 메서드
        
        Args:
            rawdata (pd.DataFrame): 시리즈를 생성할 데이터프레임
            
        Returns:
            pd.DataFrame: 시간 시리즈가 추가된 데이터프레임
        """
        start_time = rawdata['measure_at'].min()
        end_time = rawdata['measure_at'].max()
        
        full_time = pd.date_range(start=start_time, end=end_time, freq=SAMPLE_INTERVAL * pd.Timedelta(seconds=1))
        full_time_df = pd.DataFrame({'measure_at': full_time})
        
        return pd.merge(full_time_df, rawdata, on='measure_at', how='left')
