import pandas as pd
from ._types_shared import get_new_id as get_new_id
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel
from typing import Any, List, Optional

class BlobDataType(str, Enum):
    ANY: str
    DATAFRAME: str
    SERIES: str

class Blob(SQLModel, table=True):
    id: str
    expires: Optional[datetime]
    data: Optional[Any]
    content_type: Optional[str]
    filename: Optional[str]
    extension: Optional[str]
    def as_dataframe(self) -> pd.DataFrame: ...
    def as_series(self) -> pd.Series: ...

class BlobResponse(SQLModel):
    id: str
    expires: Optional[datetime]
    content_type: Optional[str]
    filename: Optional[str]
    extension: Optional[str]
    uri: Optional[str]
    rows: Optional[int]
    cols: Optional[int]
    column_names: Optional[List[str]]
