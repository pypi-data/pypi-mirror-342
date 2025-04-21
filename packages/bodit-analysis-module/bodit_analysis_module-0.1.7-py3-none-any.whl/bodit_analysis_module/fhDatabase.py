from .fhConst import REGION, SECRET_NAME, DB_NAME, SERVICE_NAME
from botocore.exceptions import ClientError
from dataclasses import dataclass
from mysql.connector import MySQLConnection
from typing import Optional, Union, Sequence, Mapping, Any

import json
import boto3
import pandas as pd

# mysql.connector.types.ParamsSequenceOrDictType 대체
ParamsSequenceOrDictType = Union[Sequence[Any], Mapping[str, Any]]


@dataclass()
class DbConnectionConfig:
    """데이터베이스 연결 설정을 위한 데이터 클래스

    Attributes:
        user (str): 데이터베이스 사용자 이름
        password (str): 데이터베이스 비밀번호
        host (str): 데이터베이스 호스트 주소
        port (str): 데이터베이스 포트 번호
    """
    user: str
    password: str
    host: str
    port: str


class DBLoader:
    """AWS RDS 데이터베이스 연결 및 쿼리 실행을 관리하는 클래스

    Attributes:
        __region (str): AWS 리전
        __secret_name (str): AWS Secrets Manager의 시크릿 이름
        __db_name (str): 데이터베이스 이름
        __secret (DbConnectionConfig): 데이터베이스 연결 설정
    """

    def __init__(self,
                 region: str = REGION,
                 secret_name: str = SECRET_NAME,
                 db_name: str = DB_NAME
                 ):
        """DBLoader 클래스의 생성자

        Args:
            region (str, optional): AWS 리전 이름
            secret_name (str, optional): AWS Secrets Manager의 시크릿 이름
            db_name (str, optional): 데이터베이스 이름
        """
        self.__region = region
        self.__secret_name = secret_name
        self.__db_name = db_name
        self.__secret = None

    def __get_db_secret(self) -> DbConnectionConfig:
        """AWS Secrets Manager에서 데이터베이스 연결 정보를 가져오는 메서드

        Returns:
            DbConnectionConfig: 데이터베이스 연결 설정 객체

        Raises:
            ClientError: AWS Secrets Manager 접근 실패 시 발생
        """
        client = boto3.client(
            service_name=SERVICE_NAME,
            region_name=self.__region,
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.__secret_name
            )
        except ClientError as e:
            raise e

        secret = json.loads(get_secret_value_response['SecretString'])

        return DbConnectionConfig(
            user=secret['username'],
            password=secret['password'],
            host=secret['host'],
            port=secret['port']
        )

    def __get_connection(self) -> MySQLConnection:
        """MySQL 데이터베이스 연결을 생성하는 메서드

        Returns:
            MySQLConnection: MySQL 데이터베이스 연결 객체
        """
        if not self.__secret:
            self.__secret = self.__get_db_secret()

        return MySQLConnection(
            user=self.__secret.user,
            password=self.__secret.password,
            host=self.__secret.host,
            port=self.__secret.port,
            database=self.__db_name,
        )

    def get_db_table(self, query: str, params: Optional[ParamsSequenceOrDictType] = None) -> pd.DataFrame:
        """SQL 쿼리를 실행하고 결과를 데이터프레임으로 반환하는 메서드

        Args:
            query (str): 실행할 SQL 쿼리
            params (Optional[ParamsSequenceOrDictType], optional): 쿼리 파라미터. 기본값은 None.

        Returns:
            pd.DataFrame: 쿼리 결과를 담은 데이터프레임
        """
        with self.__get_connection() as cnx:
            with cnx.cursor(buffered=True, named_tuple=True) as cursor:
                cursor.execute(query, params)
                record = cursor.fetchall()
                df = pd.DataFrame(record)
                return df

    def get_unique_list(self, table: str, col: str) -> list:
        """테이블에서 특정 컬럼의 고유값 목록을 반환하는 메서드

        Args:
            table (str): 테이블 이름
            col (str): 컬럼 이름

        Returns:
            list: 고유값 목록
        """
        query = f"SELECT DISTINCT {col} FROM {table}"
        df = self.get_db_table(query)
        return df[col].tolist()
