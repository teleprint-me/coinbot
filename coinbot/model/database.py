from functools import wraps
from typing import List, Optional

from peewee import (
    CharField,
    DateTimeField,
    FloatField,
    IntegerField,
    Model,
    OperationalError,
    SqliteDatabase,
)

from coinbot import logging


def ensure_db_connection(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.db.is_closed():
            logging.warning("Database connection is closed.")
            logging.info("Opening a new connection.")
            self.connect()
        return method(self, *args, **kwargs)

    return wrapper


class ValueAveragingDatabase:
    def __init__(self, db_name: Optional[str] = None):
        self.db_name = db_name or "value_averaging.db"
        self.db = SqliteDatabase(self.db_name)

    def connect(self):
        self.db.connect()

    def close(self):
        self.db.close()

    def _create_value_averaging_model(self, asset_name: str) -> Model:
        db = self.db

        class ValueAveragingRecord(Model):
            exchange = CharField()
            date = DateTimeField()
            market_price = FloatField()
            current_target = FloatField()
            current_value = FloatField()
            trade_amount = FloatField()
            total_trade_amount = FloatField()
            order_size = FloatField()
            total_order_size = FloatField()
            interval = IntegerField()

            class Meta:
                database = db
                db_table = f"va_{asset_name.lower()}"

        return ValueAveragingRecord

    @ensure_db_connection
    def get_model(self, table_name: str) -> Model:
        model = self._create_value_averaging_model(table_name)
        try:
            self.db.create_tables([model])
        except OperationalError as message:
            logging.exception(message)
            logging.warning(f"Table may or may not already exist: {table_name}")
        return model

    @ensure_db_connection
    def get_models(self, table_names: List[str]) -> List[Model]:
        models = []
        for table_name in table_names:
            model = self._create_value_averaging_model(table_name)
            models.append(model)
        try:
            self.db.create_tables(models)
        except OperationalError as message:
            logging.exception(message)
            logging.warning(f"Tables may or may not already exist: {table_names}")
        return models
