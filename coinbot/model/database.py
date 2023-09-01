from typing import List

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

db = SqliteDatabase("value_averaging.db")


def create_value_averaging_model(asset_name: str) -> Model:
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


def create_value_averaging_tables(table_names: List[str]) -> bool:
    try:
        models = []
        for table_name in table_names:
            model = create_value_averaging_model(table_name)
            models.append(model)
        db.connect()
        db.create_tables(models)
    except OperationalError as e:
        logging.error(f"Failed to create tables: {e}")
        return False

    return True
