#!/usr/bin/python3
# -*- coding: utf-8 -*-
import boto3
import logging
import pandas as pd
from io import BytesIO
from botocore.exceptions import ClientError
from fastavro import writer, parse_schema, reader
from .TransformationMapping import TransformationMapping
from ..config import (
    DESTINATION_BUCKET,
    SOURCE_BUCKET
)


logger = logging.getLogger('extraction_lambda.extraction.models.ExtractionMapping')

class ExtractionMapping():

    def __init__(self, filename, *args, **kargs):
        self._skip = False
        self._filename = filename
        self._tempDF = self.extract()
        self._transformationTypes = self.define_transformation()
        

    def define_transformation(self):
        if self._skip == False:
            return self._tempDF['on'].unique()
        

    def extract(self):
        logger.info("Beggining extraction of json file")
        try:
            s3 = boto3.resource('s3').Object(SOURCE_BUCKET, self._filename)
            with BytesIO(s3.get()['Body'].read()) as bio:
                data = pd.read_json(bio, lines=True)
            return data
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                logger.info("non existing file: "+self._filename)
                self._skip = True 
            else:
                raise

    def run(self):
        if self._skip == False:
            for transType in self._transformationTypes:
                (TransformationMapping(transType,
                                       filename=self._filename.replace(".json",""),
                                       tempDF=self._tempDF.loc[self._tempDF['on'] == transType])
                                       .transform()
                                       .load())
        return {"finished_correctly": True}
