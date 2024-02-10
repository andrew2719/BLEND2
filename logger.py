import logging

def create_logger(log_file_name):
    # Create a logger object
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set the log file name
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and set the format for log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

server_logger = create_logger('server.log')
fast_api_logger = create_logger('fast_api.log')