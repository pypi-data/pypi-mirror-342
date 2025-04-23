import json
import queue
import tempfile
import threading
from pathlib import Path
from typing import Any, Dict, Generator, List, Literal, Optional

import duckdb
from duckdb import DuckDBPyConnection
from fsspec import AbstractFileSystem, Callback
from jinja2 import Environment, PackageLoader
from markupsafe import escape
from pydantic import BaseModel
from pydantic.main import IncEx

from .filesystem import FileSystemConfig, FSType, get_storage_filesystem
from .models import DataModel, DatasetPaths, Table


class Dataset(BaseModel):
    """A dataset is a collection of tables and schemas."""

    # TODO: Add features from the other provenance files
    # TODO: Consider making the Dataset object read-only
    id: str
    name: str
    version: str = ""  # TODO: Make this a mandatory field in the future.
    version_label: str = ""  # TODO: Make this a mandatory field in the future.
    created: str = ""  # TODO: Make this a mandatory field in the future.
    description: str = ""
    dataset_info: Dict[str, Any] = {}
    fs: FileSystemConfig | None = None  # Configuration for FS
    _fs: Any = None  # Filesystem is a private attribute not visible in the dump
    fully_populate: bool = True
    conn: Any = None  #  OLAP connection
    tables: Dict[str, Any] = {}
    errors: Optional[list] = None
    paths: DatasetPaths = DatasetPaths()

    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        serialize_as_any: bool = False,
        minimal: bool = True,
    ) -> dict[str, Any]:
        """Dump the model without unserializable attributes.

        This is an override of the Pydantic BaseModel method to exclude non-serializable
        and unessential attributes from the dump.

        TODO: Create simplified models for serialization.

        Args:
            mode (str, optional): The dumping mode. Defaults to "json".

        Returns:
            Dict: A JSON-serializable dictionary.
        """
        arguments = {
            "mode": mode,
            "include": include,
            "exclude": exclude,
            "context": context,
            "by_alias": by_alias,
            "exclude_unset": exclude_unset,
            "exclude_defaults": exclude_defaults,
            "exclude_none": exclude_none,
            "round_trip": round_trip,
            "warnings": warnings,
            "serialize_as_any": serialize_as_any,
        }
        # Enumerate attributes to backup
        backup_attr = [
            "conn",
            "_fs",
            "fs",
            "dataset_info",
            "tables",
            "paths",
        ]
        if not minimal:
            backup_attr.pop(backup_attr.index("tables"))
            backup_attr.pop(backup_attr.index("dataset_info"))
            backup_attr.pop(backup_attr.index("paths"))
            backup_attr.pop(backup_attr.index("fs"))

        backups = {}
        for attr in backup_attr:
            backups[attr] = getattr(self, attr)
            setattr(self, attr, None)

        if minimal:
            self.tables = {}
            self.dataset_info = {}

        dump_json = super().model_dump(**arguments)

        # Restore attributes from backup
        for attr in backup_attr:
            setattr(self, attr, backups[attr])

        return dump_json

    def render_dataset_READMEs(self):
        """Render the README file for the version of the dataset."""
        templates = {
            "dataset": {
                "template": "dataset_README.md.j2",
                "output": self.paths.dataset_path / "README.md",
            },
            "version": {
                "template": "version_README.md.j2",
                "output": self.paths.provenance_path / "README.md",
            },
            "versions": {
                "template": "versions_README.md.j2",
                "output": self.paths.version_path / "README.md",
            },
        }

        for _, template in templates.items():
            env = Environment(
                loader=PackageLoader("fw_dataset", "templates"),
                autoescape=True,
            )
            readme_template = env.get_template(template["template"])

            # Render the template
            rendered_content = readme_template.render(
                dataset=self,
                tables={
                    name: {"description": escape(table.description)}
                    for name, table in self.tables.items()
                },
            )

            # Write with explicit encoding
            with self._fs.open(template["output"], "w", encoding="utf-8") as f:
                f.write(rendered_content)

    def save(self):
        """Save the dataset to the filesystem."""
        dataset_description_path = (
            self.paths.provenance_path / "dataset_description.json"
        )

        self._fs.write_text(
            dataset_description_path,
            json.dumps(
                self.model_dump(mode="json", minimal=False, exclude="fs"), indent=4
            ),
        )
        self.render_dataset_READMEs()

    def list_versions(self) -> List[str]:
        """Get the versions of the dataset."""
        versions = []
        latest_version_path = self.paths.dataset_path / "latest"
        latest_version_desc_path = (
            latest_version_path / "provenance/dataset_description.json"
        )
        if self._fs.exists(latest_version_desc_path):
            with self._fs.open(latest_version_desc_path) as f:
                dataset_description = json.load(f)
                latest_version = dataset_description["version"]
                version_label = dataset_description.get("version_label", latest_version)
                version_rec = {
                    "version": latest_version,
                    "label": f"{version_label}",
                    "latest": True,
                }
                versions.append(version_rec)

        versions_path = self.paths.dataset_path / "versions"
        if not self._fs.exists(versions_path):  # No versions found
            return versions
        for version_path in self._fs.ls(versions_path):
            version = Path(version_path).name
            dataset_description_path = (
                versions_path / version / "provenance/dataset_description.json"
            )
            if not self._fs.exists(dataset_description_path):
                continue
            with self._fs.open(dataset_description_path) as f:
                dataset_description = json.load(f)
                version_str = dataset_description["version"]
                version_label = dataset_description.get("version_label", version_str)
                version_rec = {
                    "version": version_str,
                    "label": version_label,
                    "latest": False,
                }
                versions.append(version_rec)
        return versions

    def delete_version(self, version: str):
        """Delete a version of the dataset.

        You cannot delete the latest version of the dataset.

        Args:
            version (str): The version of the dataset to delete.
        """
        if version == "latest":
            raise ValueError("Cannot delete the latest version of the dataset")

        version_path = self.paths.dataset_path / f"versions/{version}"
        self._fs.rm(str(version_path), recursive=True)

    def get_olap_connection(self):
        """Connect to the OLAP database.

        TODO: Add support for other OLAP databases or Cloud OLAP services.
        """
        if not self.conn:
            # Initialize OLAP connection
            # TODO: Create configurations that allow chdb, starrocks, etc.
            self.conn = duckdb.connect()

    def init_fs(self):
        """Initialize the filesystem for the dataset based on credentials."""
        filesystem = get_storage_filesystem(self.fs.type_, self.fs.credentials)
        self._fs = filesystem

    def set_filesystem(self, type: FSType, credentials: dict[str, str] | None) -> None:
        """Set the filesystem for the dataset.

        Args:
            filesystem (AbstractFileSystem): The filesystem to set for the dataset.
        """
        self.fs = FileSystemConfig(type_=type, credentials=credentials)
        filesystem = get_storage_filesystem(self.fs.type_, self.fs.credentials)
        self._fs = filesystem

    def get_filesystem(self) -> AbstractFileSystem:
        """Get the filesystem for the dataset.

        Returns:
            AbstractFileSystem: The filesystem for the dataset.
        """
        return self._fs

    def setup_paths(self, version: str = "latest"):
        """Setup the paths for the dataset."""
        # TODO: Enforce having a valid filesystem
        self.paths.root_path = Path(self.dataset_info["bucket"])
        self.paths.dataset_path = self.paths.root_path / self.dataset_info["prefix"]
        # Check if this is the latest version
        if version != "latest":
            latest_version_path = (
                self.paths.dataset_path
                / "latest/provenance"
                / "dataset_description.json"
            )
            if self._fs.exists(latest_version_path):
                with self._fs.open(latest_version_path) as f:
                    dataset_description = json.load(f)
                    if dataset_description["version"] == version:
                        version = "latest"

        if version == "latest":
            version_path = self.paths.dataset_path / version
        else:
            version_path = self.paths.dataset_path / f"versions/{version}"
        self.paths.version_path = version_path
        self.paths.schemas_path = self.paths.version_path / "schemas"
        self.paths.tables_path = self.paths.version_path / "tables"
        self.paths.provenance_path = self.paths.version_path / "provenance"
        self.paths.files_cache_path = self.paths.version_path / "files_cache"
        # TODO: Check if paths are populated in a valid manner
        for ds_path in self.paths.model_dump(mode="json").values():
            self._fs.makedirs(str(ds_path), exist_ok=True)

    def get_table_schema(self, table_name: str) -> Table:
        """Load the schema for a table.

        Args:
            table_name (str): The name of the table to load the schema for.

        Returns:
            Table: The table object with the schema loaded.
        """
        schema_path = self.paths.schemas_path / f"{table_name}.schema.json"
        schema = json.loads(self._fs.read_text(schema_path))
        return Table(
            name=table_name,
            description=schema.get("description", ""),
            data_model=DataModel(**schema),
        )

    def initialize_table_schemas(self):
        """Initialize the schemas for all the tables."""
        schema_search_str = str(self.paths.schemas_path / "*.schema.json")
        table_names = [
            Path(table).name.split(".")[0] for table in self._fs.glob(schema_search_str)
        ]
        for table_name in table_names:
            # TODO: Give status bar update on the registration of the tables.
            table = self.get_table_schema(table_name)
            self.tables[table.name] = table

    def populate_tables(self):
        """Populate the tables with the data from the filesystem.

        TODO: Add support for other file formats and data sources.
        """
        # Avoid circular import
        from .admin.admin_helpers import register_arrow_virtual_table

        for table_name in self.tables.keys():
            table_path = self.paths.tables_path / table_name
            if self._fs.exists(table_path):
                register_arrow_virtual_table(
                    self.conn, self._fs, table_name, table_path
                )

    def load_dataset_description(self) -> None:
        """Load the dataset description from the filesystem.

        Updates the current dataset object with properties from the dataset description file,
        excluding the paths attribute which should be managed separately.
        """
        dataset_description_path = (
            self.paths.provenance_path / "dataset_description.json"
        )
        if not self._fs.exists(dataset_description_path):
            raise ValueError("Dataset description not found")

        with self._fs.open(dataset_description_path) as f:
            dataset_description = json.load(f)
            # Remove paths from dataset_description if present
            dataset_description.pop("paths", None)

            # Update current object's attributes with values from description
            for key, value in dataset_description.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def connect(
        self, version: str = "latest", fully_populate: bool = True, first: bool = True
    ) -> DuckDBPyConnection:
        """Connect to the OLAP database and populate the tables.

        TODO: Add support for other OLAP databases or Cloud OLAP services.
        TODO: Add support to load tables only when identified in the query.

        Args:
            version (str, optional): The version of the dataset to connect to. Defaults to "latest".
            fully_populate (bool, optional): Fully populate the tables. Defaults to True.
            first: Initialize paths and table schemas.
                This argument is meant to be used to avoid re-initializing the
                paths and table when re-connecting to a dataset from a model
                dump.

        Returns:
            DuckDBPyConnection: A connection to the OLAP database.
        """
        # Make retrieving the storage_creds entirely transient
        self.fully_populate = fully_populate
        self.init_fs()
        if first:
            self.setup_paths(version=version)
            self.load_dataset_description()
            self.initialize_table_schemas()

        self.get_olap_connection()
        if fully_populate:
            self.populate_tables()
        return self.conn

    def execute(self, query: str) -> DuckDBPyConnection:
        """Execute a query on the OLAP database.

        Args:
            query (str): A SQL query to execute.

        Raises:
            ValueError: If no OLAP connection is found.

        Returns:
            DuckDBPyConnection: The results from the query.
        """
        if not self.conn:
            raise ValueError("No OLAP connection found")
        return self.conn.execute(query)

    def download(self, dest: Path, force: bool = False) -> Generator[str, None, None]:
        """Download the dataset to a local database.

        Args:
            dest (Path): The destination directory to download the dataset to.
        """
        dest.mkdir(parents=True, exist_ok=True)

        # Callback to pass to fsspec to update queue on file download progress
        class QueueCallback(Callback):
            def __init__(self, queue, *args, **kargs):
                super().__init__(*args, **kargs)
                self.queue = queue

            def call(self, **_kwargs):
                # Currently just puts an incremental counter starting at 0
                self.queue.put(self.value)

        def producer(q: queue.Queue, force):
            db = duckdb.connect(dest / "dataset.db")
            existing_tables = set([row[0] for row in db.sql("SHOW TABLES").fetchall()])
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir_path = Path(temp_dir)
                # TODO: Switch to ThreadPoolExecutor and `self._fs.expand_path(recursive=True)`
                self._fs.download(
                    str(self.paths.tables_path),
                    str(temp_dir_path),
                    callback=QueueCallback(q),
                    recursive=True,
                )
                for table in self.tables.keys():
                    table_path = temp_dir_path / "tables" / table
                    if table in existing_tables:
                        if force:
                            db.sql(f"DROP TABLE {table}")
                        else:
                            q.put(
                                f"Skipping table {table} because it already exists in the database"
                            )
                            continue

                    db.sql(
                        f"CREATE TABLE {table} AS SELECT * FROM read_parquet('{table_path}/*')"
                    )
                    q.put(f"Created table {table}")

        def consumer(q: queue.Queue, producer_thread: threading.Thread):
            # Yield queue values while the producer thread is alive
            while producer_thread.is_alive() or not q.empty():
                try:
                    item = q.get(timeout=1)
                    yield item
                except queue.Empty:
                    pass

        q = queue.Queue()
        # Start producer thread and yield values from consumer
        producer_thread = threading.Thread(target=producer, args=(q, force))
        producer_thread.start()
        for value in consumer(q, producer_thread):
            yield value
        # Finally finish producer thread
        producer_thread.join()

    @classmethod
    def get_dataset_from_filesystem(
        cls, fs_type, bucket, prefix, credentials
    ) -> "Dataset":
        """Create a dataset object from an authenticated filesystem.

        Fileystem Types are "s3", "gs", "az", "fs" (local).

        credentials must be a dictionary with a url key for the credential string in the
        following format for each filesystem type:
        {'url': 's3://{bucket}?access_key_id={access_key_id}&secret_access_key={secret_access_key}'}
        {'url': 'gs://{bucket}?application_credentials={
            "type": "service_account",
            "project_id": "{project_id}",
            "private_key_id": "{private_key_id}",
            "private_key": "{private_key}",
            "client_email": "{email}",
            "client_id": "{client_id}",
            "auth_uri":"{auth_uri}",
            "token_uri":"{token_uri}",
            "auth_provider_x509_cert_url":"{auth_provider_x509_cert_url}",
            "client_x509_cert_url":"{client_x509_cert_url}",
            "universe_domain": "googleapis.com"
            }'
        }
        {'url': 'az://{account_name}.blob.core.windows.net/{container}?access_key={access_key}'}

        Args:
            fs_type (str): The type of filesystem to use. Options are "s3", "gs", "az", "fs".
            bucket (str): The bucket, container, or root directory of the dataset.
            prefix (str): The path from the bucket to the dataset.
            credentials (dict): A dictionary with a url key for the credential string.

        Returns:
            Dataset: A dataset object.
        """
        # Create the filesystem with the credentials and we discard the credentials
        filesystem = get_storage_filesystem(fs_type, credentials)

        # build the path to the latest version of the dataset
        dataset_path = Path(f"{bucket}/{prefix}")
        latest_version_path = dataset_path / "latest"
        dataset_description_path = (
            latest_version_path / "provenance" / "dataset_description.json"
        )

        # load the dataset description from the filesystem
        dataset_description = json.loads(filesystem.read_text(dataset_description_path))

        # instantiate the dataset object from the dataset description
        dataset = cls(**dataset_description)
        dataset.fs = FileSystemConfig(type_=fs_type, credentials=credentials)
        dataset._fs = filesystem
        dataset.setup_paths()
        # set the filesystem and dataset info
        dataset.dataset_info = {"bucket": bucket, "prefix": prefix, "type": fs_type}

        return dataset
