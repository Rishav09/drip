from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='services/technical_indicators/settings.env', env_file_encoding='utf-8'
    )

    kafka_broker_address: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str
    candle_seconds: int
    max_candles_in_state: int = 10
    # live_or_historical: Literal['live', 'historical'] = 'live'
    # last_n_days: int = 30


config = Settings()
print(config.model_dump())
