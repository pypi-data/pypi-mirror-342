from .fhConst import SECTION_TABLE_PATH

import os
import pandas as pd
from glob import glob


def loadSectionTable() -> pd.DataFrame:
    """섹션 테이블을 로드하는 함수 (Overlap)
    
    Returns:
        pd.DataFrame: 섹션 정보가 포함된 데이터프레임
    """
    sectionTablePath = SECTION_TABLE_PATH
    sectionTable = pd.read_csv(sectionTablePath)
    return sectionTable


def createFolder(directory: str) -> None:
    """지정된 경로에 폴더를 생성하는 함수
    
    Args:
        directory (str): 생성할 폴더 경로
        
    Raises:
        Exception: 폴더 생성 실패 시 발생
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        raise Exception(f"[{pd.Timestamp.now()}] Error createFolder." + directory)
        
        
def readFile(path: str, fileName: str) -> pd.DataFrame:
    """파일을 읽어 데이터프레임으로 반환하는 함수
    
    Args:
        path (str): 파일이 존재하는 경로
        fileName (str): 파일명 (확장자 포함)
        
    Returns:
        pd.DataFrame: 읽어들인 데이터프레임
        
    Raises:
        Exception: 지원하지 않는 파일 확장자, 파일이 존재하지 않거나 비어있는 경우 발생
    """
    fullPath = os.path.join(path, fileName)   
    extension = os.path.splitext(fullPath)[1]

    try:
        if extension == '.csv':
            df = pd.read_csv(fullPath, encoding='cp949')
        elif extension == '.parquet':
            df = pd.read_parquet(fullPath)
        else:
            raise Exception(f"[{pd.Timestamp.now()}] File Extension '{extension}' is not supported.")
            
    except FileNotFoundError:
        raise Exception(f"[{pd.Timestamp.now()}] File does not exist. - {fullPath}")
    
    if df.empty:
        raise Exception(f"[{pd.Timestamp.now()}] File is empty. - {fullPath}")
    else:
        return df


def getDateList(startDate: str, endDate: str) -> list:
    """시작일과 종료일 사이의 날짜 리스트를 생성하는 함수
    
    Args:
        startDate (str): 시작일 (YYYY-MM-DD 형식)
        endDate (str): 종료일 (YYYY-MM-DD 형식)
        
    Returns:
        list: 날짜 문자열 리스트 (YYYY-MM-DD 형식)
    """
    dateList = pd.date_range(start=startDate, end=endDate)
    dateList = dateList.strftime("%Y-%m-%d").tolist()
    return dateList


def getTargetInfo(targetInfoBrief: list) -> pd.DataFrame:
    """타겟 정보를 확장하여 데이터프레임으로 반환하는 함수
    
    Args:
        targetInfoBrief (list): [cowId, startDate, endDate] 형식의 리스트
        
    Returns:
        pd.DataFrame: 확장된 타겟 정보 데이터프레임 (cowId, date 컬럼 포함)
    """
    targetInfo = []
    for cowId, startDate, endDate in targetInfoBrief:
        dateList = getDateList(startDate, endDate)
        for date in dateList:
            targetInfo.append([cowId, date])
    targetInfo = pd.DataFrame(targetInfo, columns=['cowId', 'date'])
    return targetInfo


def addPinDate(cowId: str, date: str, df: pd.DataFrame) -> pd.DataFrame:
    """데이터프레임에 pin과 date 컬럼을 추가하는 함수
    
    Args:
        cowId (str): 소의 ID
        date (str): 날짜
        df (pd.DataFrame): 원본 데이터프레임
        
    Returns:
        pd.DataFrame: pin과 date 컬럼이 추가된 데이터프레임
    """
    T = df.copy()
    T.insert(loc=0, column='pin', value=cowId)
    T.insert(loc=1, column='date', value=date)
    return T


class LatestVersion:    
    """최신 버전의 파일을 관리하는 클래스
    
    Attributes:
        cowId (str): 소의 ID
        date (str): 날짜
        basePath (str): 기본 경로
        prefix (str): 파일 접두사
        path (str): 전체 파일 경로
        fileList (pd.DataFrame): 파일 목록
    """
    
    def __init__(self, cowId, date, basePath, prefix):
        self.cowId = cowId
        self.date = date
        self.basePath = basePath
        self.prefix = prefix 
        self.path = os.path.join(basePath, cowId, date, prefix)
        self.fileList = pd.DataFrame(glob(self.path + '*'), columns = ['fileName'])
        
        versionReg = 'V(\d{1,3})_'
        self.fileList['version'] = self.fileList['fileName'].str.extract(versionReg).astype('int')
        if self.fileList.empty:
            raise FileNotFoundError(f"[{pd.Timestamp.now()}] File dose not exist - pin: {self.cowId} date: {self.date}")
    
    def getVersion(self) -> int:
        """최신 버전 번호를 반환하는 메서드
        
        Returns:
            int: 최신 버전 번호
        """
        version = self.fileList['version'].max()
        return version
    
    def getFileName(self) -> str:
        """최신 버전의 파일명을 반환하는 메서드
        
        Returns:
            str: 최신 버전 파일명
        """
        fileName = self.fileList.loc[self.fileList['version'].idxmax(), 'fileName']
        return fileName
    
    def getExtension(self) -> str:
        """파일의 확장자를 반환하는 메서드
        
        Returns:
            str: 파일 확장자
        """
        extension = os.path.splitext(self.getFileName())[1]
        return extension
    
    def getFile(self) -> pd.DataFrame:
        """최신 버전의 파일을 읽어 데이터프레임으로 반환하는 메서드
        
        Returns:
            pd.DataFrame: 파일 내용을 담은 데이터프레임
            
        Raises:
            ValueError: 지원하지 않는 파일 확장자인 경우 발생
        """
        extension = self.getExtension()
        
        if extension == '.csv':
            df = pd.read_csv(self.getFileName(), encoding='cp949')
        elif extension == '.parquet':
            df = pd.read_parquet(self.getFileName())
        else:
            raise ValueError(f"[{pd.Timestamp.now()}] File Extension '{extension}' is not supported. - pin: {self.cowId} date: {self.date}")
        
        return df
    
def find_region(country: str):
    """국가에 따른 지역을 찾는 함수
    
    Args:
        country (str): 국가명
        
    Returns:
        None: 현재 구현되지 않음
    """
    return None

# farm_id
# country