from typing import List, Dict, Union, Optional, Iterable
import os
from pathlib import Path
from tqdm import tqdm

import pandas as pd

from ._api import Connector, PyAPI, OpenAPI
from ._constants import ConnectorKeys, DefaultGroup
from ._utils import get_chunk_size, format_print
from ._utils import FilterParams
from ._submit_format import SubmitFormat


class BBrowserXProConnector(Connector):
    """
    BBrowserXPro Connector
    Supporting to work with bbrowserx data via notebook.
    """

    def __init__(self, domain: str, token: str, verify_ssl: bool = False):
        """
        Construct parameters for train and query k-nearest neighbors

        Parameters
        ----------
        domain: ``str``
            BBrowserXPro domain
        token: ``str``
            User's token
        verify_ssl: ``bool``, default: False
            Verify SSL or not.
        """
        super().__init__(domain, token, verify_ssl)

        self.__pyapi = PyAPI(domain, token, verify_ssl)
        self.__openapi = OpenAPI(domain, token, verify_ssl)

    @property
    def api_type(self) -> str:
        return None

    @property
    def pyapi(self) -> PyAPI:
        return self.__pyapi

    @property
    def openapi(self) -> OpenAPI:
        return self.__openapi

    @property
    def info(self):
        """Current user's information"""
        info = self.openapi.info
        return {
            field: info[field]
            for field in ConnectorKeys.INFORMATION_FIELDS
        }

    @property
    def groups(self) -> Dict[str, str]:
        """List all reachable groups of current user in domain server."""
        group_info = self.openapi.groups
        groups = {
            v: k for k, v in group_info[ConnectorKeys.DEFAULT].items()
        }
        for group in group_info[ConnectorKeys.GROUPS]:
            groups[group["name"]] = group["id"]
        return groups

    @property
    def external_mounts(self):
        """List all reachable mounted shared folders of current user from BBrowserX/BioStudio."""
        return {
            folder["name"]: folder["path"]
            for folder in self.openapi.mounts["s3"]
        }

    @property
    def external_folders(self):
        """List all reachable mounted shared folders of current user from BBrowserX/BioStudio."""
        return {
            folder["name"]: folder["path"]
            for folder in self.openapi.mounts["folders"]
        }

    @property
    def folders(self):
        """List all reachable mounted shared folders of current user in domain server."""
        defaults = {
            folder["name"]: folder["path"]
            for folder in self.openapi.info["default_mount"]["folders"]
        }
        return dict(self.external_folders.items() | defaults.items())

    @property
    def s3(self):
        """List all reachable mounted s3 clouds of current user in domain server."""
        defaults = {
            s3["map_settings"]["name"]: s3["map_settings"]["path"]
            for s3 in self.openapi.s3
        }
        return dict(self.external_mounts.items() | defaults.items())

    def listdir(
        self,
        path: str,
        ignore_hidden: bool = True,
        get_details: bool = False,
    ) -> Union[List[Dict[str, Union[str, int, dict]]], List[str]]:
        """
        List all files and folders with path in domain server

        Parameters
        ----------
        path: ``str``
            path of folder to list
        ignore_hidden: ``bool``, default: True
            Ignore hidden files/folders or not
        get_details: ``bool``, default: False
            Get details information or not

        Returns
        -------
        results: ``Union[List[Dict[str, Union[str, int, dict]]], List[str]]``
            Folders and files with their information
        """
        dir_elements = self.openapi.list_dir(
            path, ignore_hidden=ignore_hidden
        )[ConnectorKeys.ENTITIES]
        if get_details:
            return dir_elements
        return [element[ConnectorKeys.NAME] for element in dir_elements]

    def list_project(
        self, group: str, species: str, **kwargs
    ) -> pd.DataFrame:
        """
        List reachable studies

        Parameters
        ----------
        group: ``str``
            Group of studies
        species: ``str``
            Species of studies

        Returns
        -------
        results: ``pd.DataFrame``
            List of studies include:
                - Project ID
                - Dataset ID
                - Project Title
                - Authors
                - References
                - Abstract
                - Total Study
                - Total Cell
                - Created Date
                - Last Updated Date
                - Created By

        Keyword Arguments
        -----------------
        limit: ``int``, default: 50
            Limit of responsing data
        offset: ``int``, default: 50
            Starting point of responsing data
        """
        df = pd.DataFrame(self.openapi.list_project(self.groups[group], species, **kwargs)["list"])
        df = df[
            [
                "project_id", "map_publication", "title", "map_author", "map_doi_url",
                "description", "total_study", "total_cell", "created_at", "updated_at", "email_id",
            ]
        ].rename(
            columns={
                "project_id": "Project ID",
                "map_publication": "Dataset ID",
                "title": "Project Title",
                "map_author": "Authors",
                "map_doi_url": "References",
                "description": "Abstract",
                "total_study": "Total Study",
                "total_cell": "Total Cell",
                "created_at": "Created Date",
                "updated_at": "Last Updated Date",
                "email_id": "Created By",
            }
        )

        return self._convert_datetime(df).set_index("Project ID")

    def get_project_detail(
        self, project_id: str, **kwargs
    ) -> Dict[str, Union[str, dict, List[dict]]]:
        """
        Get details information of project

        Parameters
        ----------
        project_id: ``str``
            Id of project

        Returns
        -------
        results: ``Dict[str, Union[str, dict, List[dict]]]``
            Information of project

        Keyword Arguments
        -----------------
        limit: ``int``, default: 50
            Limit of responsing data
        offset: ``int``, default: 50
            Starting point of responsing data
        """
        return self.openapi.get_project_detail(project_id, **kwargs)

    def _convert_datetime(
        self,
        df: pd.DataFrame,
        columns: List[str] = None,
    ) -> pd.DataFrame:
        if columns is None:
            columns = ["Created Date", "Last Updated Date"]
        for key in columns:
            df[key] = pd.to_datetime(df[key], unit="s").dt.strftime("%b %d, %Y")
        return df

    def list_study(self, project_id: str, **kwargs) -> pd.DataFrame:
        """
        List studies in a project

        Parameters
        ----------
        project_id: ``str``
            Id of project

        Returns
        -------
        results: ``pd.DataFrame``
            List of studies include:
                - Study ID
                - Study Title
                - Total Cell
                - Created By
                - Created Date

        Keyword Arguments
        -----------------
        limit: ``int``, default: 50
            Limit of responsing data
        offset: ``int``, default: 50
            Starting point of responsing data
        """
        df = pd.DataFrame(self.openapi.list_study(project_id, **kwargs)["list"])
        df = df[["study_id", "title", "total_cell", "email_id", "created_at", "updated_at"]].rename(
            columns={
                "study_id": "Study ID",
                "title": "Study Title",
                "total_cell": "Total Cell",
                "email_id": "Created By",
                "created_at": "Created Date",
                "updated_at": "Last Updated Date",
            }
        )
        return self._convert_datetime(df).set_index("Study ID")

    def add_study(
        self,
        project_id: str,
        name: str,
        filter_params: Dict = None,
        normalize: bool = True,
        study_data: Optional[List[dict]] = None,
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        Add a study to a existed project

        Parameters
        ----------
        project_id: ``str``
            Id of project
        name: ``str``
            Study name
        study_data: ``List[dict]``, default: []
            List of data in study, each data is result of ``parse_data_information`` function

        Returns
        -------
        results: ``Dict[str, Union[str, List[dict]]]``
            Submission information
        """
        if filter_params is None:
            filter_params = FilterParams()

        return self.openapi.create_study(
            filter_params=filter_params,
            name=name,
            normalize=normalize,
            project_id=project_id,
            submission_info=study_data)

    def submit(
        self,
        group: str,
        species: str,
        title: str,
        normalize: bool,
        study_name: str,
        study_data: List[SubmitFormat],
        author: List[str] = None,
        dataset_ids: Optional[Iterable[str]] = None,
        filter_params: Dict = None,
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        Create new project and submit the first study.

        Parameters
        ----------
        group: ``str``
            Group of project
        species: ``str``
            Species of data in project
        title: ``str``
            Title of project
        filter_params: ``Dict``
            Dict of cell-filtering parameters
        normalize: ``bool``
            Choose whether apply log-normalize or not
        study_name: ``str``
            Study name
        study_data: ``List[SubmitFormat]``
            List of data in study, each data is a child of ``SubmitFormat``

        Returns
        -------
        results: ``Dict[str, Union[str, List[dict]]]``
            Submission information
        """
        if not filter_params:
            filter_params = FilterParams().dict()

        project_id = self.openapi.create_project(
            group_id=self.groups[group],
            species=species,
            title=title,
            dataset_ids=dataset_ids,
            author=author
        )[ConnectorKeys.PROJECT_ID]

        return self.add_study(
            project_id=project_id,
            name=study_name,
            filter_params=filter_params,
            normalize=normalize,
            study_data=list(map(lambda x: x.parse(), study_data))
        )

    def upload_file(
        self,
        file_path: str,
        server_folder_name: str = "",
        upload_id: str = "",
        is_chunk: bool = False,
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        upload a small file

        Parameters
        ----------
        file_path: ``str``
            File location
        server_folder_name: ``str``
            Folder location in bbrowserxpro server
        upload_id: ``str``
            Upload ID

        Returns
        -------
        results: ``Dict[str, Union[str, List[dict]]]``
            Upload information
        """
        return self.openapi.upload_file(
            file_path=file_path,
            folder_name=server_folder_name,
            upload_id=upload_id,
            is_chunk=is_chunk,
        )

    def upload_big_file(
        self,
        file_path: str,
        chunk_size: int = 0,
        debug_mode: bool = False,
        server_folder_name: str = "",
        chunk_resp: dict = None,
        move_to_parent: bool = True,
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        Upload a big file

        Parameters
        ----------
        file_path: ``str``
            File location
        chunk_size: ``int``
            Chunk size (bytes), 0: auto
        debug_mode: ``bool``
            Debug mode
        server_folder_name: ``str``
            Folder location in bbrowserxpro server

        Returns
        -------
        results: ``Dict[str, Union[str, List[dict]]]``
            Upload information
        """

        if not os.path.isfile(file_path):
            raise ValueError(f"Invalid file: {file_path}")

        if chunk_resp is None:
            chunk_resp = {}

        file_size = os.stat(os.path.abspath(file_path)).st_size
        upload_id = ""
        resp = chunk_resp
        if ConnectorKeys.UNIQUE_ID in resp:
            upload_id = resp[ConnectorKeys.UNIQUE_ID]

        # Direct upload if small file
        if file_size < ConnectorKeys.UPLOAD_CHUNK_SMALL_SIZE:
            if ConnectorKeys.UNIQUE_ID in resp:
                upload_id = resp[ConnectorKeys.UNIQUE_ID]

            return self.upload_file(
                file_path=file_path,
                server_folder_name=server_folder_name,
                upload_id=upload_id,
                is_chunk=True,
            )

        file_name = Path(file_path).name
        item_chunk_size = get_chunk_size(chunk_size, file_size)

        if (len(resp.keys()) == 0) or (len(upload_id) == 0):
            resp = self.openapi.upload_chunk_start(
                folder_name=server_folder_name,
                parent_is_file=2,
            )

            if ConnectorKeys.UNIQUE_ID in resp:
                upload_id = resp[ConnectorKeys.UNIQUE_ID]

        file = open(file_path, "rb")
        file.seek(0, 0)
        sending_index = 0
        offset_size = 0
        progress_bar = None
        if debug_mode:
            progress_bar = tqdm(total=file_size, unit="B", unit_scale=True)

        while True:
            data = file.read(item_chunk_size)
            if not data:
                break

            offset_size = offset_size + item_chunk_size
            offset_size = min(file_size, offset_size)

            if debug_mode:
                format_print(f"Upload {file_path}, chunk index : {sending_index + 1} ...")

            self.openapi.upload_chunk_process(
                chunk_size=item_chunk_size,
                file_size=file_size,
                offset=offset_size,
                file_name=file_name,
                folder_name=server_folder_name,
                upload_id=upload_id,
                path=resp[ConnectorKeys.ROOT_FOLDER],
                sending_index=sending_index,
                parent_is_file=2,
                file_data=data,
            )

            if debug_mode:
                if progress_bar is not None:
                    progress_bar.update(len(data))

            sending_index = sending_index + 1

        total_index = sending_index
        file.close()

        resp2 = self.openapi.upload_chunk_merge(
            total_chunk=total_index,
            file_name=file_name,
            folder_name=server_folder_name,
            upload_id=upload_id,
            path=resp[ConnectorKeys.ROOT_FOLDER],
            parent_is_file=2,
            move_to_parent=move_to_parent,
        )

        if move_to_parent:
            return resp2
        return resp

    def upload_folder(
        self,
        dir_path: str,
        folder_path: Optional[str] = None,
        chunk_size: int = 0,
        debug_mode: bool = False,
        server_folder_name: str = "",
        chunk_resp: dict = None,
    ) -> bool:
        """
        Upload folder as: zarr

        Parameters
        ----------
        dir_path: ``str``
            Folder location
        chunk_size: ``int``
            Chunk size (bytes), 0: auto
        debug_mode: ``bool``
            Debug mode
        server_folder_name: ``str``
            Folder location in bbrowserxpro server
        """
        if not os.path.isdir(dir_path):
            raise ValueError(f"Invalid directory: {dir_path}")

        if chunk_resp is None:
            chunk_resp = {}
        root_folder_path = ""
        if folder_path is None:
            folder_path = server_folder_name + os.path.basename(dir_path)
            root_folder_path = str(folder_path)

        src_path = Path(dir_path)
        resp = chunk_resp

        for src_child in src_path.iterdir():
            if src_child.is_dir():
                folder_path = os.path.join(folder_path, src_child.stem)
                dst_child = os.path.join(dir_path, src_child.stem)
                self.upload_folder(
                    dir_path=dst_child, folder_path=folder_path,
                    chunk_size=chunk_size, debug_mode=debug_mode,
                    server_folder_name=server_folder_name,
                    chunk_resp=resp,
                )
            else:
                if src_child.is_symlink():
                    continue

                dst_child = os.path.join(dir_path, src_child.name)
                resp = self.upload_big_file(
                    file_path=dst_child,
                    chunk_size=chunk_size,
                    debug_mode=debug_mode,
                    server_folder_name=folder_path,
                    chunk_resp=resp,
                    move_to_parent=False,
                )

        return self.openapi.upload_folder_finish(
            root_folder_path,
            resp[ConnectorKeys.UNIQUE_ID],
        )

    def list_bbx_studies(self, host: str, token: str, group: str, species: str):
        # pylint:disable=import-outside-toplevel
        from bioturing_connector.bbrowserx_connector import BBrowserXConnector

        connector = BBrowserXConnector(host=host, token=token, ssl=True)
        connector.test_connection()
        if group == DefaultGroup.PERSONAL_WORKSPACE:
            group_id = DefaultGroup.BBX_GROUP_ID_PERSONAL_WORKSPACE
        elif group == DefaultGroup.ALL_MEMBERS:
            group_id = DefaultGroup.BBX_GROUP_ID_ALL_MEMBERS
        else:
            group_id = self.groups.get(group, group)

        studies_info = connector.get_all_studies_info_in_group(group_id=group_id, species=species)
        studies_info = [
            {
                **info,
                ConnectorKeys.SPECIES: species,
                ConnectorKeys.GROUP_ID: self.groups.get(group, DefaultGroup.PERSONAL_WORKSPACE),
            }
            for info in studies_info
        ]
        return studies_info

    def import_metadata(
            self,
            metadata_path: str,
            project_id: str,
            study_id: str,
    ):
        project_path = self.get_project_detail(project_id=project_id)["project"]["root_path"]
        self.pyapi.import_metadata(
            project_path=project_path,
            study_id=study_id,
            metadata_path=metadata_path,
        )

    def update_default_info(
            self, project_id: str, study_id: str, embedding: str = None, metadata: str = None
    ):
        """
        Update default information of a study.
        """
        self.pyapi.update_default_info(
            project_path=self.get_project_detail(project_id=project_id)["project"]["root_path"],
            study_id=study_id,
            embedding=embedding,
            metadata=metadata,
        )

    def convert_from_bbx(self, project_id: str, name: str, bbx_id: str):
        """
        Convert a study from BBrowserX to BBrowserXPro
        """
        return self.openapi.convert_from_bbx(project_id=project_id, name=name, bbx_id=bbx_id)

    def get_standardized_data(
            self, project_id: str, study_id: str, ontology_id: str,
    ) -> pd.DataFrame:
        project_path = self.get_project_detail(project_id=project_id)["project"]["root_path"]
        df = pd.DataFrame(
            self.pyapi.list_term_mapping(
                project_path=project_path, study_id=study_id, ontology_id=ontology_id
            )
        )
        return df.rename(
            columns={
                "ontology_id": "Ontology ID",
                "node_id": "Node ID",
                "metadata_field": "Metadata",
                "metadata_label": "Label",
                "created_time": "Created Time",
                "status": "Status",
            }
        )

    def get_study_by_dataset_id(self, dataset_id: str, group: str, species: str, **kwargs):
        """
        Get project id, study id from dataset id
        """
        studies = []
        projects = self.openapi.list_project(self.groups[group], species, **kwargs)["list"]
        for project in tqdm(projects):
            project_id = project["project_id"]
            bbx_id_list = project["map_publication"]
            if project["total_cell"] == 0:
                continue
            if dataset_id in bbx_id_list:
                if project["total_cell"] == 0:
                    continue
                df = self.list_study(project_id)
                df["Dataset ID"] = bbx_id_list
                df["Project ID"] = project_id
                studies.append(df)
        return pd.concat(studies)

    def delete_project(self, project_id: str, *, is_cleanup: bool = False):
        """Delete a project

        Parameters
        ----------
        project_id: ``str``
            Id of project
        is_cleanup: ``bool``, default: False
            Whether to delete the project permanently or not

        Returns
        -------
        results: ``str``
            Project ID
        """
        return self.openapi.delete(
            key_id=project_id, is_cleanup=is_cleanup, is_project=True
        )["data"]

    def restore_project(self, project_id: str):
        """Restore a project

        Parameters
        ----------
        project_id: ``str``
            Id of project

        Returns
        -------
        results: ``str``
            Project ID
        """
        return self.openapi.restore_project(project_id=project_id, is_project=True)["project_id"]

    def restore_study(self, study_id: str):
        """Restore a study

        Parameters
        ----------
        study_id: ``str``
            Id of study

        Returns
        -------
        results: ``str``
            Study ID
        """
        return self.openapi.restore_project(project_id=study_id, is_project=False)["project_id"]

    def delete_study(self, study_id: str, *, is_cleanup: bool = False):
        """Delete a study

        Parameters
        ----------
        study_id: ``str``
            Id of study
        is_cleanup: ``bool``, default: False
            Whether to delete the study permanently or not.

        Returns
        -------
        results: ``str``
            Study ID
        """
        return self.openapi.delete(key_id=study_id, is_cleanup=is_cleanup, is_project=False)["data"]

    def rename_layer(self, project_id: str, study_id: str, layer: str, new_layer: str):
        """Rename a layer of a study

        Parameters
        ----------
        project_id: ``str``
            Id of project
        study_id: ``str``
            Id of study
        layer: ``str``
            Layer name
        new_layer: ``str``
            New layer name

        Returns
        -------
        results: ``str``
            Layer name
        """
        return self.pyapi.rename_layer(
            project_path=self.get_project_detail(project_id)["project"]["root_path"],
            study_id=study_id,
            layer=layer,
            new_layer=new_layer,
        )
