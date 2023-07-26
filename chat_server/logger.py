import logging
import sys

def makeLogger(
    name: str=__name__, 
    logfmt: str="%(asctime)s : %(levelname)s : %(message)s", 
    datefmt: str="%H:%M:%S", 
    level=logging.DEBUG,
    handler_stdout: bool = True
) -> logging.Logger:
    """Provides a logger with the given configuration

    Args:
        name (str, optional): Name of the logger. Defaults to __name__.
        logfmt (str, optional): log format.
                Defaults to "%(asctime)s : %(levelname)s : %(message)s".
        datefmt (str, optional): datetime format. 
                Defaults to "%H:%M:%S".
        level (int, optional): effective level for the logger. 
                Defaults to logging.NOTSET.
        handler_stdout (bool, optional): if logger should log to stdout. 
                Defaults to True.

    Returns:
        logging.Logger: The logger object with the given configuration
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # stdout handler
    if handler_stdout:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
    
        # formatter
        formatter = logging.Formatter(
            logfmt, datefmt=datefmt)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)

    return logger