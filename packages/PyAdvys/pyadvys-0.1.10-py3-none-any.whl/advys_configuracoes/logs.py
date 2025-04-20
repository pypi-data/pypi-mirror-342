import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def configurar_logging(
    arquivo_log,
    max_bytes=5 * 1024 * 1024,  # 5MB
    backup_count=3,
    habilitar_log_console=False,
):
    caminho = Path(arquivo_log)
    caminho.parent.mkdir(exist_ok=True, parents=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Formato do log
    formato = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )

    # Handler para arquivo com rotação
    file_handler = RotatingFileHandler(
        arquivo_log, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setFormatter(formato)

    # Handler opcional para console
    console = None
    if habilitar_log_console:
        console = logging.StreamHandler()
        console.setFormatter(formato)


    # Adiciona os handlers caso não existam
    if not logger.handlers:
        logger.addHandler(file_handler)
        if console:
            logger.addHandler(console)