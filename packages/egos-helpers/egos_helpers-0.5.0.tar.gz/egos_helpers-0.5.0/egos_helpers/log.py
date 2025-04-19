#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Global logging configuration """

import logging
import pygelf
from .constants import NAME

def setup_logger(
    name: str,
    level='INFO',
    gelf_host=None,
    gelf_port=None,
    configure_egos=True,
    **kwargs
) -> logging :
    """
    sets up the logger

    :param name: The main name of the logger to initialize
    :param level: The logging level
    :param gelf_host: The fqdn of the GELF host
    :param gelf_port: The port for the GELF host
    :param configure_egos: Set to `False` if you don't want the egos libraries to also log
    """

    if level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
        level = 'INFO'

    logging.basicConfig(handlers=[logging.NullHandler()])
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(get_formatter(level))
    logger.addHandler(handler)

    if gelf_host and gelf_port:
        handler = pygelf.GelfUdpHandler(
            host=gelf_host,
            port=gelf_port,
            debug=True,
            include_extra_fields=True,
            **kwargs
        )
        logger.addHandler(handler)

    if configure_egos:
        # The logging settings for ix-notifiers
        ix_logger = logging.getLogger('ix-notifiers')
        ix_logger.setLevel(level)
        ix_handler = logging.StreamHandler()
        ix_handler.setFormatter(get_formatter(level))
        ix_logger.addHandler(ix_handler)

        # The logging settings for egos-helpers
        egos_logger = logging.getLogger(NAME)
        egos_logger.setLevel(level)
        egos_handler = logging.StreamHandler()
        egos_handler.setFormatter(get_formatter(level))
        egos_logger.addHandler(egos_handler)

    return logger

def get_formatter(level='INFO') -> logging.Formatter:
    """ Creates the formatter for the logs """

    fmt = '%(asctime)s.%(msecs)03d %(levelname)s [%(name)s'

    if level == 'DEBUG':
        fmt += ' %(module)s:%(lineno)d %(funcName)s'

    fmt += '] %(message)s'

    return logging.Formatter(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S')
