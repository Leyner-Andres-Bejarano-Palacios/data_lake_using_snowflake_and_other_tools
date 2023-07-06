#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging as _logging
from os import environ as _environ

LOGGING_LEVELS = {
    'TEST': _logging.DEBUG,
    'DEV':  _logging.INFO,
    'STG':  _logging.INFO,
    'PRD':  _logging.INFO
}
ENV = _environ['ENV']
SOURCE_BUCKET = _environ['SOURCE_BUCKET']
DESTINATION_BUCKET = _environ['DESTINATION_BUCKET']
LOGGING_LEVEL = LOGGING_LEVELS.get(ENV)