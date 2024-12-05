import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

def setup_logging():
    # Configure the logging level
    logging.basicConfig(level=logging.INFO)

    # Create a handler for the rotating log file
    handler = RotatingFileHandler(rf'app.log', maxBytes=10000, backupCount=1)
 
    # Define the log format in JSON
    json_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.setFormatter(json_formatter)

    # Add the handler to the root logger
    logging.getLogger().addHandler(handler)

# Configure logging
#setup_logging()