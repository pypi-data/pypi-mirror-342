from typing import Union, List, Dict, Optional, Iterable
from abc import abstractmethod
import os
import json
from urllib.parse import urlparse, parse_qs
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from ._utils import request, parse_to_str
from ._utils import RequestMode, RequestContent
from ._constants import (
    StudyType,
    StudyStatus,
    StudyFilter,
    APIType,
    PyAPIUrl,
    OpenAPIUrl,
    ConnectorKeys,
    TOKEN_KEY,
    DEFAULT_GENE_VERSION,
)


class Connector:
    def __init__(
        self,
        domain: str,
        token: str,
        verify_ssl: bool = False,
    ):
        self._token = token
        self._verify_ssl = verify_ssl

        link = urlparse(domain)
        if len(link.netloc) == 0:
            raise ValueError(f"invalid domain: {domain}")

        params = dict(parse_qs(link.query))
        params = {k: v[0] for k, v in params.items()}
        self.params = params
        self._domain = f"{link.scheme}://{link.netloc}{link.path}"

    @property
    @abstractmethod
    def api_type(self) -> str:
        """Return the API type."""

    def request(
            self,
            url: str,
            req: RequestContent,
            mode: str = RequestMode.POST,
    ):
        for k, v in self.params.items():
            req.params[k] = v
        req.headers = {TOKEN_KEY: self._token}

        res = request(
            url=url.replace(os.sep, "/"),
            req=req,
            mode=mode,
            verify=self._verify_ssl
        )
        if res["status"] != 0:
            raise Exception(parse_to_str(res))

        return res[ConnectorKeys.MESSAGE]

    def post_request(
            self, url: str,
            req: RequestContent = RequestContent(),
            mode: str = RequestMode.POST,
    ) -> Union[BaseModel, str]:
        return self.request(
            os.path.join(self._domain, self.api_type, url),
            req=req,
            mode=mode
        )


class PyAPI(Connector):
    @property
    def api_type(self):
        return APIType.PY_API_V1

    def import_metadata(
            self, project_path: str, study_id: str, metadata_path: str
    ):
        return self.post_request(
            url=PyAPIUrl.IMPORT_METADATA,
            req=RequestContent(
                body_json={
                    ConnectorKeys.PROJECT_PATH: project_path,
                    ConnectorKeys.STUDY_ID: study_id,
                    "permission_name": "MODIFY_METADATA",
                    "metadata_path": metadata_path
                }
            )
        )

    def update_default_info(
            self, project_path: str, study_id: str, embedding: str = None, metadata: str = None,
    ):
        return self.post_request(
            url=PyAPIUrl.UPDATE_DEFAULT_INFO,
            req=RequestContent(
                body_json={
                    ConnectorKeys.PROJECT_PATH: project_path,
                    ConnectorKeys.STUDY_ID: study_id,
                    "embedding": embedding,
                    "metadata": metadata,
                }
            )
        )

    def list_term_mapping(
            self, ontology_id: str, project_path: str, study_id: str,
    ):
        return self.post_request(
            url=PyAPIUrl.LIST_TERM_MAPPING,
            req=RequestContent(
                body_json={
                    ConnectorKeys.PROJECT_PATH: project_path,
                    ConnectorKeys.STUDY_ID: study_id,
                    ConnectorKeys.ONTOLOGY_ID: ontology_id,
                }
            )
        )

    def rename_layer(self, project_path: str, study_id: str, layer: str, new_layer: str):
        return self.post_request(
            url=PyAPIUrl.RENAME_LAYER,
            req=RequestContent(
                body_json={
                    ConnectorKeys.PROJECT_PATH: project_path,
                    ConnectorKeys.STUDY_ID: study_id,
                    "layer": layer,
                    "new_layer": new_layer,
                }
            )
        )


class OpenAPI(Connector):
    @property
    def api_type(self):
        return APIType.OPEN_API

    @property
    def info(self):
        return self.post_request(
            url=OpenAPIUrl.INFO_URL,
            mode=RequestMode.GET,
        )

    @property
    def mounts(self):
        return self.post_request(
            url=OpenAPIUrl.EXTERNAL_MOUNT_URL,
            mode=RequestMode.GET,
        )

    def list_s3(self, offset: int = 0, limit: int = 100):
        return self.post_request(
            url=OpenAPIUrl.LIST_S3,
            req=RequestContent(
                data={
                    ConnectorKeys.LIMIT: limit,
                    ConnectorKeys.OFFSET: offset,
                }
            ),
            mode=RequestMode.POST,

        )

    @property
    def s3(self):
        return self.list_s3()

    @property
    def groups(self):
        return self.post_request(
            url=OpenAPIUrl.GROUPS_URL,
            mode=RequestMode.GET,
        )

    def list_dir(self, path: str, ignore_hidden: bool = True):
        return self.post_request(
            OpenAPIUrl.LIST_URL,
            req=RequestContent(
                data={
                    ConnectorKeys.PATH: path,
                    ConnectorKeys.IGNORE_HIDDEN: ignore_hidden,
                }
            )
        )

    def create_project(
        self,
        group_id: str,
        species: str,
        title: str,
        author: List[str] = None,
        dataset_ids: Optional[Iterable[str]] = None,
        create_type: int = StudyType.SINGLECELL_STUDY_TYPE_NUMBER,
        **kwargs
    ):
        if author is None:
            author = []
        return self.post_request(
            url=OpenAPIUrl.CREATE_PROJECT_URL,
            req=RequestContent(
                body_json={
                    ConnectorKeys.AUTHOR: author,
                    ConnectorKeys.GROUP_ID: group_id,
                    ConnectorKeys.SPECIES: species,
                    ConnectorKeys.TITLE: title,
                    ConnectorKeys.TYPE: create_type,
                    ConnectorKeys.PUBLICATION: dataset_ids,
                    **kwargs,
                }
            )
        )

    def list_project(
        self,
        group_id: str,
        species: str,
        limit: int = 50,
        offset: int = 0,
        active: int = StudyStatus.PROCESSING_STATUS,
        compare: int = StudyFilter.NOT_LARGER,
    ):
        return self.post_request(
            url=OpenAPIUrl.LIST_PROJECT_URL,
            req=RequestContent(
                data={
                    ConnectorKeys.GROUP_ID: group_id,
                    ConnectorKeys.SPECIES: species,
                    ConnectorKeys.LIMIT: limit,
                    ConnectorKeys.OFFSET: offset,
                    ConnectorKeys.ACTIVE: active,
                    ConnectorKeys.COMPARE: compare,
                }
            )
        )

    def get_project_detail(self, project_id: str, limit: int = 50, offset: int = 0):
        return self.post_request(
            url=OpenAPIUrl.DETAIL_PROJECT_URL,
            req=RequestContent(
                params={
                    ConnectorKeys.KEY: project_id,
                    ConnectorKeys.LIMIT: limit,
                    ConnectorKeys.OFFSET: offset,
                }
            ),
            mode=RequestMode.GET,
        )

    def create_study(
        self,
        name: str,
        normalize: bool,
        project_id: str,
        submission_info: List[Dict],
        filter_params: Dict = None,
    ):
        if isinstance(filter_params, Dict) and filter_params:
            filter_str = json.dumps(filter_params)
        else:
            filter_str = ""
        if len(submission_info) == 0:
            raise ValueError("Submission data is empty")

        return self.post_request(
            url=OpenAPIUrl.CREATE_STUDY_URL,
            req=RequestContent(
                body_json={
                    ConnectorKeys.FILTER_PARAMS: filter_str,
                    ConnectorKeys.GENOME_VERSION: DEFAULT_GENE_VERSION,
                    ConnectorKeys.NAME: name,
                    ConnectorKeys.APPLY_NORMALIZE: normalize,
                    ConnectorKeys.PROJECT_ID: project_id,
                    ConnectorKeys.SUBMISSION_INFO: json.dumps(submission_info),
                    ConnectorKeys.TOTAL_BATCH: len(submission_info),
                }
            )
        )

    def list_study(
        self,
        project_id: str,
        limit: int = 50,
        offset: int = 0,
        need_data: bool = False,
    ):
        return self.post_request(
            url=OpenAPIUrl.LIST_STUDY_URL,
            req=RequestContent(
                params={
                    ConnectorKeys.KEY: project_id,
                    ConnectorKeys.LIMIT: limit,
                    ConnectorKeys.OFFSET: offset,
                    ConnectorKeys.NEED_DATA: need_data,
                }
            ),
            mode=RequestMode.GET,
        )

    def get_study_detail(self, study_id: str, limit: int = 50, offset: int = 0):
        return self.post_request(
            url=OpenAPIUrl.DETAIL_STUDY_URL,
            req=RequestContent(
                params={
                    ConnectorKeys.KEY: study_id,
                    ConnectorKeys.LIMIT: limit,
                    ConnectorKeys.OFFSET: offset,
                }
            ),
            mode=RequestMode.GET,
        )

    def list_public_project(
        self,
        group_id: str,
        species: str,
        limit: int = 50,
        offset: int = 0,
        active: int = StudyStatus.PROCESSING_STATUS,
    ):
        return self.post_request(
            url=OpenAPIUrl.LIST_PUBLIC_PROJECT_URL,
            req=RequestContent(
                body_json={
                    ConnectorKeys.GROUP_ID: group_id,
                    ConnectorKeys.SPECIES: species,
                    ConnectorKeys.LIMIT: limit,
                    ConnectorKeys.OFFSET: offset,
                    ConnectorKeys.ACTIVE: active,
                }
            )
        )

    def upload_file(
        self, file_path: str,
        folder_name: str, upload_id: str,
        is_chunk: bool,
    ):
        with open(file_path, "rb") as file:
            resp = self.post_request(
                url=OpenAPIUrl.UPLOAD_FILE_URL,
                req=RequestContent(
                    data={
                        ConnectorKeys.UPLOAD_FOLDER_NAME: folder_name,
                        ConnectorKeys.UPLOAD_UNIQUE_ID: upload_id,
                        ConnectorKeys.UPLOAD_IS_CHUNK: is_chunk,
                    },
                    files={
                        ConnectorKeys.UPLOAD_FILE_DATA: file,
                    }
                )
            )
        return resp

    def upload_chunk_start(self, folder_name: str, parent_is_file: int):
        return self.post_request(
            url=OpenAPIUrl.UPLOAD_CHUNK_START_URL,
            req=RequestContent(
                body_json={
                    ConnectorKeys.UPLOAD_FOLDER_NAME: folder_name,
                    ConnectorKeys.UPLOAD_PARENT_IS_FILE: parent_is_file,
                }
            )
        )

    def upload_chunk_process(
        self,
        chunk_size: int,
        file_size: int,
        offset: int,
        file_name: str,
        folder_name: str,
        upload_id: str,
        path: str,
        sending_index: int,
        parent_is_file: int,
        file_data: list[str],
    ):
        return self.post_request(
            url=OpenAPIUrl.UPLOAD_CHUNK_PROCESS_URL,
            req=RequestContent(
                data={
                    ConnectorKeys.UPLOAD_FOLDER_NAME: folder_name,
                    ConnectorKeys.UPLOAD_PARENT_IS_FILE: parent_is_file,
                    ConnectorKeys.UPLOAD_CHUNK_SIZE: chunk_size,
                    ConnectorKeys.UPLOAD_FILE_SIZE: file_size,
                    ConnectorKeys.UPLOAD_OFFSET: offset,
                    ConnectorKeys.UPLOAD_FILE_NAME: file_name,
                    ConnectorKeys.UPLOAD_UNIQUE_ID: upload_id,
                    ConnectorKeys.UPLOAD_PATH: path,
                    ConnectorKeys.UPLOAD_SENDING_INDEX: sending_index,
                },
                files={
                    ConnectorKeys.UPLOAD_FILE_DATA: file_data,
                }
            )
        )

    def upload_chunk_merge(
        self,
        total_chunk: int,
        file_name: str,
        folder_name: str,
        upload_id: str,
        path: str,
        parent_is_file: int,
        move_to_parent: bool,
    ):
        return self.post_request(
            url=OpenAPIUrl.UPLOAD_CHUNK_MERGE_URL,
            req=RequestContent(
                body_json={
                    ConnectorKeys.UPLOAD_FOLDER_NAME: folder_name,
                    ConnectorKeys.UPLOAD_PARENT_IS_FILE: parent_is_file,
                    ConnectorKeys.UPLOAD_TOTAL_CHUNK: total_chunk,
                    ConnectorKeys.UPLOAD_FILE_NAME: file_name,
                    ConnectorKeys.UPLOAD_UNIQUE_ID: upload_id,
                    ConnectorKeys.UPLOAD_PATH: path,
                    ConnectorKeys.UPLOAD_MOVE_TO_PARENT: move_to_parent,
                }
            )
        )

    def upload_folder_finish(self, folder_name: str, upload_id: str):
        return self.post_request(
            url=OpenAPIUrl.UPLOAD_FOLDER_FINISH_URL,
            req=RequestContent(
                data={
                    ConnectorKeys.UPLOAD_FOLDER_NAME: folder_name,
                    ConnectorKeys.UPLOAD_UNIQUE_ID: upload_id,
                },
            )
        )

    def convert_from_bbx(self, project_id: str, name: str, bbx_id: str):
        return self.post_request(
            url=OpenAPIUrl.CONVERT_FROM_BBX_URL,
            req=RequestContent(
                body_json={
                    ConnectorKeys.PROJECT_ID: project_id,
                    ConnectorKeys.NAME: name,
                    "bbx_id": bbx_id,
                }
            )
        )

    def delete(self, key_id: str, is_cleanup: bool = False, is_project: bool = True):
        if is_project:
            url = OpenAPIUrl.STOP_CREATE_SUBMIT_PROJECT_URL
        else:
            url = OpenAPIUrl.STOP_CREATE_SUBMIT_STUDY_URL
        return self.post_request(
            url=url,
            req=RequestContent(
                body_json={
                    "key_id": key_id,
                    "cleanup_flg": is_cleanup,
                }
            )
        )

    def restore_project(self, project_id: str, is_project: bool = True):
        if is_project:
            url = OpenAPIUrl.UPDATE_PROJECT_URL
        else:
            url = OpenAPIUrl.UPDATE_STUDY_URL
        return self.post_request(
            url=url,
            req=RequestContent(
                body_json={
                    ConnectorKeys.PROJECT_ID: project_id,
                    "enable_status": StudyStatus.SUCCESS_STATUS,
                }
            )
        )
