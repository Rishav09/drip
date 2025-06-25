# Create an Application instance with Kafka configs
from typing import Optional

from kraken_api import KrakenAPI, Trade
from loguru import logger
from quixstreams import Application


def run(
    kafka_broker_address: str,
    kafka_topic_name: str,
    kraken_api: KrakenAPI,
    kafka_topic_partitions: Optional[int] = 1,
):
    app = Application(broker_address=kafka_broker_address, consumer_group='example')
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            # Define a topic "my_topic" with JSON serialization

            events: list[Trade] = kraken_api.get_trades()

            for event in events:
                # Serialize an event using the defined Topic
                message = topic.serialize(  # key=event.product_id,
                    value=event.to_dict()
                )
                # logger.info(
                #     f'Preparing to produce: key={event.product_id}, value={event.to_dict()}'
                # )
                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name,
                    value=message.value,
                    # key=message.key
                )
                logger.info(f'Produced message to topic{topic.name}')
                logger.info(f'Trade{event.model_dump()} pushed to kafka')


#
if __name__ == '__main__':
    from trades.config import config

    api = KrakenAPI(product_ids=config.product_ids)
    run(
        # kafka_broker_address='localhost:31234',
        # kafka_broker_address='kafka-e11b-kafka-bootstrap.kafka.svc.cluster.local:9092',
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic_name=config.kafka_topic_name,
        # kafka_topic_name='trades',
        kraken_api=api,
    )
