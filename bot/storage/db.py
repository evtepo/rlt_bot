import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from configs.settings import settings


class ABCStorage(ABC):
    @abstractmethod
    async def get(self, collection: str, params: dict):
        """
        Method for obtaining data.
        """
        ...

    @abstractmethod
    async def _prepare_date(self, date: str, format_type: str | None = None):
        """
        A method for converting dates into the correct format.
        """
        ...

    @abstractmethod
    async def generate_dates(
        self, dt_from: datetime, dt_upto: datetime, group_type: str
    ):
        """
        Method for generating dates.
        """
        ...


class MongoDB(ABCStorage):
    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(
            f"mongodb://{settings.mongo_user}:{settings.mongo_password}@{settings.mongo_host}:{settings.mongo_port}/"
        )
        self.database = self.client[settings.mongo_db_name]

    async def get(self, collection: str, params: dict):
        """
        Method for obtaining data.
        """
        collection: AsyncIOMotorCollection = self.database[collection]

        dt_from = await self._prepare_date(params.get("dt_from"))
        dt_upto = await self._prepare_date(params.get("dt_upto"))

        pipeline = [
            {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
            {
                "$group": {
                    "_id": {
                        "$dateTrunc": {"date": "$dt", "unit": params.get("group_type")}
                    },
                    "value_sum": {"$sum": "$value"},
                }
            },
            {"$sort": {"_id": 1}},
        ]

        result = await collection.aggregate(pipeline).to_list(None)
        if not result:
            return "The result is empty."

        dates = await self.generate_dates(dt_from, dt_upto, params.get("group_type"))

        i = 0
        mixed_result = []
        for date in dates:
            if i < len(result) and result[i]["_id"] == date:
                mixed_result.append(result[i])
                i += 1
            else:
                mixed_result.append({"_id": date, "value_sum": 0})

        return json.dumps(
            {
                "dataset": [doc["value_sum"] for doc in mixed_result],
                "labels": [doc["_id"].isoformat() for doc in mixed_result],
            }
        )

    async def _prepare_date(self, date: str, format_type: str | None = None):
        """
        A method for converting dates into the correct format.
        """
        if not format_type:
            format_type = "%Y-%m-%dT%H:%M:%S"

        return datetime.strptime(date, format_type)

    async def generate_dates(self, dt_from: datetime, dt_upto: datetime, group_type: str):
        """
        Method for generating dates.
        """
        step = {
            "month": relativedelta(months=1),
            "week": timedelta(weeks=1),
            "day": timedelta(days=1),
            "hour": timedelta(hours=1),
        }.get(group_type, None)

        if not step:
            raise ValueError("Invalid group_type.")

        dates = []
        current_date = dt_from
        while current_date <= dt_upto:
            dates.append(current_date)
            current_date += step

        return dates


def get_db():
    return MongoDB()
