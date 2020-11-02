import boto3, os, botocore, shutil, datetime, time
from dateutil.tz import gettz
from services import logger
from config import klambda_config
from constants import clients, resources

class CognitoClient():

    pool_user_id = 'us-east-1_qfMPe0dUz'

    __client = boto3.client(clients.Clients.COGNITO,
                        region_name=klambda_config.KlambdaConfig.REGION,
                        aws_access_key_id=klambda_config.KlambdaConfig.AWS_USER_PUBLIC_KEY, 
                        aws_secret_access_key=klambda_config.KlambdaConfig.AWS_USER_SECRET_KEY)

    def sign_up(self, pClientId, pKlambdaUser):
        '''
        Register a user in a user pool, with given attributes

        :param str pClientId: id of user pool app client
        :param object pKlambdaUser: KlambdaUser object
        :raises Botocore Client Exception
        '''
        try:
            self.__client.sign_up(
                ClientId=pClientId,
                Username=pKlambdaUser.username,
                Password=pKlambdaUser.password,
                UserAttributes=[
                    {
                        'Name': 'name',
                        'Value': pKlambdaUser.name
                    },
                    {
                        'Name': 'email',
                        'Value': pKlambdaUser.email
                    },
                    {
                        'Name': 'updated_at',
                        'Value': datetime.datetime(2012,4,1,0,0).strftime('%s') # unix timestamp 
                    }
                ],
            )
            self.confirm_user(pKlambdaUser.username)
            logger.info("User %s successfully registered" % pKlambdaUser.username)
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()

    def confirm_user(self, pUsername):
        '''
        Confirms user sign up to user pool

        :param str pUsername: username
        :raises Botocore Client Exception
        '''
        try:
            self.__client.admin_confirm_sign_up(
                UserPoolId=self.pool_user_id,
                Username=pUsername
            )
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()

    def initiate_auth(self, pClientId, pUsername, pPassword):
        '''
        Initiates the authentication for a certain user

        :param str pClientId: id of user pool app client
        :param str pUsername: username
        :param str pPassword: password for user
        :return: initiation tokens for user
        :rType: dict
        :raises Botocore Client Exception
        '''
        try:
            response = self.__client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': pUsername,
                    'PASSWORD': pPassword
                },
                ClientId=pClientId
            )
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()
        else:
            return response


    def get_user(self, pUsername):
        '''
        Gets the user attribites

        :param str pUsername: username
        :return: user attributes
        :rType: dict
        '''
        try:
            response = self.__client.admin_get_user(
                UserPoolId=self.pool_user_id, # id of user pool
                Username=pUsername
            )
            return response
        except botocore.exceptions.ClientError:
            return {}

    def user_exists(self, pUsername):
        '''
        Register a user in a user pool, with given attributes

        :param str pUsername: username
        :return: bool indicating existance of user  
        :rType: bool
        '''
        try: 
            self.__client.admin_get_user(
                UserPoolId=self.pool_user_id,
                Username=pUsername
            )
        except botocore.exceptions.ClientError:
            return False
        else:
            return True

    def verify_email(self, pAccessToken, pCode):
        '''
        Register a user in a user pool, with given attributes

        :param str pClientId: id of user pool app client
        :param object pKlambdaUser: KlambdaUser object
        :raises Botocore Client Exception
        '''
        try:
            self.__client.verify_user_attribute(
                AccessToken=pAccessToken,
                AttributeName='email',
                Code=pCode
            )
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()
        else:
            logger.info("Your email verified correctly")

    def resend_code(self, pClientId, pUsername):
        '''
        Register a user in a user pool, with given attributes

        :param str pClientId: id of user pool app client
        :param object pKlambdaUser: KlambdaUser object
        :raises Botocore Client Exception
        '''
        try:
            self.__client.resend_confirmation_code(
                ClientId=pClientId,
                Username=pUsername
            )
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()
        else:
            logger.info("Code resent...")
    

