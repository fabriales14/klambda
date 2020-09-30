import boto3, os, botocore, shutil
from services import logger
from config import klambda_config
from constants import clients, resources

class S3Client():

    __client = boto3.client(clients.Clients.S3,
                        region_name=klambda_config.KlambdaConfig.REGION,
                        aws_access_key_id=klambda_config.KlambdaConfig.AWS_USER_PUBLIC_KEY, 
                        aws_secret_access_key=klambda_config.KlambdaConfig.AWS_USER_SECRET_KEY)
    __resource = boto3.resource(resources.Resources.S3,
                        region_name=klambda_config.KlambdaConfig.REGION,
                        aws_access_key_id=klambda_config.KlambdaConfig.AWS_USER_PUBLIC_KEY, 
                        aws_secret_access_key=klambda_config.KlambdaConfig.AWS_USER_SECRET_KEY)

    def upload_object(self, pBucketName, pObjectPath, pDestPath):
        '''
        Uploads an object to S3 bucket

        :param str pBucketName: name of the bucket
        :param str pObjectPath: path of file to upload
        :param str pDestPath: path to upload file
        :raises Botocore Client Exception
        '''
        try:
            klambda_bucket = self.__resource.Bucket(pBucketName)
            klambda_bucket.upload_file(pObjectPath, pDestPath)
            logger.info("Object %s successfully uploaded to %s" % (klambda_bucket,pDestPath))
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()

    def object_exists(self, pBucketName, pObjectPath):
        try:
            self.__client.head_object(Bucket=pBucketName, Key=pObjectPath)
            return True
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()

    def delete_object(self, pBucketName, pObjectPath):
        '''
        Deletes an object from S3 bucket

        :param str pBucketName: name of the bucket
        :param str pObjectPath: path of file in S3
        :raises Botocore Client Exception
        '''
        try:
            klambda_bucket = self.__resource.Bucket(pBucketName)
            klambda_bucket.objects.filter(Prefix=pObjectPath).delete()
            logger.info("Object %s deleted succesfully from %s" % (pObjectPath,klambda_bucket))
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()

    def download_obejct(self, pBucketName, pObjectPath):
        '''
        Downloads an object from S3 bucket

        :param str pBucketName: name of the bucket
        :param str pObjectPath: path of file in S3
        :raises Botocore Client Exception
        '''
        try:
            klambda_bucket = self.__resource.Bucket(pBucketName)
            if os.path.isdir("."+pObjectPath):
                shutil.rmtree("."+pObjectPath)
            os.mkdir("."+pObjectPath)
            for object in klambda_bucket.objects.filter(Prefix=pObjectPath+"/"):
                klambda_bucket.download_file(object.key, object.key)
        except botocore.exceptions.ClientError as err:
            logger.error(err)
            exit()
        
    