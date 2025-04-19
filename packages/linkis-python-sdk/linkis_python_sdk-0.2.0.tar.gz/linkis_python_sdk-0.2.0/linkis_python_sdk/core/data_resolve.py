from typing import List, Dict, Any

import numpy as np
import pandas as pd

from linkis_python_sdk.model.model import ResultSet


def resolve_data(result_sets: List[ResultSet], query_req: Dict[str, Any]) -> (List[Dict[str, Any]], int):
    if len(result_sets) == 1:
        df = result_sets[0].to_pandas()
    else:
        dfs = [rs.to_pandas() for rs in result_sets]
        df = pd.concat(dfs, ignore_index=True)
    df = df[[c["column"] for c in query_req.get("columns", [])]]
    for f in query_req.get("filters", []):
        column = f["column"]
        operator = f["operator"].lower()
        value = f["value"]
        if operator == 'eq':
            df = df[df[column] == value]
        elif operator == 'ne':
            df = df[df[column] != value]
        elif operator == 'gt':
            df = df[df[column] > value]
        elif operator == 'gte':
            df = df[df[column] >= value]
        elif operator == 'lt':
            df = df[df[column] < value]
        elif operator == 'lte':
            df = df[df[column] <= value]
        elif operator == 'in':
            values = [v.strip() for v in value.split(',')]
            df = df[df[column].isin(values)]
        elif operator == 'not_in':
            values = [v.strip() for v in value.split(',')]
            df = df[~df[column].isin(values)]
    if orderbys := query_req.get("orderbys", []):
        sort_columns = [ob["column"] for ob in orderbys]
        ascending = [ob["ascending"] for ob in orderbys]
        df = df.sort_values(by=sort_columns, ascending=ascending)
    total_records = len(df)
    if (page := query_req.get("page", 0)) and (page_size := query_req.get("page_size", 0)):
        start = (page - 1) * page_size
        end = start + page_size
        df = df.iloc[start:end]
    df.replace({np.nan: None}, inplace=True)
    data = df.to_dict(orient="records")
    return data, total_records
