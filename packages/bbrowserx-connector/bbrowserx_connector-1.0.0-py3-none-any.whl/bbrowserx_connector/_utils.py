from typing import Dict, List, Optional
import requests
from pydantic import BaseModel
from requests.adapters import Retry, HTTPAdapter

from ._constants import ConnectorKeys, UNTITLED


TAB_STRING: str = " " * 4


class RequestMode:
    POST: str = "post"
    PUT: str = "put"
    GET: str = "get"


class RequestContent(BaseModel):
    params: Dict = {}
    data: Dict = {}
    body_json: Dict = {}
    headers: Dict = {}
    files: Dict = {}


class FilterParams(BaseModel):
    min_genes: Optional[int] = 10
    max_genes: Optional[int] = None
    min_counts: int = 10
    max_counts: Optional[int] = None
    mito_controls_percentage: float = 25


class StudySubmitInfo(BaseModel):
    submission_type: str
    format: str
    files: List[Dict]
    folders: List[Dict] = []
    name: str = UNTITLED
    args: List[Dict] = []
    kwargs: List[Dict] = []
    identities: List[str] = []


def create_requests_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.1
    )
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


def request(
    url: str,
    req: RequestContent,
    mode: str = RequestMode.POST,
    verify: bool = False,
):
    session = create_requests_session()
    r: requests.Response = getattr(session, mode)(
        url, params=req.params, json=req.body_json, data=req.data,
        headers=req.headers, verify=verify, files=req.files,
        timeout=1800
    )

    if r.status_code >= 400:
        raise Exception(
            f"Call request to {url} failed with status code {r.status_code}, response {r.text}"
        )
    response = r.json()
    r.close()
    return response


def parse_to_str(data, tab_level: int = 0) -> str:
    if isinstance(data, list):
        return list_to_str(data, tab_level)
    if isinstance(data, tuple):
        return tuple_to_str(data, tab_level)
    if isinstance(data, dict):
        return dict_to_str(data, tab_level)
    return f"{data}"


def list_to_str(data: list, tab_level: int = 0) -> str:
    if len(data) == 0:
        return "[""]"
    return "[\n" + "".join([
        TAB_STRING * (tab_level + 1) +
        f"{parse_to_str(value, tab_level + 1)}\n" for value in data
    ]) + TAB_STRING * tab_level + "]"


def tuple_to_str(data: list, tab_level: int = 0) -> str:
    if len(data) == 0:
        return "("")"
    return "(\n" + "".join([
        TAB_STRING * (tab_level + 1) +
        f"{parse_to_str(value, tab_level + 1)}\n" for value in data
    ]) + TAB_STRING * tab_level + ")"


def dict_to_str(data: dict, tab_level: int = 0) -> str:
    if len(data) == 0:
        return "{""}"
    return "{\n" + "".join([
        f"{TAB_STRING * (tab_level + 1)}{key}: "
        f"{parse_to_str(value, tab_level + 1)}\n"
        for key, value in data.items()
    ]) + TAB_STRING * tab_level + "}"


def format_print(data):
    print(parse_to_str(data))


def get_chunk_size(chunk_size: int, file_size: int) -> int:
    if chunk_size > 0:
        return min(chunk_size, ConnectorKeys.UPLOAD_CHUNK_LARGE_SIZE)

    if file_size < 15*1024*1024:
        return ConnectorKeys.UPLOAD_CHUNK_SMALL_SIZE
    if file_size < 100*1024*1024:
        return ConnectorKeys.UPLOAD_CHUNK_MEDIUM_SIZE
    if file_size < 1024*1024*1024:
        return ConnectorKeys.UPLOAD_CHUNK_NORMAL_SIZE

    return ConnectorKeys.UPLOAD_CHUNK_LARGE_SIZE
