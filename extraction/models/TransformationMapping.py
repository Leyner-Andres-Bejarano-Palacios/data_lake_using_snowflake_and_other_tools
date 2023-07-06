#!/usr/bin/python3
# -*- coding: utf-8 -*-
import boto3
import logging
import pandas as pd
from io import BytesIO
from fastavro import writer, parse_schema, reader
from ..config import (
    DESTINATION_BUCKET,
    SOURCE_BUCKET
)

logger = logging.getLogger('extraction_lambda.extraction.models.TransformationMapping')

class TransformationMapping:


    def __new__(cls, on, *args, **kwargs):
        subclass_map = {subclass.on: subclass for subclass in cls.__subclasses__()}
        subclass = subclass_map[on]
        instance = super(TransformationMapping, subclass).__new__(subclass)
        return instance

    def __init__(self, on, filename=None, tempDF=None, *args, **kwargs):
        super().__init__(on, filename=None, tempDF=None, *args, **kwargs)


    
    def load(self):
        schema = {
            'doc': 'door2door',
            'name': 'door2door',
            'namespace': 'door2door',
            'type': 'record',
            'fields': [
            {'name': 'event', "type": ["null", "string"], "default": None},
            {'name': 'on', "type": ["null", "string"], "default": None},
            {'name': 'at', "type": ["null", "string"], "default": None},
            {'name': 'organization_id', "type": ["null", "string"], "default": None},
            {'name': 'id', "type": ["null", "string"], "default": None},
            {'name': 'lat', "type": ["null", "float"], "default": None},
            {'name': 'lng', "type": ["null", "float"], "default": None},
            {'name': 'start', "type": ["null", "string"], "default": None},
            {'name': 'finish', "type": ["null", "string"], "default": None},
            ]
        }
        parsed_schema = parse_schema(schema)
        records = self._tempDF.to_dict('records')
        fo = BytesIO()
        writer(fo, parsed_schema, records)
        year, month, day, _, _, _, _  = self._keyName.split("-")
        key = "demo/{on}/{year}/{month}/{day}/{keyName}.avro".format(on=self.on,
                                                                year=year,
                                                                month=month,
                                                                day=day,
                                                                keyName=self._keyName)
        s3 = boto3.resource('s3').Object(DESTINATION_BUCKET,key)
        s3.put(Body=fo.getvalue())
        return {"finished_correctly": True}

class Vehicle(TransformationMapping):
    on = 'vehicle'

    def __init__(self, on, filename=None, tempDF=None, *args, **kwargs):
        self._tempDF = tempDF
        self._keyName = filename


    def transform(self):
        self._tempDF = pd.concat([self._tempDF.drop(['data'], axis=1), 
                                  self._tempDF['data'].apply(pd.Series)], 
                                  axis=1)
        if 'location' in self._tempDF:
            self._tempDF = pd.concat([self._tempDF.drop(['location'], axis=1), 
                                    self._tempDF['location'].apply(pd.Series)], 
                                    axis=1)
            self._tempDF = self._tempDF.loc[:, ~self._tempDF.columns.duplicated()]
        return self

class OperatingPeriod(TransformationMapping):
    on = 'operating_period'

    def __init__(self, on, filename=None, tempDF=None, *args, **kwargs):
        self._tempDF = tempDF
        self._keyName = filename

    def transform(self):
        self._tempDF = pd.concat([self._tempDF.drop(['data'], axis=1), 
                                  self._tempDF['data'].apply(pd.Series)], 
                                  axis=1)
        return self

