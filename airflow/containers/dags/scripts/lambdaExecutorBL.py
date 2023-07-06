#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import threading

class LambdaExecutorBL:
    def __init__(self, vArgs):
        self.__vName = self.__class__.__name__
        self.__vExecutionDate = vArgs.vExecutionDate
        self.__vExecutionHour = vArgs.vExecutionHour
        self.__vQueueUrl = vArgs.vQueueUrl
        self.__sqs = sqs = boto3.client('sqs',
                                        aws_access_key_id=vArgs.vAccessKey,
                                        aws_secret_access_key=vArgs.vSecretKey,
                                        region_name="us-east-2",) 


    def get_filename(self, t_min, t_sec):
        return  '{dt}-{dh}-{t_min}-{t_sec}-events.json'.format(
                  dt=self.__vExecutionDate, 
                  dh=self.__vExecutionHour,
                  t_min=t_min, 
                  t_sec=t_sec)

    def launch_functions(self):
        threads = []
        for t_min in range(60):
            for t_sec in range(60):
                t = threading.Thread(target=self.create_functions, args=( t_min, t_sec ))
                t.start()
                threads.append(t)

        for thread in threads:
            thread.join()

    def create_functions(self, t_min, t_sec):
        file_name = self.get_filename(t_min, t_sec)
        response = self.__sqs.send_message(
            QueueUrl = self.__vQueueUrl,
            MessageBody=file_name,
            MessageAttributes={
            'from': {
                'StringValue': file_name,
                'DataType': 'String'
                }
            }
        )
