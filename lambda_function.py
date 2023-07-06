#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
from extraction import  ExtractionMapping, config


logging.basicConfig(level=config.LOGGING_LEVEL,
                    format=config.FORMAT,
                    force=True)

logger = logging.getLogger('extraction_lambda')

def handler(event, ctx):
    logger.info(f'Lambda invoked/nEvent: {json.dumps(event).replace("//","")}')
    for record in event.get('Records',[]):
        ExtractionMapping(record['body']).run()
    return {"status_code":200}
