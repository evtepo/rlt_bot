import json
import logging

from storage.db import ABCStorage


async def get_data(collection: str, params: dict | str, db: ABCStorage):
    try:
        params = json.loads(params)
    except json.JSONDecodeError as ex:
        logging.info(f"Error -> {type(ex).__name__}: {ex}")
        return """
        Invalid input. The data must be in the format:
        {
        "dt_from":"2021-12-31T20:53:00",
        "dt_upto":"2022-01-01T01:15:00",
        "group_type":"month"
        }
        """

    return await db.get(collection, params)
