import pandas as pd
from ._types_shared import get_new_id as get_new_id
from rich.text import Text as Text
from solas_shared import ui as ui
from sqlmodel import SQLModel
from typing import Dict, Optional

class PerfReport(SQLModel, table=False):
    class Config:
        arbitrary_types_allowed: bool
    id: str
    name: str
    description: Optional[str]
    body: Optional[str]
    timers: Optional[Dict[str, pd.DataFrame]]
    timers_json: Optional[str]
    def show(self) -> None: ...
    def __ipython_display__(self) -> None: ...
