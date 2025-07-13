import logging

def get_logger():
    logger = logging.getLogger("pipeline")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler("logs/pipeline.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(fh)
    return logger 