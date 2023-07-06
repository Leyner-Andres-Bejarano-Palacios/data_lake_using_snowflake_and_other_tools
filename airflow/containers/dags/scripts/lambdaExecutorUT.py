#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import argparse


class ArgParser:
    MODULE_DESCRIPTION = "V1.0 This is a module for calling the AWS SQS  \
         that triggers the AWS lambda function"
    MODULE_EPILOG = "Created by Leyner Bejarano"
    EXECUTION_DATE = "Date taken from the airflow execution date, not the date when it was executed"
    EXECUTION_HOUR = "Hour taken from the airflow execution date, not the date when it was executed"
    QUEUE_URL = "Url of the aws sqs service"
    AWS_ACCESS_KEY = "AWS access key"
    AWS_SECRET_KEY = "AWS secret key"
    @classmethod
    def fn_get_args(cls):
        parser = argparse.ArgumentParser(description = cls.MODULE_DESCRIPTION, \
            epilog = cls.MODULE_EPILOG)
        parser.add_argument('--execution-date', '-dt', help = cls.EXECUTION_DATE, \
            type = str, dest = 'vExecutionDate', required = True)
        parser.add_argument('--execution-hour', '-dh', help = cls.EXECUTION_HOUR, \
            type = str, dest = 'vExecutionHour', required = True)
        parser.add_argument('--queue-url', '-q', help = cls.QUEUE_URL, \
            type = str, dest = 'vQueueUrl', required = True)
        parser.add_argument('--access-key', '-ak', help = cls.AWS_ACCESS_KEY, \
            type = str, dest = 'vAccessKey', required = True)   
        parser.add_argument('--secret-key', '-sk', help = cls.AWS_SECRET_KEY, \
            type = str, dest = 'vSecretKey', required = True)                        
        arguments = parser.parse_args()
        return arguments