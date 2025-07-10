from loguru import logger
from quixstreams import Application

from technical_indicators.candle import update_candles_in_state
from technical_indicators.indicators import compute_technical_indicators


def run(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_seconds: int,
):
    """
    Transforms a stream of input candles into a stream of technical indicators.

    In 3 steps:
    - Ingests candles from the `kafka_input_topic`
    - Compute technical indicators
    - Produces technical indicators to the kafka output topic

    Args:
        kafka_broker_address (str): Kafka broker address
        kafka_input_topic (str): Kafka input topic name
        kafka_output_topic (str): Kafka output topic name
        kafka_consumer_group (str): Kafka consumer group name
        candle_seconds (int): Candle duration in seconds
    """

    app = Application(
        broker_address=kafka_broker_address, consumer_group=kafka_consumer_group
    )

    candles_topic = app.topic(name=kafka_input_topic, value_deserializer='json')
    technical_indicators_topic = app.topic(
        name=kafka_output_topic, value_serializer='json'
    )

    # Step 1. Ingest trades from the input Kafka topic, Create a streaming data frame connected to
    # input Kafka topic
    sdf = app.dataframe(topic=candles_topic)

    # Filter the candles b the given candle seconds
    sdf = sdf[sdf['candle_seconds'] == candle_seconds]

    # Step 3 Add candles to the state dictionary
    sdf = sdf.apply(update_candles_in_state, stateful=True)

    # Step 4 Compute technial indicators from the candles in the state dictionary
    sdf = sdf.apply(compute_technical_indicators, stateful=True)

    # Log input messages on the console
    sdf = sdf.update(lambda value: logger.debug(f'Final message: {value}'))

    # ## Step 5. Produce the candles to the output kafka topic
    sdf = sdf.to_topic(technical_indicators_topic)

    app.run()


if __name__ == '__main__':
    from technical_indicators.config import config

    run(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        candle_seconds=config.candle_seconds,
    )
