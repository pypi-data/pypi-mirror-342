
# Bodit-Analysis-Module

**BODIT 분석을 위한 Python 패키지입니다.**
🔗 PyPI: <https://pypi.org/project/bodit-analysis-module/>
<details>
  <summary>📑 개요</summary>

- [설치 방법](#설치-방법)
- [사용 예시](#사용-예시)
- [모듈 설명](#모듈-설명)
  - [fhBasic](#fhbasic-모듈)
  - [fhDatabase](#fhdatabase-모듈)
  - [fhRawdata](#fhrawdata-모듈)
- [변경 사항](#변경-사항)

</details>

## 설치 방법

```bash
pip install bodit-analysis-module
```

## 사용 예시

```python
from bodit_analysis_module import fhBasic, fhDatabase, fhRawdata

# 데이터 로드
data = fhRawdata.load_data()

# 특성 추출
features = fhFeature.extract_features(data)
```

## 버전 정보

:white_check_mark:**v0.1.8** (2025‑04‑21)

- FeatureExtraction 관련 모듈 추가

:x:**v0.1.5** (2025‑04‑18)

- 초기 베타 릴리즈
- fhBasic, fhDatabase, fhRawdata 모듈 기본 기능 제공
- 주요 유틸리티 함수 및 데이터베이스 연결/Rawdata 처리 클래스 포함

:x:**v0.1.4** (2025-04-17)

- PyPI 업로드 및 초기 테스트

## 모듈 설명

### fhBasic 모듈

기본적인 유틸리티 함수들을 제공하는 모듈입니다.

#### 주요 함수_fhBasic

##### 1. loadSectionTable 함수

```python
def loadSectionTable() -> pd.DataFrame
```

- **반환값**: pd.DataFrame - 섹션 정보가 포함된 데이터프레임
- **설명**: 섹션 테이블을 로드하는 함수입니다.

##### 2. createFolder 함수

```python
def createFolder(directory: str) -> None
```

- **파라미터**:
  - `directory`: str - 생성할 폴더 경로
- **설명**: 지정된 경로에 폴더를 생성하는 함수입니다.

##### 3. readFile 함수

```python
def readFile(path: str, fileName: str) -> pd.DataFrame
```

- **파라미터**:
  - `path`: str - 파일이 존재하는 경로
  - `fileName`: str - 파일명 (확장자 포함)
- **반환값**: pd.DataFrame - 읽어들인 데이터프레임
- **설명**: 파일을 읽어 데이터프레임으로 반환하는 함수입니다.

##### 4. getDateList 함수

```python
def getDateList(startDate: str, endDate: str) -> list
```

- **파라미터**:
  - `startDate`: str - 시작일 (YYYY-MM-DD 형식)
  - `endDate`: str - 종료일 (YYYY-MM-DD 형식)
- **반환값**: list - 날짜 문자열 리스트 (YYYY-MM-DD 형식)
- **설명**: 시작일과 종료일 사이의 날짜 리스트를 생성하는 함수입니다.

##### 5. getTargetInfo 함수

```python
def getTargetInfo(targetInfoBrief: list) -> pd.DataFrame
```

- **파라미터**:
  - `targetInfoBrief`: list - [cowId, startDate, endDate] 형식의 리스트
- **반환값**: pd.DataFrame - 확장된 타겟 정보 데이터프레임 (cowId, date 컬럼 포함)
- **설명**: 타겟 정보를 확장하여 데이터프레임으로 반환하는 함수입니다.

##### 6. addPinDate 함수

```python
def addPinDate(cowId: str, date: str, df: pd.DataFrame) -> pd.DataFrame
```

- **파라미터**:
  - `cowId`: str - 소의 ID
  - `date`: str - 날짜
  - `df`: pd.DataFrame - 원본 데이터프레임
- **반환값**: pd.DataFrame - pin과 date 컬럼이 추가된 데이터프레임
- **설명**: 데이터프레임에 pin과 date 컬럼을 추가하는 함수입니다.

#### 주요 클래스_fhBasic

##### LatestVersion 클래스

```python
class LatestVersion:
    def __init__(self, cowId, date, basePath, prefix):
        # ...
    
    def getVersion(self) -> int:
        # ...
    
    def getFileName(self) -> str:
        # ...
    
    def getExtension(self) -> str:
        # ...
    
    def getFile(self) -> pd.DataFrame:
        # ...
```

- **설명**: 최신 버전의 파일을 관리하는 클래스입니다.
- **주요 메서드**:
  - `getVersion()`: 최신 버전 번호를 반환합니다.
  - `getFileName()`: 최신 버전의 파일명을 반환합니다.
  - `getExtension()`: 파일의 확장자를 반환합니다.
  - `getFile()`: 최신 버전의 파일을 읽어 데이터프레임으로 반환합니다.

### fhDatabase 모듈

데이터베이스 연결 및 쿼리 실행을 관리하는 모듈입니다.

#### 주요 클래스_fhDatabase

##### DbConnectionConfig 클래스

```python
@dataclass()
class DbConnectionConfig:
    user: str
    password: str
    host: str
    port: str
```

- **설명**: 데이터베이스 연결 설정을 위한 데이터 클래스입니다.
- **속성**:
  - `user`: 데이터베이스 사용자 이름
  - `password`: 데이터베이스 비밀번호
  - `host`: 데이터베이스 호스트 주소
  - `port`: 데이터베이스 포트 번호

##### DBLoader 클래스

```python
class DBLoader:
    def __init__(self, region: str = 'ap-northeast-2', secret_name: str = 'rds-db-credentials/fh-db-prod-cluster/console', db_name: str = 'fh'):
        # ...
    
    def get_db_table(self, query: str, params: Optional[ParamsSequenceOrDictType] = None) -> pd.DataFrame:
        # ...
    
    def get_unique_list(self, table: str, col: str) -> list:
        # ...
```

- **설명**: AWS RDS 데이터베이스 연결 및 쿼리 실행을 관리하는 클래스입니다.
- **주요 메서드**:
  - `get_db_table()`: SQL 쿼리를 실행하고 결과를 데이터프레임으로 반환합니다.
  - `get_unique_list()`: 테이블에서 특정 컬럼의 고유값 목록을 반환합니다.

### fhRawdata 모듈

Rawdata 처리 및 추출 관련 함수들을 제공하는 모듈입니다.

#### 주요 함수_fhRawdata

##### 1. get_rawdata_window 함수

```python
def get_rawdata_window(rawData: pd.DataFrame) -> np.ndarray
```

- **파라미터**:
  - `rawData`: pd.DataFrame - 처리할 rawdata 데이터프레임
- **반환값**: np.ndarray - 윈도우 처리된 데이터 배열
- **설명**: Rawdata를 윈도우 단위로 처리하는 함수입니다.

##### 2. get_empty_list 함수

```python
def get_empty_list(rawDataWindow: np.ndarray) -> list
```

- **파라미터**:
  - `rawDataWindow`: np.ndarray - 윈도우 처리된 데이터 배열
- **반환값**: list - 빈 데이터가 있는 윈도우의 인덱스 리스트
- **설명**: 빈 데이터가 있는 윈도우의 인덱스를 찾는 함수입니다.

#### 주요 클래스_fhRawdata

##### FHRawdataException 클래스

```python
class FHRawdataException(Exception):
    def __init__(self, message="This is a fhRawdata exception"):
        # ...
```

- **설명**: Rawdata 관련 예외를 처리하는 클래스입니다.

##### RawDataExtractor 클래스

```python
class RawDataExtractor:
    def __init__(self, cow_id: str, date: str, region: str):
        # ...
    
    def extract_rawdata(self) -> pd.DataFrame:
        # ...
    
    def __get_bucket_name(self) -> str:
        # ...
    
    def _get_farm_info(self) -> tuple:
        # ...
    
    def _merge_rawdata(self) -> pd.DataFrame:
        # ...
    
    def __make_datetime_range(self) -> pd.DatetimeIndex:
        # ...
    
    def __read_file_from_s3(self, year: str, month: str, day: str, hour: str) -> pd.DataFrame:
        # ...
    
    def _clean_rawdata(self, df: pd.DataFrame) -> pd.DataFrame:
        # ...
    
    def _adjust_rawdata(self, df: pd.DataFrame) -> pd.DataFrame:
        # ...
```

- **설명**: 1시간 단위 파일에서 Rawdata를 추출하는 클래스입니다.
- **주요 메서드**:
  - `extract_rawdata()`: Rawdata를 추출하고 전처리합니다.
  - `__get_bucket_name()`: 지역 코드에 따른 S3 버킷 이름을 반환합니다.
  - `_get_farm_info()`: 소의 농장 정보를 조회합니다.
  - `_merge_rawdata()`: S3에서 1시간 단위 rawdata 파일을 읽어와 병합합니다.
  - `_clean_rawdata()`: Rawdata에서 이상치를 제거합니다.
  - `_adjust_rawdata()`: Rawdata의 샘플링 간격을 조정합니다.
