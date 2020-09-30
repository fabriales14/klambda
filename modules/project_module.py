import sys, os, datetime
from classes import cli_command
from modules import base_module
from services import logger, db_service, s3_client, cognito_client, file_processor
from config import klambda_config

class ProjectModule(base_module.BaseModule):
    # child class from Module that contains the action for the commands
    # and access the klambda file content 

    def __init__(self, pName, pDescription, pReader):
        super(ProjectModule, self).__init__(db_service.DbService(),pName, pDescription, pReader) # instance the parent class
        self.register_commands() # register all the commands of the module
        self.project = self.reader.data['project']
        self.__s3_client = s3_client.S3Client()
        self.__cognito_client = cognito_client.CognitoClient()
        self.credentials = file_processor.FileProcessor(os.getcwd()+'/user.yml')

    def create_project(self, pParameters):
        '''
        Creates a project in db with klambda file info

        :param list pParameters: a list of optional parameters
        '''
        self.validate_user(self.project) # verify if current user can perfom this action
        if not self.client.check_item("Klambda_projects", {'name': self.project['name'], 'author': self.project['author']}):
            self.project['created_on'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.project['last_update'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.client.put_item("Klambda_projects",self.project)
            logger.info("The project %s created succesfully" % self.project['name'])
            self.upload_files(self.project['files']) # uploads listed files on S3
        else:
            logger.error("The project %s already exists" % self.project['name'])

    def edit_project(self, pParameters):
        '''
        Edits a project in db with klambda file info

        :param list pParameters: a list of optional parameters
        '''
        if self.client.check_item("Klambda_projects", {'name': self.project['name'], 'author': self.project['author']}): 
            item = self.client.get_item("Klambda_projects", {'name': self.project['name'], 'author': self.project['author']})
            self.validate_user(item) # verify if current user can perfom this action
            item['users'] = self.project['users']
            item['description'] = self.project['description']
            item['repo_url'] = self.project['repo_url']
            item['files'] = self.project['files']  
            item['last_update'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.client.put_item("Klambda_projects",item)
            destination_path = self.project['name'] + "-" + self.project['author'] 
            self.__s3_client.delete_object('klambda', destination_path) # deletes the project folder
            self.upload_files(self.project['files']) # uploads listed files on S3
            logger.info("The project %s edited succesfully" % self.project['name'])
        else:
            logger.error("The project %s doesn't exist" % self.project['name'])

    def delete_project(self, pParameters):
        '''
        Deletes a project from db

        :param list pParameters: a list of optional parameters
        '''
        if self.client.check_item("Klambda_projects", {'name': self.project['name'], 'author': self.project['author']}):
            item = self.client.get_item("Klambda_projects", {'name': self.project['name'], 'author': self.project['author']})
            self.validate_user(item) # verify if current user can perfom this action
            self.client.delete_item("Klambda_projects", {'name': self.project['name'], 'author': self.project['author']})
            destination_path = self.project['name'] + "-" + self.project['author']
            self.__s3_client.delete_object('klambda', destination_path)
            logger.info("The project %s deleted succesfully" % self.project['name'])
        else:
            logger.error("The project %s doesn't exist" % self.project['name'])

    def upload_files(self, pFiles):
        '''
        Uploads a list of files to the S3 bucket

        :param list pFiles: a list of file names paths
        '''
        for file_path in pFiles:
            destination_path = self.project['name'] + "-" + self.project['author'] + file_path
            self.__s3_client.upload_object('klambda', './' + file_path, destination_path)

    def download_project(self):
        '''
        Nothing
        '''
        pass

    def validate_user(self, pProject):
        '''
        Validates if current user logged can perform actions on project

        :param dict pProject: information from project
        '''
        if self.credentials.data['USERNAME'] == pProject['author'] or self.credentials.data['USERNAME'] in pProject['users']:
            return 
        else:
            logger.error("Your user %s can't perform actions on this project" % self.credentials.data['USERNAME'])
            exit() 
        for user in pProject['users']:
            if not self.__cognito_client.user_exists(user):
                logger.error("The username %s added in the project doesn't exist" % user)
                exit()

    def register_commands(self):
        '''
        Creates the commands for the module and asings a certain action to it
        '''
        #CONFIG = cli_command.CLICommand(self.config_lambdas, 
        #    "Downloads the functions listed on the klambda file")
        #super(ProjectModule,self).register("config", CONFIG)
        CREATE = cli_command.CLICommand(self.create_project, 
            "creates a project under the specifications in the klambda.yml")
        super(ProjectModule,self).register("create", CREATE)
        EDIT = cli_command.CLICommand(self.edit_project, 
            "edits a project under the specifications in the klambda.yml")
        super(ProjectModule,self).register("edit", EDIT)
        DELETE = cli_command.CLICommand(self.delete_project, 
            "deletes a project under the specifications in the klambda.yml")
        super(ProjectModule,self).register("delete", DELETE)


