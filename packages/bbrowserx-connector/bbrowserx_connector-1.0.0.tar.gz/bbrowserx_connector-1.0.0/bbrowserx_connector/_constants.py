from typing import List

DEFAULT_GENE_VERSION = "V110"

UNTITLED = "Untitled"
TOKEN_KEY = "BBrowserX-Token"


class APIType:
    PY_API_V1 = "pyapi/v1"
    OPEN_API = "openapi"


# PyAPI
class PyAPIUrl:
    UPDATE_DEFAULT_INFO = "study/update_default_info"
    IMPORT_METADATA = "metadata/import_metadata"
    LIST_TERM_MAPPING = "ontology/list_term_mapping"
    RENAME_LAYER = "study/rename_layer"


# OpenAPI
class OpenAPIUrl:
    INFO_URL = "account/info"
    EXTERNAL_MOUNT_URL = "mount/external_listing"
    LIST_S3 = "cloud/setting_list"
    GROUPS_URL = "account/groups"
    LIST_URL = "directory/entities"

    CREATE_PROJECT_URL = "project/create"
    LIST_PROJECT_URL = "project/list"
    DETAIL_PROJECT_URL = "project/detail"
    LIST_PUBLIC_PROJECT_URL = "project/list_public"
    STOP_CREATE_SUBMIT_PROJECT_URL = "project/stop_create_submit"
    UPDATE_PROJECT_URL = "project/update"

    CREATE_STUDY_URL = "study/create"
    LIST_STUDY_URL = "study/list"
    DETAIL_STUDY_URL = "study/detail"
    STOP_CREATE_SUBMIT_STUDY_URL = "project/stop_create_submit"
    UPDATE_STUDY_URL = "study/update"

    ADD_SAMPLE_DATA_URL = "data/create"
    ADD_SAMPLE_DATA_ELEMENT_URL = "data/add_element"

    UPLOAD_FILE_URL = "upload/simple"
    UPLOAD_CHUNK_START_URL = "upload/chunk/start"
    UPLOAD_CHUNK_PROCESS_URL = "upload/chunk/process"
    UPLOAD_CHUNK_MERGE_URL = "upload/chunk/merge"
    UPLOAD_CHUNK_FINISH_URL = "upload/chunk/finish"
    UPLOAD_FOLDER_FINISH_URL = "upload/folder_finish"

    CONVERT_FROM_BBX_URL = "study/convert_from_bbx"


# Types
class StudyFormat:
    H5AD: str = "H5AD"
    SEURAT: str = "SEURAT"
    MTX_10X: str = "MTX_10X"
    H5_10X: str = "H5_10X"
    TSV: str = "TSV"
    PARSE_BIOSCIENCE: str = "PARSE_BIOSCIENCE"


class Species:
    HUMAN: str = "human"
    MOUSE: str = "mouse"
    OTHERS: str = "others"
    NON_HUMAN_PRIMATE: str = "nonHumanPrimate"


class StudyType:
    SINGLECELL_STUDY_TYPE_NUMBER: int = 1
    ATACSEQ_STUDY_TYPE_NUMBER: int = 2
    CITESEQ_STUDY_TYPE_NUMBER: int = 4
    PERTURBATION_STUDY_TYPE_NUMBER: int = 8


class StudyStatus:
    CREATED_STATUS: int = 0
    SUCCESS_STATUS: int = 1
    PROCESSING_STATUS: int = 2
    DELETE_STATUS: int = 3


class StudyFilter:
    EQUAL: int = 0
    NOT_LARGER: int = 1
    LARGER: int = 2


class DefaultGroup:
    PERSONAL_WORKSPACE: str = "Personal workspace"
    ALL_MEMBERS: str = "All members"

    BBX_GROUP_ID_PERSONAL_WORKSPACE: str = "personal"
    BBX_GROUP_ID_ALL_MEMBERS: str = "all_members"


class ConnectorKeys:
    INFORMATION_FIELDS: List[str] = [
        "email", "sub_dir", "name", "app_base_url", "routing_table"
    ]

    # Response keys
    ENTITIES: str = "entities"
    MESSAGE: str = "message"
    UNIQUE_ID: str = "unique_id"
    ROOT_FOLDER: str = "root_folder"

    # Parameter keys
    PROJECT_PATH: str = "project_path"
    PROJECT_ID: str = "project_id"
    STUDY_ID: str = "study_id"
    GROUP_ID: str = "group_id"
    AUTHOR: str = "author"
    ONTOLOGY_ID: str = "ontology_id"
    GENOME_VERSION: str = "gene_mapping_version"
    APPLY_NORMALIZE: str = "normalize"
    SUBMISSION_INFO: str = "submission_info"
    TOTAL_BATCH: str = "total_batch"
    FILTER_PARAMS: str = "filter_params"
    SPECIES: str = "species"
    LIMIT: str = "limit"
    OFFSET: str = "offset"
    ACTIVE: str = "active"
    COMPARE: str = "compare"
    NAME: str = "name"
    DATA: str = "data"
    PUBLICATION: str = "publication"
    DATA_NAME: str = "data_name"
    TITLE: str = "title"
    KEY: str = "key"
    TYPE: str = "type"
    PATH: str = "path"
    DATA_PATH: str = "data_path"
    IGNORE_HIDDEN: str = "ignore_hidden"
    FORMAT: str = "study_format"
    NEED_DATA: str = "need_data"
    LENS_DATA_PATH: str = "lens_data_path"
    GROUPS: str = "groups"
    DEFAULT: str = "default"

    # Parameter upload keys
    UPLOAD_PARENT_IS_FILE: str = "parent_is_file"
    UPLOAD_CHUNK_SIZE: str = "chunk_size"
    UPLOAD_FILE_SIZE: str = "file_size"
    UPLOAD_OFFSET: str = "offset"
    UPLOAD_FILE_NAME: str = "name"
    UPLOAD_FOLDER_NAME: str = "folder_name"
    UPLOAD_UNIQUE_ID: str = "unique_id"
    UPLOAD_PATH: str = "path"
    UPLOAD_MOVE_TO_PARENT: str = "move_to_parent"
    UPLOAD_SENDING_INDEX: str = "sending_index"
    UPLOAD_FILE_DATA: str = "file"
    UPLOAD_TOTAL_CHUNK: str = "total"
    UPLOAD_IS_CHUNK: str = "is_chunk"
    UPLOAD_CHUNK_SMALL_SIZE: int = 1024 * 1024
    UPLOAD_CHUNK_MEDIUM_SIZE: int = 16 * 1024 * 1024
    UPLOAD_CHUNK_NORMAL_SIZE: int = 50 * 1024 * 1024
    UPLOAD_CHUNK_LARGE_SIZE: int = 100 * 1024 * 1024
