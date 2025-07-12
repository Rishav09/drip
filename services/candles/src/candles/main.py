from datetime import timedelta

from loguru import logger
from quixstreams import Application


def init_candle(trade: dict) -> dict:
    """
    Initializes a candle with the first trade.

    Args:
        trades (dict): A dictionary representing a trade.

    Returns:
        dict: A dictionary representing the initialized candle.
    """
    return {
        'open': trade['price'],
        'high': trade['price'],
        'low': trade['price'],
        'close': trade['price'],
        'volume': trade['quantity'],
        # 'timestamp_ms': trade['timestamp_ms'],
        'pair': trade['product_id'],
    }


def update_candle(candle: dict, trade: dict) -> dict:
    """
    Updates a candle with a new trade.

    Args:
        candle (dict): A dictionary representing the current candle.
        trade (dict): A dictionary representing a new trade.

    Returns:
        dict: A dictionary representing the updated candle.
    """
    if candle['open'] is None:
        candle['open'] = trade['price']
        candle['pair'] = trade['product_id']
    candle['high'] = max(candle['high'], trade['price'])
    candle['low'] = min(candle['low'], trade['price'])
    candle['close'] = trade['price']
    candle['volume'] += trade['quantity']
    return candle


def run(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    kafka_consumer_group: str,
    candle_seconds: int,
):
    """
    Transforms a stream of input trades into a stream of output candles.

    In 3 steps:
    - Ingests trades from the `kafka_input_topic`
    - Aggregates trades into candles
    - Produces candles to the `kafka_output_topic`

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

    trades_topic = app.topic(name=kafka_input_topic, value_deserializer='json')
    candles_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # Step 1. Ingest trades from the input Kafka topic
    sdf = app.dataframe(topic=trades_topic)
    sdf = sdf.update(lambda trade: logger.debug(f'RAW TRADE ➜ {trade}'))

    # Log input messages
    sdf = sdf.update(lambda message: logger.info(f'Input: {message}'))

    # Step 2. [Placeholder for candle logic using candle_seconds if needed]
    sdf = (
        # Define a tumbling window of 10 minutes
        sdf.tumbling_window(timedelta(seconds=candle_seconds))
        # Create a "reduce" aggregation with "reducer" and "initializer" functions
        .reduce(reducer=update_candle, initializer=init_candle)
    )
    sdf = sdf.current()

    # # Extract open, high, low, close, volume, timestamp_ms, pair from the dataframe
    sdf['open'] = sdf['value']['open']
    sdf['high'] = sdf['value']['high']
    sdf['low'] = sdf['value']['low']
    sdf['close'] = sdf['value']['close']
    sdf['volume'] = sdf['value']['volume']
    # sdf['timestamp_ms'] = sdf['value']['timestamp_ms']
    sdf['pair'] = sdf['value']['pair']

    # # Extract window start and end timestamps
    sdf['window_start_ms'] = sdf['start']
    sdf['window_end_ms'] = sdf['end']

    # # keep only the relevant columns
    sdf = sdf[
        [
            'pair',
            # 'timestamp_ms',
            'open',
            'high',
            'low',
            'close',
            'volume',
            'window_start_ms',
            'window_end_ms',
        ]
    ]

    sdf['candle_seconds'] = candle_seconds

    # # logging on the console
    sdf = sdf.update(lambda value: logger.debug(f'Candle: {value}'))

    # ## Step 3. Output to the output topic
    sdf = sdf.to_topic(candles_topic)

    app.run()


if __name__ == '__main__':
    from candles.config import config

    run(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        kafka_consumer_group=config.kafka_consumer_group,
        candle_seconds=config.candle_seconds,
    )
