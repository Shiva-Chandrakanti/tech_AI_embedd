"""
This module will be used to fetch the pdf and image file from S3 bucket.
"""

import json
import yaml
import pandas as pd
import os
from io import StringIO

class ConfigRead():
    """
    This class will be used to fetch and update the file in S3 bucket.
    """

    def __init__(self):

        
        self.success = "Success"

        
    def config_load(self,file_path,file_name):
        if file_path is None:
            file_path = "."
        else:
            file_path = file_path
        key = os.path.join(file_path,file_name+".yaml")
        if os.path.isfile(key):
            conf_file = open(key)
            conf_key = yaml.safe_load(conf_file)
            return conf_key
        else:
            raise IOError('Config path={} not found'.format(key))
    
    