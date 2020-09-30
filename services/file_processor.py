import json, os, time, sys, yaml
from services import logger

class FileProcessor():

    def __init__(self, pFile):
        self.file = pFile
        self.data = {}
        self.load_file()

    def load_file(self):
        '''
        Opends the .yml file with the path provided
        '''
        try:
            with open(self.file, 'r') as yaml_file:
                self.data = yaml.safe_load(yaml_file)
        except OSError:
            logger.error("Not a Klambda folder project, please create one")
            sys.exit(1)

    def write_file(self):
        try:
            with open(self.file, 'w') as outfile:
                yaml.dump(self.data, outfile, default_flow_style=False)
        except OSError as err:
            logger.error(err)
            sys.exit(1)

    def validate_schema(self, pSchema):
        '''
        Recieves a defined schema and validates with the opened file
        '''
        pass

    

