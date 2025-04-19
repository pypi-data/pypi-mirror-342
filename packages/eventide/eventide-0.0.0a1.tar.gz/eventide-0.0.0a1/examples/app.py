import logging

from eventide import Eventide, EventideConfig, MockQueueConfig

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    Eventide(
        config=EventideConfig(
            handler_paths=["./examples"],
            queue=MockQueueConfig(
                buffer_size=20,
                min_messages=1,
                max_messages=10,
            ),
            concurrency=2,
            timeout=1.0,
            retry_for=[Exception],
            retry_limit=3,
        ),
    ).run()
