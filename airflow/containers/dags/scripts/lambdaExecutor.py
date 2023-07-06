#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import boto3
from lambdaExecutorUT import ArgParser
from lambdaExecutorBL import LambdaExecutorBL






class LambdaExecutor:
    def __init__(self, vArgs):
        self.__vBusinessLayer = LambdaExecutorBL(vArgs)
        self.__vName = self.__class__.__name__


    def fn_execute(self):
        self.__vBusinessLayer.launch_functions()

if __name__ == '__main__':
    vArgs = ArgParser.fn_get_args()
    vExecutor = LambdaExecutor(vArgs)
    try:
        vExecutor.fn_execute()
    except Exception as ex:
        sys.exit(1)
        raise