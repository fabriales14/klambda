import boto3, botocore
from constants import resources
from services import logger
from config import klambda_config

class DbService():

    def __init__(self):
        self.__dynamoDB = boto3.resource( # calls the dynamodb resource
                                resources.Resources.DYNAMO_DB, 
                                region_name=klambda_config.KlambdaConfig.REGION,
                                aws_access_key_id=klambda_config.KlambdaConfig.AWS_USER_PUBLIC_KEY, 
                                aws_secret_access_key=klambda_config.KlambdaConfig.AWS_USER_SECRET_KEY
                                ) 

    def put_item(self, pTableName, pItem):
        '''
        Adds data to a table (idempotent: if item already exists edits existing one)

        :param str pTableName: name of table to add item
        :param dict pItem: dictionary containing the data to add
        :return: None
        :raises Botocore Client Exception
        '''
        try:
            table = self.__dynamoDB.Table(pTableName) # gets the table 
            table.put_item(Item=pItem) # puts item on table
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()

    def delete_item(self, pTableName, pKey):
        '''
        Deletes data from a table

        :param str pTableName: name of table to add item
        :param dict pKey: dictionary containing the partition and/or sort key
        :return: None
        :raises Botocore Client Exception
        '''
        try:
            table = self.__dynamoDB.Table(pTableName) # gets the table 
            table.delete_item(Key=pKey) # delets item with given key
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit() 
        
    def check_item(self, pTableName, pKey):
        '''
        Checks if item exists on table

        :param str pTableName: name of table to add item
        :param dict pKey: dictionary containing the partition and/or sort key
        :return: None
        :raises Botocore Client Exception
        '''
        try:
            table = self.__dynamoDB.Table(pTableName) # gets the table 
            response = table.get_item(Key=pKey) # gets the item with given key
            if 'Item' in response:
                return True # if item exists return True
            return False
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()

    def get_item(self, pTableName, pKey):
        '''
        Looks for item on table

        :param str pTableName: name of table to add item
        :param dict pKey: dictionary containing the partition and/or sort key
        :return: item
        :rType: dict
        :raises Botocore Client Exception
        '''
        try:
            table = self.__dynamoDB.Table(pTableName) # gets the table 
            response = table.get_item(Key=pKey) # gets the item with given key
            if 'Item' in response:
                return response['Item'] # if item exists return dict
            return {} # else return empty dict
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()