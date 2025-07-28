import logging

def setup_logger(name:str, level:int = logging.INFO):
    """Initialize a logger automatically. For name arg,
    pass in __name__ to get the current file name.

    Args:
        name (str): Current file name -> should pass __name__
        level (int, optional): Level to set Logger object. Defaults to logging.INFO.

    Returns:
        _type_: Returns a logger object. Should assign to a variable that you can call
        for log messages
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        logging.basicConfig(format = "%(asctime)s - %(levelname)s - %(message)s")
    
    return logger