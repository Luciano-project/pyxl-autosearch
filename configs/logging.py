import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

def setup_logging():
    # Configura o nível de logging
    logging.basicConfig(level=logging.INFO)

    # Cria um handler para o arquivo de log rotativo
    handler = RotatingFileHandler(rf'app.log', maxBytes=10000, backupCount=1)

    # Define o formato do log em JSON
    json_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    handler.setFormatter(json_formatter)

    # Adiciona o handler ao logger raiz
    logging.getLogger().addHandler(handler)

# Configurar o logging
#setup_logging()