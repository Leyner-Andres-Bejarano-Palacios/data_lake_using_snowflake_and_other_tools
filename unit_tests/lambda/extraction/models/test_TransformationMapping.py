#!/usr/bin/python3
# -*- coding: utf-8 -*-
import boto3
import pandas as pd
from pytest import mark
from botocore.errorfactory import ClientError

def test_transformation_mapping_vehicle():
    from extraction.models.TransformationMapping import TransformationMapping,Vehicle
    jsonStr = r'''{"event":"create","on":"operating_period","at":"2019-06-01T18:17:03.087Z","data":{"id":"op_2","start":"2019-06-01T18:17:04.079Z","finish":"2019-06-01T18:22:04.079Z"},"organization_id":"org-id"}'''
    df = pd.read_json(jsonStr, lines=True)
    transformationMapping = TransformationMapping('vehicle',
                                                  filename='2019-06-01-15-17-3-events.json',
                                                  tempDF=df)
    assert isinstance(transformationMapping, Vehicle)


def test_transformation_mapping_vehicle_transform():
    from extraction.models.TransformationMapping import TransformationMapping,Vehicle
    jsonStr = r'''{"event":"register","on":"vehicle","at":"2019-06-01T18:17:04.088Z","data":{"id":"3a3eb23a-f22e-4fe9-8c20-f37220a81909"},"organization_id":"org-id"}'''
    df = pd.read_json(jsonStr, lines=True)
    transformationMapping = TransformationMapping('vehicle',
                                                  filename='1_testing_vehicle_2019-06-01-15-17-4-events.json',
                                                  tempDF=df)
    jsonStr = r'''{"event":"register","on":"vehicle","at":"2019-06-01T18:17:04.088Z","organization_id":"org-id","id":"3a3eb23a-f22e-4fe9-8c20-f37220a81909"}'''
    df_transformed = pd.read_json(jsonStr, lines=True)
    assert df_transformed.equals(transformationMapping.transform()._tempDF)

def test_transformation_mapping_vehicle_load():
    from extraction.models.TransformationMapping import TransformationMapping,Vehicle
    from extraction.config import DESTINATION_BUCKET
    jsonStr = r'''{"event":"create","on":"operating_period","at":"2019-06-01T18:17:03.087Z","data":{"id":"op_2","start":"2019-06-01T18:17:04.079Z","finish":"2019-06-01T18:22:04.079Z"},"organization_id":"org-id"}'''
    df = pd.read_json(jsonStr, lines=True)
    transformationMapping = (TransformationMapping('vehicle',
                                                  filename='testing_upload',
                                                  tempDF=df).transform()
                                                            .load())
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket=DESTINATION_BUCKET, Key='testing_upload.avro')
        assert True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            assert False
        elif e.response['Error']['Code'] == 403:
            assert False
        else:
            assert False



def test_transformation_mapping_operating_period():
    from extraction.models.TransformationMapping import TransformationMapping,OperatingPeriod
    jsonStr = r'''{"event":"create","on":"operating_period","at":"2019-06-01T18:17:03.087Z","data":{"id":"op_2","start":"2019-06-01T18:17:04.079Z","finish":"2019-06-01T18:22:04.079Z"},"organization_id":"org-id"}'''
    df = pd.read_json(jsonStr, lines=True)
    transformationMapping = TransformationMapping('operating_period',
                                                  filename='2019-06-01-15-17-3-events.json',
                                                  tempDF=df)
    assert isinstance(transformationMapping, OperatingPeriod)

def test_transformation_mapping_operating_period_transform():
    from extraction.models.TransformationMapping import TransformationMapping
    jsonStr = r'''{"event":"create","on":"operating_period","at":"2019-06-01T18:17:03.087Z","data":{"id":"op_2","start":"2019-06-01T18:17:04.079Z","finish":"2019-06-01T18:22:04.079Z"},"organization_id":"org-id"}'''
    df = pd.read_json(jsonStr, lines=True)
    transformationMapping = TransformationMapping('operating_period',
                                                  filename='1_testing_vehicle_2019-06-01-15-17-4-events',
                                                  tempDF=df)
    jsonStr = r'''{"event":"create","on":"operating_period","at":"2019-06-01T18:17:03.087Z","organization_id":"org-id","id":"op_2","start":"2019-06-01T18:17:04.079Z","finish":"2019-06-01T18:22:04.079Z"}'''
    df_transformed = pd.read_json(jsonStr, lines=True)
    assert df_transformed.equals(transformationMapping.transform()._tempDF)



def test_transformation_mapping_operating_period_load():
    from extraction.models.TransformationMapping import TransformationMapping
    from extraction.config import DESTINATION_BUCKET
    jsonStr = r'''{"event":"create","on":"operating_period","at":"2019-06-01T18:17:03.087Z","data":{"id":"op_2","start":"2019-06-01T18:17:04.079Z","finish":"2019-06-01T18:22:04.079Z"},"organization_id":"org-id"}'''
    df = pd.read_json(jsonStr, lines=True)
    transformationMapping = (TransformationMapping('operating_period',
                                                  filename='testing_upload',
                                                  tempDF=df).transform()
                                                            .load())
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket=DESTINATION_BUCKET, Key='testing_upload.avro')
        assert True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            assert False
        elif e.response['Error']['Code'] == 403:
            assert False
        else:
            assert False