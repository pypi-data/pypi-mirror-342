import logging
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

import pandas as pd


@dataclass
class Column:
    name: str
    type: str
    comment: Optional[str] = None


class ResultSet:
    def __init__(
            self,
            metadata: List[Dict[str, str]],
            data: List[List[Any]],
            total_page: int = 0,
            total_line: int = 0,
            page: int = 1,
            type_id: str = "2"
    ):
        self.columns = [
            Column(
                name=col.get('columnName', ''),
                type=col.get('dataType', 'string'),
                comment=col.get('comment')
            ) for col in metadata
        ]
        self.data = data
        self.total_page = total_page
        self.total_line = total_line
        self.page = page
        self.type_id = type_id

    @classmethod
    def from_response(cls, response_data: Dict[str, Any]) -> 'ResultSet':
        return cls(
            metadata=response_data.get('metadata', []),
            data=response_data.get('fileContent', []),
            total_page=response_data.get('totalPage', 0),
            total_line=response_data.get('totalLine', 0),
            page=response_data.get('page', 1),
            type_id=response_data.get('type', '2')
        )

    def to_pandas(self) -> pd.DataFrame:
        column_names = [col.name for col in self.columns]
        if not self.data:
            return pd.DataFrame(columns=column_names)
        df = pd.DataFrame(self.data, columns=column_names)
        for col in self.columns:
            if col.name in df.columns:
                try:
                    if col.type.lower() in ('tinyint', 'smallint', 'int', 'integer', 'bigint', 'long'):
                        df[col.name] = pd.to_numeric(df[col.name], errors='coerce').astype('Int64')
                    elif col.type.lower() in ('float', 'double', 'decimal', 'numeric'):
                        df[col.name] = pd.to_numeric(df[col.name], errors='coerce')
                    elif col.type.lower() in ('boolean', 'bool'):
                        df[col.name] = df[col.name].map({'true': True, 'false': False, '1': True, '0': False})
                    elif col.type.lower() in ('timestamp', 'datetime'):
                        df[col.name] = pd.to_datetime(df[col.name], errors='coerce')
                    elif col.type.lower() == 'date':
                        df[col.name] = pd.to_datetime(df[col.name], errors='coerce').dt.date
                except Exception as e:
                    logging.warning(e)
        return df
