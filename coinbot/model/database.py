from functools import wraps
from typing import List, Optional

from peewee import (
    CharField,
    DateTimeField,
    DecimalField,
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


def close_db_after_use(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        logging.info("Closing the database connection.")
        self.close()
        return result

    return wrapper


class ValueAveragingDatabase:
    def __init__(self, db_name: Optional[str] = None):
        self.db_name = db_name or "value_averaging.sqlite"
        self.db = SqliteDatabase(self.db_name)

    def connect(self) -> bool:
        try:
            return self.db.connect()
        except OperationalError as message:
            logging.exception(message)
            logging.warning(f"Connection already exists: {self.db_name}")
        return False

    def close(self) -> bool:
        return self.db.close()

    def _create_value_averaging_model(self, asset_name: str) -> Model:
        db = self.db

        class ValueAveragingRecord(Model):
            exchange = CharField()
            date = DateTimeField()
            market_price = DecimalField()
            current_target = DecimalField()
            current_value = DecimalField()
            trade_amount = DecimalField()
            total_trade_amount = DecimalField()
            order_size = DecimalField()
            total_order_size = DecimalField()
            interval = IntegerField()

            class Meta:
                database = db
                db_table = f"va_{asset_name.lower()}"

        return ValueAveragingRecord

    @ensure_db_connection
    def get_model(self, table_name: str) -> Model:
        model = self._create_value_averaging_model(table_name)
        if self.db.table_exists(model._meta.table_name):
            logging.info(f"Table {model._meta.table_name} already exists.")
        else:
            try:
                self.db.create_tables([model])
                logging.info(f"Table {model._meta.table_name} created.")
            except OperationalError as message:
                logging.exception(message)
                logging.warning(f"Table existence is ambiguous: {table_name}")
        return model

    @ensure_db_connection
    def get_models(self, table_names: List[str]) -> List[Model]:
        models = []
        new_models = []

        for table_name in table_names:
            model = self._create_value_averaging_model(table_name)
            models.append(model)

        for model in models:
            if self.db.table_exists(model._meta.table_name):
                new_models.append(model)
        try:
            if new_models:
                self.db.create_tables(new_models)
                logging.info(f"Tables for {new_models} created.")
        except OperationalError as message:
            logging.exception(message)
            logging.warning(f"Tables existence is ambiguous: {table_names}")

        return models
