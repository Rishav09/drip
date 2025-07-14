# Create an Application instance with Kafka configs
from typing import Optional

from loguru import logger
from quixstreams import Application

from trades.kraken_rest_api import KrakenRestAPI
from trades.kraken_websocket_api import KrakenWebsocketAPI
from trades.trade import Trade


def run(
    kafka_broker_address: str,
    kafka_topic_name: str,
    kraken_api: KrakenWebsocketAPI | KrakenRestAPI,
    kafka_topic_partitions: Optional[int] = 1,
):
    app = Application(broker_address=kafka_broker_address, consumer_group='example')
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    # Create a Producer instance
    with app.get_producer() as producer:
        while not kraken_api.is_done():
            # Define a topic "my_topic" with JSON serialization

            events: list[Trade] = kraken_api.get_trades()

            for event in events:
                # Serialize an event using the defined Topic
                message = topic.serialize(key=event.product_id, value=event.to_dict())
                # logger.info(
                #     f'Preparing to produce: key={event.product_id}, value={event.to_dict()}'
                # )
                # Produce a message into the Kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)
                logger.info(f'Produced message to topic{topic.name}')
                logger.info(f'Trade{event.model_dump()} pushed to kafka')


#
if __name__ == '__main__':
    from trades.config import config

    if config.live_or_historical == 'live':
        logger.info('Creating KrakenWebSocketAPI object')
        api = KrakenWebsocketAPI(product_ids=config.product_ids)
    elif config.live_or_historical == 'historical':
        logger.info('Creating KrakenRestAPI object')
        api = KrakenRestAPI(
            product_id=config.product_ids[0],
            last_n_days=config.last_n_days,
        )
    else:
        raise ValueError('Invalid value for live or historical')
    run(
        # kafka_broker_address='localhost:31234',
        # kafka_broker_address='kafka-e11b-kafka-bootstrap.kafka.svc.cluster.local:9092',
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic_name=config.kafka_topic_name,
        # kafka_topic_name='trades',
        kraken_api=api,
    )
