import logging

def configure_logging():
    logging.basicConfig(
        filename='chat_log.txt',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
    )
