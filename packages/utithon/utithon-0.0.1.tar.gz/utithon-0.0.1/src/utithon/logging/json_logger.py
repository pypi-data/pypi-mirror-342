# -*- coding: utf-8 -*-
"""
(c) Charlie Collier, all rights reserved
"""

import logging

import json_log_formatter


class JsonLogger:
    """
    JSON Logger Class
    """
    def __init__(
        self,
        logger_name: str,
        logging_level: int | None = logging.INFO
    ) -> None:
        """
        :param logger_name: the name of the logger
        :param logging_level: the logging level, see [here](https://docs.python.org/3/library/logging.html#logging-levels)
        """
        self._logger_name = logger_name
        self._logging_level = logging_level

        logger_instance = logging.getLogger(logger_name)
        logger_instance.handlers.clear()
        logger_instance.setLevel(logging_level)

        # Set the JSON log formatter as the stream handler for the logger
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(json_log_formatter.JSONFormatter())
        logger_instance.addHandler(stream_handler)

        self._logger_instance = logger_instance

    def info(
        self,
        message: str
    ) -> None:
        self._logger_instance.info(message)
