from collections.abc import Iterable
from typing import TypedDict, Literal, Callable, Any
from warnings import warn
import urllib3
from civipy.exceptions import CiviProgrammingError

CiviValue = dict[str, int | str]
CiviV3Request = CiviValue


class CiviV3ResponseOptional(TypedDict, total=False):
    id: int
    error_message: str
    undefined_fields: list[str]


class CiviV3Response(CiviV3ResponseOptional):
    is_error: Literal[0, 1]
    version: Literal[3]
    count: int
    values: list[CiviValue] | dict[str, CiviValue] | CiviValue


class CiviV4Request(TypedDict, total=False):
    select: list[str]
    join: list[list[str | list[str]]]
    translationMode: Literal["fuzzy", "strict"]
    where: list[list[str | int]]
    values: list[CiviValue]
    orderBy: dict[str, Literal["ASC", "DESC"]]
    limit: int
    offset: int
    language: str
    chain: dict[str, list["str | CiviV4Request"]]
    groupBy: list[str]
    having: list[list[str | int]]
    debug: bool


class CiviV4ResponseOptional(TypedDict, total=False):
    error_code: int
    error_message: str
    debug: dict[str, str | list[str]]


class CiviV4Response(CiviV4ResponseOptional):
    entity: str
    action: str
    version: Literal[4]
    count: int
    countFetched: int
    values: list[CiviValue]


CiviResponse = CiviV3Response | CiviV4Response


class BaseInterface:
    """Interface manages communication with the CiviCRM API

    Call the Interface instance with `action`, `entity`, and `params` values to submit an API request.

    The `search_query` method is a helper function to generate query parameters.
    The `values` method is a helper function to generate parameters for create/update.
    """

    api_version: str = ""

    def __init__(self):
        self.func: Callable[[str, str, CiviValue], CiviResponse] | None = None
        self.http: urllib3.PoolManager | None = None
        self.create_retry: urllib3.util.Retry | None = None

    def _configure_http_connection(self) -> None:
        timeout = urllib3.util.Timeout(connect=10.0, read=30.0)
        # retry on all methods, because many non-create requests are made with POST
        retry = urllib3.util.Retry(total=6, backoff_factor=3, backoff_jitter=2, allowed_methods=None)
        self.http = urllib3.PoolManager(timeout=timeout, retries=retry)
        # a retry object to override on Create POST requests
        self.create_retry = urllib3.util.Retry(
            connect=6, read=0, status=3, other=0, backoff_factor=3, backoff_jitter=2, allowed_methods={"POST"}
        )

    def __call__(self, action: str, entity: str, params: CiviValue) -> CiviResponse:
        warn(
            "interface.__call__ will be removed in v0.1.0, use interface.execute instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.execute(action, entity, params)

    def execute(self, action: str, entity: str, params: CiviValue) -> CiviResponse:
        raise NotImplementedError

    operators = {
        "lte": "<=",
        "gte": ">=",
        "lt": "<",
        "gt": ">",
        "ne": "!=",
        "like": "LIKE",
        "not_like": "NOT LIKE",
        "in": "IN",
        "not_in": "NOT IN",
        "between": "BETWEEN",
        "not_between": "NOT BETWEEN",
        "isnull": "IS NULL",
    }

    @staticmethod
    def _arg_is_iterable(arg) -> bool:
        if isinstance(arg, (str, bytes)):
            return False
        return isinstance(arg, Iterable)

    @classmethod
    def _check_is_iterable(cls, op: str, arg: Any) -> Any:
        if op.rpartition("_")[2] not in ("between", "in"):
            return arg
        if isinstance(arg, (str, bytes)) or not isinstance(arg, Iterable):
            raise CiviProgrammingError(f"Must provide an iterable value for `{op}` operator.")
        return list(arg)

    @staticmethod
    def select(fields: list[str]) -> CiviValue | CiviV4Request:
        raise NotImplementedError

    @staticmethod
    def join(tables: list[tuple[str, str, str]]) -> CiviValue | CiviV4Request:
        raise NotImplementedError

    @staticmethod
    def sort(kwargs: CiviValue) -> CiviValue | CiviV4Request:
        raise NotImplementedError

    @staticmethod
    def limit(value: int, offset: int | None = None) -> CiviValue | CiviV4Request:
        raise NotImplementedError

    @staticmethod
    def where(kwargs: CiviValue) -> CiviValue | CiviV4Request:
        raise NotImplementedError

    @staticmethod
    def values(kwargs: CiviValue) -> CiviValue | CiviV4Request:
        raise NotImplementedError


__all__ = ["BaseInterface", "CiviValue", "CiviV3Response", "CiviV4Request", "CiviV4Response", "CiviResponse"]
