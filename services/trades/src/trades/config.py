from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='services/trades/settings.env', env_file_encoding='utf-8'
    )

    product_ids: list[str] = [
        'ETH/USD',
        'BTC/USD',
        'SOL/USD',
        'XRP/USD',
    ]
    kafka_broker_address: str
    kafka_topic_name: str
    # live_or_historical: str = 'live'
    live_or_historical: Literal['live', 'historical'] = 'live'
    last_n_days: int = 30


config = Settings()
print(config.model_dump())
