from gel import AsyncIOClient

import numpy as np
import pandas as pd


async def convert_excel_data_into_dictionary(
    session: AsyncIOClient,
    file_path: str,
    mapping: dict[str, str] | None,
    sheet_name: str | None,
) -> list[dict]:
    excel_data = (
        pd.read_excel(file_path, sheet_name=sheet_name)
        if sheet_name
        else pd.read_excel(file_path)
    )
    excel_data = excel_data.replace({np.nan: None})
    data = excel_data.to_dict(orient="records")
    if mapping:
        mapped_data = []
        for record in data:
            mapped_record = {}
            for file_col, db_field in mapping.items():
                if file_col in record:
                    mapped_record[db_field] = record[file_col]
            mapped_data.append(mapped_record)
        return mapped_data

    return data
