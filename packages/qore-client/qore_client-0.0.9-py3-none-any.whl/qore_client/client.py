import hashlib
import hmac
import time
from io import BytesIO
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import pandas as pd
from requests import Response, request

from qore_client.settings import ACCESS_KEY, BASE_URL, SECRET_KEY


class QoreClient:
    """
    Qore API Client
    ~~~~~~~~~~~~~~~

    Qore 서비스에 접근할 수 있는 파이썬 Client SDK 예시입니다.
    """

    domain: str = BASE_URL

    def __init__(self, access_key: Optional[str] = None, secret_key: Optional[str] = None) -> None:
        """
        :param access_key: Qore API 인증에 사용되는 Access Key
        :param secret_key: Qore API 인증에 사용되는 Secret Key
        """
        self.__access_key = access_key or ACCESS_KEY
        self.__secret_key = secret_key or SECRET_KEY

        if not self.__access_key or not self.__secret_key:
            raise ValueError("access_key and secret_key must be provided")

    def generate_headers(self, credential_source: str) -> Dict[str, Any]:
        return {
            "X-API-ACCESS-KEY": self.__access_key,
            "X-API-SIGNATURE": self.generate_signature(credential_source=credential_source),
        }

    def generate_signature(self, credential_source: str) -> str:
        if self.__secret_key is None:
            raise TypeError("Secret key is None, cannot create signature.")
        signature = hmac.new(self.__secret_key.encode(), credential_source.encode(), hashlib.sha256).hexdigest()
        return signature

    def _get_file_response(self, file_id: str) -> Response:
        """
        파일 다운로드 URL을 가져와서 HTTP 응답 객체를 반환합니다.

        :param file_id: 다운로드할 파일의 ID
        :return: 다운로드된 파일에 대한 HTTP 응답 객체
        """

        response = self._request("GET", f"/api/file/{file_id}/download_url")

        if response is None:
            raise ValueError("Failed to get download info, received None response.")

        file_response = request("GET", response["download_url"])
        file_response.raise_for_status()

        return file_response

    def upload_file(self, folder_id: str, file_path: str) -> Dict[str, Any]:
        """
        파일 업로드 URL을 가져와서 HTTP 응답 객체를 반환합니다.

        :param folder_id: 업로드할 폴더의 ID
        :param file_name: 업로드할 파일의 이름
        :return: 업로드된 파일에 대한 HTTP 응답 객체
        """
        data = {
            "folder_id": folder_id,
        }

        with open(file_path, "rb") as f:
            files = {"file": f}
            response_data = self._request("POST", "/api/file/create", data=data, files=files)
            # _request for POST /api/file/create should always return a dict on success
            if response_data is None:
                raise ValueError("Failed to upload file, received None response.")

        return response_data

    def get_file(self, file_id: str) -> BytesIO:
        response = self._get_file_response(file_id)
        file_content = BytesIO(response.content)
        file_content.seek(0)
        return file_content

    def get_dataframe(self, dataframe_id: str) -> pd.DataFrame:
        response = self._get_file_response(dataframe_id)
        content_type = response.headers["Content-Type"]
        content = response.content

        if content_type == "application/vnd.quantit.parquet":
            return pd.read_parquet(BytesIO(content))
        else:
            raise ValueError(
                f"Only files saved using the 'Save Dataframe' node in Workspace can be converted to dataframe. File content type: {content_type}"
            )

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | list[tuple[str, Any]] | None = None,
        json: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """
        내부적으로 사용하는 공통 요청 메서드

        :param method: HTTP 메서드 (GET, POST, PATCH, DELETE 등)
        :param path: API 엔드포인트 경로 (ex: "/d/12345")
        :param params: query string으로 전송할 딕셔너리
        :param data: 폼데이터(form-data) 등으로 전송할 딕셔너리
        :param json: JSON 형태로 전송할 딕셔너리
        :param files: multipart/form-data 요청 시 사용할 파일(dict)
        :return: 응답 JSON(dict) 또는 raw 데이터
        """
        url = f"{self.domain}{path}"

        # method, path, params를 문자열로 결합하여 서명 생성
        if params is None:
            params = {}
        params["timestamp"] = time.time()
        query_string = urlencode(params)
        credential_source = f"{method}:{path}:{query_string}"

        headers = self.generate_headers(credential_source=credential_source)

        response: Response = request(
            method=method,
            headers=headers,
            url=url,
            params=params,
            data=data,
            json=json,
            files=files,
        )
        # 에러 발생 시 raise_for_status()가 예외를 던짐
        response.raise_for_status()

        # 일부 DELETE 요청은 204(No Content)일 수 있으므로, 이 경우 JSON 파싱 불가
        if response.status_code == 204 or not response.content:
            return None

        return response.json()
