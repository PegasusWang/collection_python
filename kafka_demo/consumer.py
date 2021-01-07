# -*- coding:utf-8 -*-

"""
pip3 install kafka-python
"""

import time
import json


from kafka import KafkaConsumer


def main():

    consumer = KafkaConsumer(
        "topic_name",
        bootstrap_servers=["127.0.0.1:9092"],
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
    )

    for message in consumer:
        print(
            "%s:%d:%d: key=%s value=%s"
            % (
                message.topic,
                message.partition,
                message.offset,
                message.key,
                message.value,
            )
        )
        time.sleep(3)


if __name__ == "__main__":
    main()
