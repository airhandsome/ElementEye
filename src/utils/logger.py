import logging
import os

def setup_logger():
    log_dir = '.html_parser/logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir + '/app.log'),
            logging.StreamHandler()
        ]
    )

def get_logger(name):
    return logging.getLogger(name)
