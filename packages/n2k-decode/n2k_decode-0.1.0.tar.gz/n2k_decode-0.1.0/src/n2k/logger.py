import logging
import sys
from pathlib import Path

def setup_logger(name: str = "n2k") -> logging.Logger:
    """
    Configure and return a logger for the n2k module.
    
    Args:
        name: The name of the logger (default: "n2k")
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Set up file handler
    file_handler = logging.FileHandler(log_dir / "n2k.log")
    file_handler.setLevel(logging.DEBUG)
    
    # Set up console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Set formatters
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Set default level
    logger.setLevel(logging.DEBUG)
    
    return logger 