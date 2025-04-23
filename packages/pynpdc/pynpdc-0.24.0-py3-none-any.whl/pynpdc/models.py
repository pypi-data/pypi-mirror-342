from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date, datetime
from enum import Enum
import json
import requests
from typing import (
    Any,
    BinaryIO,
    Dict,
    Generic,
    Iterator,
    Optional,
    Tuple,
    TypedDict,
    TypeVar,
    TYPE_CHECKING,
)
from typing_extensions import NotRequired, Self, Unpack
from urllib.parse import urlencode
import urllib3
import uuid

from .exception import MissingClientException
from .utils import to_datetime, guard_utc_datetime

if TYPE_CHECKING:  # pragma: no cover
    from .auth_client import AuthClient
    from .data_client import DataClient


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------


DEFAULT_CHUNK_SIZE = 50

# ------------------------------------------------------------------------------
# Enums
# ------------------------------------------------------------------------------


class AccessLevel(Enum):
    """
    The access level of an account

    Attributes:
        EXTERNAL  enum value for an external user
        INTERNAL  enum value for an internal user with a @npolar.no email address
        ADMIN     enum value for an admin user
    """

    EXTERNAL = "external"
    INTERNAL = "internal"
    ADMIN = "admin"


class DatasetType(Enum):
    """
    The type of a dataset

    Attributes:
        DRAFT     enum value for a draft dataset. It can be made internal or
                  public in the frontend
        INTERNAL  enum value for an internal dataset
        PUBLIC    enum value for a public dataset
    """

    DRAFT = "draft"
    INTERNAL = "internal"
    PUBLIC = "public"


class LabelType(Enum):
    """
    The type of a label

    Attributes:
        PROJECT  enum value for a project label
    """

    PROJECT = "project"


# ------------------------------------------------------------------------------
# Type aliases
# ------------------------------------------------------------------------------


Content = Dict[str, Any]


# ------------------------------------------------------------------------------
# API Responses (TypedDict)
# ------------------------------------------------------------------------------


class AccountAPIResponse(TypedDict):
    id: str
    email: str
    accessLevel: str
    directoryUser: bool


class AccountWithTokenAPIResponse(AccountAPIResponse):
    token: str


class KeepaliveAPIResponse(TypedDict):
    token: str


class PermissionAPIResponse(TypedDict):
    objectId: str
    userId: str
    mayDelete: bool
    mayRead: bool
    mayUpdate: bool


class BaseModelAPIResponse(TypedDict):
    created: str
    createdBy: str
    id: str
    modified: str
    modifiedBy: str
    permissions: PermissionAPIResponse


class AttachmentAPIResponse(BaseModelAPIResponse):
    byteSize: int
    datasetId: str
    description: str
    filename: str
    mimeType: str
    prefix: str
    released: str
    sha256: str
    title: str


class DatasetAPIResponse(BaseModelAPIResponse):
    content: Content
    doi: Optional[str]
    published: str
    publishedBy: str
    type: str


class LabelAPIResponse(TypedDict):
    id: str
    created: str
    createdBy: str
    modified: str
    modifiedBy: str
    type: str
    title: str
    url: str


class PrefixAPIResponse(TypedDict):
    byteSize: int
    datasetId: str
    fileCount: int
    id: str
    prefix: str


class RecordAPIResponse(BaseModelAPIResponse):
    content: Content
    datasetId: str
    parentId: Optional[str]
    type: str


class RecordInfoAPIResponse(TypedDict):
    numProcessed: int
    numCreated: int
    numConflict: int


class UploadInfoAPIResponse(TypedDict):
    id: str
    fileName: str
    sha256: str


# ------------------------------------------------------------------------------
# Account and auth models
# ------------------------------------------------------------------------------


class Account:
    """
    A basic account object.

    Attributes:
        raw (AccountAPIResponse): The API response data parsed from JSON
        client (AuthClient | None): The client for the auth module
    """

    def __init__(
        self, raw: AccountAPIResponse, *, client: Optional[AuthClient] = None
    ) -> None:
        """
        Initialize an instance of the Account model class.

        Args:
            raw (AccountAPIResponse): The API response as parsed JSON
            client (AuthClient): The used auth client
        """
        self.client: Optional[AuthClient] = client
        self.access_level: AccessLevel = AccessLevel(raw["accessLevel"])
        self.directory_user: bool = raw.get("directoryUser", False)
        self.email: str = raw["email"]
        self.id: uuid.UUID = uuid.UUID(raw["id"])


class AuthContainer:
    """
    A container that can be used for authentification.

    Attributes:
        token (str): the auth token used for authentification

    """

    def __init__(self, token: str) -> None:
        """
        Initialize an instance of the AuthContainer class.

        Args:
            token (str): the auth token used for authentification
        """
        self.token: str = token

    @property
    def headers(self) -> dict[str, str]:
        """
        Retreive the header(s) for an authorized HTTP request

        Returns:
            dict[str, str]: The auth headers
        """
        return {"Authorization": f"Bearer {self.token}"}


class AccountWithToken(AuthContainer, Account):
    """
    A logged in account with token. Inherits from AuthContainer and Account

    Attributes:
        raw (AccountWithTokenAPIResponse): The API response data parsed from JSON
        client (AuthClient | None): The client for the auth module
    """

    def __init__(
        self, raw: AccountWithTokenAPIResponse, *, client: Optional[AuthClient] = None
    ) -> None:
        """
        Initialize an instance of the AccountWithToken model class.

        Args:
            raw (AccountWithTokenAPIResponse): The API response as parsed JSON
            client (AuthClient): The used auth client
        """

        Account.__init__(self, raw, client=client)
        AuthContainer.__init__(self, raw["token"])


# ------------------------------------------------------------------------------
# Permission model
# ------------------------------------------------------------------------------


class Permission:
    def __init__(self, raw: PermissionAPIResponse):
        """
        Initialize an instance of a Permission.

        Args:
            raw (PermissionAPIResponse): The API response as parsed JSON
        """

        self.object_id: uuid.UUID = uuid.UUID(raw["objectId"])
        self.user_id: Optional[uuid.UUID] = None
        if "userId" in raw:
            self.user_id = uuid.UUID(raw["userId"])
        self.may_read: bool = raw["mayRead"]
        self.may_update: bool = raw["mayUpdate"]
        self.may_delete: bool = raw["mayDelete"]


# ------------------------------------------------------------------------------
# Generic data models
# ------------------------------------------------------------------------------

R = TypeVar(
    "R",
    AttachmentAPIResponse,
    DatasetAPIResponse,
    LabelAPIResponse,
    PrefixAPIResponse,
    RecordAPIResponse,
)


class Model(Generic[R], ABC):
    """
    A single Model as Dataset or Attachment, that has been retrieved using the
    DataClient.

    Attributes:
        client (DataClient | None) The client for the dataset module
    """

    def __init__(self, raw: R, *, client: Optional[DataClient] = None):
        """
        Initialize an instance of a model class as Dataset or Attachment.

        Args:
            raw (R): The API response as parsed JSON
            client (DataClient): The used dataset client
        """

        self.client: Optional[DataClient] = client
        self.id: uuid.UUID = uuid.UUID(raw["id"])


class Attachment(Model[AttachmentAPIResponse]):
    """
    The metadata of a single Attachment retrieved from the NPDC dataset module.
    """

    def __init__(
        self, raw: AttachmentAPIResponse, *, client: Optional[DataClient] = None
    ) -> None:
        super().__init__(raw, client=client)

        self.created: Optional[datetime] = to_datetime(raw["created"])
        self.created_by: uuid.UUID = uuid.UUID(raw["createdBy"])
        self.modified: Optional[datetime] = to_datetime(raw["modified"])
        self.modified_by: uuid.UUID = uuid.UUID(raw["modifiedBy"])
        if "permissions" in raw:
            self.permissions: Optional[Permission] = Permission(raw["permissions"])

        self.byte_size: int = raw["byteSize"]
        self.dataset_id: uuid.UUID = uuid.UUID(raw["datasetId"])
        self.description: str = raw["description"]
        self.filename: str = raw["filename"]
        self.mime_type: str = raw["mimeType"]
        self.prefix: str = raw["prefix"]
        self.released: Optional[datetime] = to_datetime(raw["released"])
        self.sha256: str = raw["sha256"]
        self.title: str = raw["title"]

    def reader(self) -> urllib3.response.HTTPResponse:
        """
        Retrieve a reader to stream the attachment content.

        This is a shortcut for DataClient.get_attachment_reader.

        Raises:
            MissingClientException: when no DataClient is available

        Returns:
            urllib3.response.HTTPResponse: a response object with read access to
                the body

        """
        if self.client is None:
            raise MissingClientException()
        return self.client.get_attachment_reader(self.dataset_id, self.id)


class Dataset(Model[DatasetAPIResponse]):
    """
    The metadata of a single Dataset retrieved from the NPDC dataset module.

    The user generated metadata as dataset title, geographical information,
    contributors or timeframes are found in the content property.
    """

    def __init__(
        self, raw: DatasetAPIResponse, *, client: Optional[DataClient] = None
    ) -> None:
        super().__init__(raw, client=client)

        self.created: Optional[datetime] = to_datetime(raw["created"])
        self.created_by: uuid.UUID = uuid.UUID(raw["createdBy"])
        self.modified: Optional[datetime] = to_datetime(raw["modified"])
        self.modified_by: uuid.UUID = uuid.UUID(raw["modifiedBy"])
        if "permissions" in raw:
            self.permissions: Optional[Permission] = Permission(raw["permissions"])

        self.content: Content = raw["content"]
        self.doi: Optional[str] = raw["doi"]
        self.published: Optional[datetime] = to_datetime(raw["published"])
        self.type = DatasetType(raw["type"])

        self.published_by: Optional[uuid.UUID] = None
        published_by = raw["publishedBy"]
        if published_by != "":
            self.published_by = uuid.UUID(published_by)

    def get_attachments(self, **query: Unpack[AttachmentQuery]) -> AttachmentCollection:
        """
        Retrieve attachment metadata filtered by query for the dataset.

        This is a shortcut for DataClient.get_attachments.

        Args:
            query (dict): optional query parameters for filtering

        Raises:
            MissingClientException: when no DataClient is available

        Returns:
            AttachmentCollection: a lazy collection of attachments
        """
        if self.client is None:
            raise MissingClientException()
        return self.client.get_attachments(self.id, **query)

    def get_records(self, **query: Unpack[RecordQuery]) -> RecordCollection:
        """
        Retrieve records by query for the dataset.

        This is a shortcut for DataClient.get_records.

        Args:
            query (dict): optional query parameters for filtering

        Raises:
            MissingClientException: when no DataClient is available

        Returns:
            RecordCollection: a lazy collection of records
        """
        if self.client is None:
            raise MissingClientException()
        return self.client.get_records(self.id, **query)

    def download_attachments_as_zip(self, target_dir: str) -> str:
        """
        Download all dataset attachments as a zip file.

        This is a shortcut for DataClient.download_attachments_as_zip.

        Args:
            target_dir (str): the target directory where the ZIP file should be
                saved.

        Raises:
            MissingClientException: when no DataClient is available

        Returns:
            str: The path of the downloaded ZIP file
        """
        if self.client is None:
            raise MissingClientException()
        return self.client.download_attachments_as_zip(self.id, target_dir)


class Label(Model[LabelAPIResponse]):
    """
    The metadata of a NPDC label
    """

    def __init__(
        self, raw: LabelAPIResponse, *, client: Optional[DataClient] = None
    ) -> None:
        super().__init__(raw, client=client)

        self.created: Optional[datetime] = to_datetime(raw["created"])
        self.created_by: uuid.UUID = uuid.UUID(raw["createdBy"])
        self.modified: Optional[datetime] = to_datetime(raw["modified"])
        self.modified_by: uuid.UUID = uuid.UUID(raw["modifiedBy"])
        self.title: str = raw["title"]
        self.type: LabelType = LabelType(raw["type"])
        self.url: Optional[str] = raw.get("url")


class Prefix(Model[PrefixAPIResponse]):
    """The prefix data"""

    def __init__(
        self, raw: PrefixAPIResponse, *, client: Optional[DataClient] = None
    ) -> None:
        super().__init__(raw, client=client)

        self.prefix: str = raw["prefix"]
        self.dataset_id: uuid.UUID = uuid.UUID(raw["datasetId"])
        self.file_count: int = raw["fileCount"]
        self.byte_size: int = raw["byteSize"]


class Record(Model[RecordAPIResponse]):
    """
    The metadata of a single record retrieved from the NPDC dataset module.
    """

    def __init__(
        self, raw: RecordAPIResponse, *, client: Optional[DataClient] = None
    ) -> None:
        super().__init__(raw, client=client)

        self.created: Optional[datetime] = to_datetime(raw["created"])
        self.created_by: str = raw["createdBy"]
        self.modified: Optional[datetime] = to_datetime(raw["modified"])
        self.modified_by: str = raw["modifiedBy"]

        self.content: Content = raw["content"]
        self.dataset_id: uuid.UUID = uuid.UUID(raw["datasetId"])
        self.id: uuid.UUID = uuid.UUID(raw["id"])
        self.parent_id: Optional[uuid.UUID] = None
        if "parentId" in raw:
            self.parent_id = uuid.UUID(raw["parentId"])
        self.type: str = raw["type"]


# ------------------------------------------------------------------------------
# Queries
# ------------------------------------------------------------------------------

AttachmentQuery = TypedDict(
    "AttachmentQuery",
    {
        # see https://beta.data.npolar.no/-/docs/dataset/#/attachment/get_dataset__datasetID__attachment_
        "skip": NotRequired[int],
        "take": NotRequired[int],
        "count": NotRequired[bool],
        "q": NotRequired[str],
        "prefix": NotRequired[str],  # starts and ends with /
        "recursive": NotRequired[bool],
        "from": NotRequired[date],
        "until": NotRequired[date],
    },
)

AttachmentZIPQuery = TypedDict(
    "AttachmentZIPQuery",
    {
        # see https://beta.data.npolar.no/-/docs/dataset/#/attachment/get_dataset__datasetID__attachment__blob
        "skip": NotRequired[int],
        "take": NotRequired[int],
        "count": NotRequired[bool],
        "q": NotRequired[str],
        "prefix": NotRequired[str],  # starts and ends with /
        "recursive": NotRequired[bool],
        "zip": NotRequired[bool],
    },
)

DatasetQuery = TypedDict(
    "DatasetQuery",
    {
        # see https://beta.data.npolar.no/-/docs/dataset/#/dataset/get_dataset_
        "q": NotRequired[str],
        "location": NotRequired[str],  # WTF format
        "skip": NotRequired[int],
        "take": NotRequired[int],
        "count": NotRequired[bool],
        "type": NotRequired[DatasetType],
        "from": NotRequired[date],
        "until": NotRequired[date],
    },
)

LabelQuery = TypedDict(
    "LabelQuery",
    {
        # see https://beta.data.npolar.no/-/docs/dataset/#/label/get_dataset__datasetID__label_
        "dataset_id": NotRequired[str],
        "q": NotRequired[str],
        "type": NotRequired[LabelType],
        "skip": NotRequired[int],
        "take": NotRequired[int],
        "count": NotRequired[bool],
    },
)

PrefixQuery = TypedDict(
    "PrefixQuery",
    {
        # https://beta.data.npolar.no/-/docs/dataset/#/prefix/get_dataset__datasetID__prefix_
        "skip": NotRequired[int],
        "take": NotRequired[int],
        "count": NotRequired[bool],
        "q": NotRequired[str],
        "prefix": NotRequired[str],
        "recursive": NotRequired[bool],
    },
)

RecordQuery = TypedDict(
    "RecordQuery",
    {
        # https://beta.data.npolar.no/-/docs/dataset/#/record/get_dataset__datasetID__record_
        "skip": NotRequired[int],
        "take": NotRequired[int],
        "count": NotRequired[bool],
    },
)

Q = TypeVar(
    "Q",
    AttachmentQuery,
    AttachmentZIPQuery,
    DatasetQuery,
    LabelQuery,
    PrefixQuery,
    RecordQuery,
)


class QuerySerializer(Generic[Q], ABC):
    def prepare(self, query: Q) -> dict[str, Any]:
        kv = {**query}

        if query.get("count"):
            kv["count"] = "true"
        else:
            kv.pop("count", False)

        return kv

    def __call__(self, query: Q) -> str:
        if len(query) == 0:
            return ""
        return "?" + urlencode(self.prepare(query))


class AttachmentQuerySerializer(QuerySerializer[AttachmentQuery]):
    def prepare(self, query: AttachmentQuery) -> dict[str, Any]:
        kv = super().prepare(query)

        if query.get("recursive"):
            kv["recursive"] = "true"
        else:
            kv.pop("recursive", False)

        if query.get("from"):
            kv["from"] = query["from"].isoformat()

        if query.get("until"):
            kv["until"] = query["until"].isoformat()

        return kv


class AttachmentZIPQuerySerializer(QuerySerializer[AttachmentZIPQuery]):

    def prepare(self, query: AttachmentZIPQuery) -> dict[str, Any]:
        kv = super().prepare(query)

        if query.get("recursive"):
            kv["recursive"] = "true"
        else:
            kv.pop("recursive", False)

        if "zip" in query:
            kv["zip"] = "true"  # can contain any value
        else:
            kv.pop("zip", False)

        return kv


class DatasetQuerySerializer(QuerySerializer[DatasetQuery]):
    def prepare(self, query: DatasetQuery) -> dict[str, Any]:
        kv = super().prepare(query)

        if query.get("type"):
            kv["type"] = query["type"].value

        if query.get("from"):
            kv["from"] = query["from"].isoformat()

        if query.get("until"):
            kv["until"] = query["until"].isoformat()

        return kv


class LabelQuerySerializer(QuerySerializer[LabelQuery]):
    pass


class PrefixQuerySerializer(QuerySerializer[PrefixQuery]):

    def prepare(self, query: PrefixQuery) -> dict[str, Any]:
        kv = super().prepare(query)

        if query.get("recursive"):
            kv["recursive"] = "true"
        else:
            kv.pop("recursive", False)

        return kv


class RecordQuerySerializer(QuerySerializer[RecordQuery]):
    pass


QS = TypeVar(
    "QS",
    AttachmentQuerySerializer,
    DatasetQuerySerializer,
    LabelQuerySerializer,
    PrefixQuerySerializer,
    RecordQuerySerializer,
)

# ------------------------------------------------------------------------------
# Collections
# ------------------------------------------------------------------------------

T = TypeVar("T", Attachment, Dataset, Label, Prefix, Record)


class LazyCollection(Generic[T, Q, QS], ABC):
    model_class: type[T]  # ClassVar

    def __init__(
        self,
        *,
        client: DataClient,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        query: Q,
    ) -> None:
        if chunk_size < 1 or chunk_size > 255:
            raise ValueError("Chunk size have to be between 1 and 255")

        self.client: DataClient = client
        self.chunk_size: int = chunk_size
        self._generator: Iterator[T] = self._generate()
        # request
        self.query: Q = query
        self.query_serializer: QS
        # response
        self.count: Optional[int] = None

    @property
    @abstractmethod
    def _endpoint(self) -> str:
        pass

    def _request(self, query: Q) -> requests.Response:
        # TODO: fix typing issue and remove type:ignore flag
        url = self._endpoint + self.query_serializer(query)  # type:ignore
        return self.client._exec_request("GET", url)

    def _generate(self) -> Iterator[T]:
        skip = self.query.get("skip", 0)
        take = self.query.get("take")  # if not set, fetch all items
        fetch_count = self.query.get("count")
        chunk_size = self.chunk_size
        if take is not None and take < chunk_size:
            chunk_size = take

        query = self.query.copy()
        query["take"] = chunk_size
        query["skip"] = skip

        c = 0
        while True:
            resp = self._request(query)
            raw = resp.json()

            if fetch_count:
                self.count = raw["count"]
                fetch_count = None

            items = raw["items"]

            for data in items:
                yield self.model_class(data, client=self.client)
                c += 1
                if take is not None and c >= take:
                    return  # data complete

            if len(items) < chunk_size:
                break  # no more chunks

            query["skip"] += query["take"]

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> T:
        return next(self._generator)


class AttachmentCollection(
    LazyCollection[Attachment, AttachmentQuery, AttachmentQuerySerializer]
):
    """
    A generator to retrieve Attachment models in a lazy way.

    AttachmentCollection will retrieve models in chunks and yield each model
    until all models for the query have been received.

    Attributes:
        dataset_id (str): the ID of the dataset the attachment is related to
        client (DataClient): the client used to request models
        chunk_size (int): the number of models fetched per chunk size
        skip (int): the number of models to skip
        take (int): the number of models to retrieve
        query (dict): additional query parameters. Check the API documentation
            for details:
            https://beta.data.npolar.no/-/docs/dataset/#/attachment/get_dataset__datasetId__attachment_
    """

    model_class = Attachment
    query_serializer = AttachmentQuerySerializer()

    def __init__(
        self,
        dataset_id: uuid.UUID,
        *,
        client: DataClient,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        query: AttachmentQuery,
    ) -> None:
        super().__init__(client=client, chunk_size=chunk_size, query=query)
        self.dataset_id = dataset_id

    @property
    def _endpoint(self) -> str:
        return f"{self.client.entrypoint}dataset/{self.dataset_id}/attachment/"


class DatasetCollection(LazyCollection[Dataset, DatasetQuery, DatasetQuerySerializer]):
    """
    A generator to retrieve Dataset models in a lazy way.

    DatasetCollection will retrieve models in chunks and yield each model until
    all models for the query have been received.

    Attributes:
        client (DataClient): the client used to request models
        chunk_size (int): the number of models fetched per chunk size
        skip (int): the number of models to skip
        take (int): the number of models to retrieve
        query (dict): additional query parameters. Check the API documentation
            for details:
            https://beta.data.npolar.no/-/docs/dataset/#/dataset/get_dataset_
    """

    model_class = Dataset
    query_serializer = DatasetQuerySerializer()

    @property
    def _endpoint(self) -> str:
        return f"{self.client.entrypoint}dataset/"


class LabelCollection(LazyCollection[Label, LabelQuery, LabelQuerySerializer]):
    """
    A generator to retrieve Label models in a lazy way.

    LabelCollection will retrieve labels in chunks and yield each model until
    all models for the query have been received.

    Attributes:
        client (DataClient): the client used to request models
        chunk_size (int): the number of models fetched per chunk size
        skip (int): the number of models to skip
        take (int): the number of models to retrieve
        query (dict): additional query parameters.
    """

    model_class = Label
    query_serializer = LabelQuerySerializer()

    @property
    def _endpoint(self) -> str:
        return f"{self.client.entrypoint}label/"


class PermissionCollection:
    def __init__(self, raw_permission_list: list[PermissionAPIResponse]) -> None:
        self._generator = iter(raw_permission_list)

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Permission:
        return Permission(next(self._generator))


class PrefixCollection(LazyCollection[Prefix, PrefixQuery, PrefixQuerySerializer]):
    """
    A generator to retrieve Prefixes models in a lazy way.

    PrefixCollection will retrieve models in chunks and yield each model until
    all models for the query have been received.

    Attributes:
        client (DataClient): the client used to request models
        chunk_size (int): the number of models fetched per chunk size
        skip (int): the number of models to skip
        take (int): the number of models to retrieve
        query (dict): additional query parameters. Check the API documentation
            for details:
            https://beta.data.npolar.no/-/docs/dataset/#/prefix/get_dataset__datasetID__prefix_
    """

    model_class = Prefix
    query_serializer = PrefixQuerySerializer()

    def __init__(
        self,
        dataset_id: uuid.UUID,
        *,
        client: DataClient,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        query: PrefixQuery,
    ) -> None:
        super().__init__(client=client, chunk_size=chunk_size, query=query)
        self.dataset_id = dataset_id

    @property
    def _endpoint(self) -> str:
        return f"{self.client.entrypoint}dataset/{self.dataset_id}/prefix/"


class RecordCollection(LazyCollection[Record, RecordQuery, RecordQuerySerializer]):
    """
    A generator to retrieve Record models in a lazy way.

    RecordCollection will retrieve models in chunks and yield each model until
    all models for the query have been received.

    Attributes:
        client (DataClient): the client used to request models
        chunk_size (int): the number of models fetched per chunk size
        skip (int): the number of models to skip
        take (int): the number of models to retrieve
        query (dict): additional query parameters. Check the API documentation
            for details:
            https://beta.data.npolar.no/-/docs/dataset/#/record/get_dataset__datasetID__record_
    """

    model_class = Record
    query_serializer = RecordQuerySerializer()

    def __init__(
        self,
        dataset_id: uuid.UUID,
        *,
        client: DataClient,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        query: RecordQuery,
    ) -> None:
        super().__init__(client=client, chunk_size=chunk_size, query=query)
        self.dataset_id = dataset_id

    @property
    def _endpoint(self) -> str:
        return f"{self.client.entrypoint}dataset/{self.dataset_id}/record/"


# ------------------------------------------------------------------------------
# Attachment DTOs
# ------------------------------------------------------------------------------


class AttachmentCreateDTO:
    """
    A file upload containing a reader to retrieve the content as well as
    metadata.

    Attributes:
        reader (BinaryIO): a reader
        filename (str): the file name
        description (str | None): an optional description
        mime_type (str) the mime type (a.k.a. content type) of the file
        prefix (str | None): an optional prefix. Has to start and end with "/"
        released (datetime | None): when not set, the attachment is never released
        title (str | None): an optional title
    """

    def __init__(
        self,
        reader: BinaryIO,
        filename: str,
        *,
        description: Optional[str] = None,
        mime_type: Optional[str] = None,
        prefix: Optional[str] = None,
        released: Optional[datetime] = None,
        title: Optional[str] = None,
    ) -> None:
        """
        Initialize an AttachmentCreateDTO instance

        Args:
            reader (BinaryIO): reader to fetch the data
            filename (str): the file name
            released (datetime | None): the release date. When None the
                attachment is not released
            description (str | None): an optional description
            mime_type (str | None):
                the mime type (a.k.a. content type) of the file. When None it
                will be set to ""application/octet-stream"
            prefix (str | None): an optional prefix. Has to start and end with "/"
            title (str | None): an optional title

        Raises:
            ValueError: when the released arg does not have timezone UTC
        """

        guard_utc_datetime(released)

        self.reader: BinaryIO = reader
        self.filename: str = filename

        self.description: Optional[str] = description
        self.mime_type: str
        if mime_type is None:
            self.mime_type = "application/octet-stream"
        else:
            self.mime_type = mime_type
        self.prefix: Optional[str] = prefix
        self.released: Optional[datetime] = released
        self.title: Optional[str] = title

    def _get_multiparts(self) -> list[Tuple[Any, ...]]:
        data: list[Tuple[Any, ...]] = []

        if self.description is not None:
            data.append(
                ("description", self.description),
            )
        if self.prefix is not None:
            data.append(
                ("prefix", self.prefix),
            )
        if self.released is not None:
            data.append(
                ("released", self.released.isoformat().replace("+00:00", "Z")),
            )
        if self.title is not None:
            data.append(
                ("title", self.title),
            )

        # blob has to be the last tuple to be added
        data.append(
            ("blob", (self.filename, self.reader, self.mime_type)),
        )

        return data


class AttachmentCreationInfo:
    """
    Information of an uploaded attachment
    """

    def __init__(self, raw: UploadInfoAPIResponse) -> None:
        self.id: uuid.UUID = uuid.UUID(raw["id"])
        self.filename: str = raw["fileName"]
        self.sha256: str = raw["sha256"]


# ------------------------------------------------------------------------------
# Record DTOs
# ------------------------------------------------------------------------------


class RecordCreateDTO:
    """
    A record upload containing data and metadata for a record to add.

    Attributes:
        content (Content): the content of the record,
        type (str): the type of the content
        id (uuid.UUID): an optional UUID
        parent_id (uuid.UUID): an optional parent record id
    """

    def __init__(
        self,
        content: Content,
        type: str,
        id: Optional[uuid.UUID] = None,
        parent_id: Optional[uuid.UUID] = None,
    ) -> None:
        """
        Initialize a RecordCreateDTO instance

        Args:
            content (Content): the content of the record,
            type (str): the type of the content
            id (uuid.UUID): an optional UUID. A id be created when not provided here
            parent_id (uuid.UUID): an optional parent record id
        """

        self.content: Content = content
        self.type: str = type
        if id is None:
            id = uuid.uuid4()
        self.id: uuid.UUID = id
        self.parent_id: Optional[uuid.UUID] = parent_id


class RecordCreateDTOEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, RecordCreateDTO):
            return {
                "content": obj.content,
                "type": obj.type,
                "id": str(obj.id) if obj.id is not None else None,
                "parentId": str(obj.parent_id) if obj.parent_id is not None else None,
            }
        return super().default(obj)  # pragma: no cover


class RecordCreationInfo:
    """
    Information about added records
    """

    def __init__(self, raw: RecordInfoAPIResponse) -> None:
        self.num_processed: int = raw["numProcessed"]
        self.num_created: int = raw["numCreated"]
        self.num_conflict: int = raw["numConflict"]
