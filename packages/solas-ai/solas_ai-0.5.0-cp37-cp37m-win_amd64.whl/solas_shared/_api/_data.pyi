from ._api_shared import get_db as get_db
from _typeshed import Incomplete
from datetime import datetime
from fastapi import UploadFile as UploadFile
from solas_shared import app_api as app_api
from solas_shared.types import Blob as Blob, BlobResponse as BlobResponse
from sqlalchemy.orm import Session as Session
from typing import List, Optional

SUPPORTED_DATA_TYPE_EXTENSIONS: Incomplete

async def data_upload_supported_types(): ...
def get_data_columns(id: str, session: Session = ...) -> List[str]: ...
def data_upload(file: UploadFile = ..., expires: Optional[datetime] = ..., session: Session = ...): ...
