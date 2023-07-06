#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
from pytest import mark

def test_extraction_mapping_filename():
    from extraction.models.ExtractionMapping import ExtractionMapping
    extractionMapping = ExtractionMapping('2019-06-01-15-17-10-events.json')
    assert extractionMapping._filename == '2019-06-01-15-17-10-events.json'

def test_extraction_mapping_extract():
    from extraction.models.ExtractionMapping import ExtractionMapping
    jsonStr = r'''{"event":"create","on":"operating_period","at":"2019-06-01T18:17:03.087Z","data":{"id":"op_2","start":"2019-06-01T18:17:04.079Z","finish":"2019-06-01T18:22:04.079Z"},"organization_id":"org-id"}'''
    df = pd.read_json(jsonStr, lines=True)
    extractionMapping = ExtractionMapping('2019-06-01-15-17-3-events.json')
    assert df.equals(extractionMapping.extract())

def test_extraction_mapping_define_transformation_operating_period():
    from extraction.models.ExtractionMapping import ExtractionMapping
    extractionMapping = ExtractionMapping('2019-06-01-15-17-10-events.json')
    assert extractionMapping._transformationTypes == ['vehicle']

def test_extraction_mapping_define_transformation_skip():
    from extraction.models.ExtractionMapping import ExtractionMapping
    extractionMapping = ExtractionMapping('non_existing_key.json')
    assert extractionMapping._skip == True

def test_extraction_mapping_define_transformation_skip():
    from extraction.models.ExtractionMapping import ExtractionMapping
    extractionMapping = ExtractionMapping('2019-06-01-15-17-3-events.json')
    assert extractionMapping.run() == {"finished_correctly": True}
