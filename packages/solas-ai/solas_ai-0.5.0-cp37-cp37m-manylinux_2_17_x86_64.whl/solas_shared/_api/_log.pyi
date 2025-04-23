from ._api_shared import get_db as get_db
from datetime import datetime as datetime, timedelta as timedelta
from fastapi import File as File, HTTPException as HTTPException, UploadFile as UploadFile
from solas_shared import app_api as app_api
from solas_shared.types import Log as Log, LogEntry as LogEntry
from sqlalchemy.orm import Session as Session
from typing import List, Optional

async def get_log(solas_id: Optional[str] = ..., max_records: Optional[int] = ..., for_display: Optional[bool] = ..., session: Session = ...) -> List[LogEntry]: ...
