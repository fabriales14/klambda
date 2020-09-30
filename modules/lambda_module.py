import sys, os, datetime, json, hashlib
from svn import remote, local
from classes import cli_command
from modules import base_module
from services import logger, db_service, file_processor
from config import klambda_config

class LambdaModule(base_module.BaseModule):
    # child class from BaseModule that contains the actions for the commands and access the klambda file content 

    def __init__(self, pName, pDescription, pReader):
        super(LambdaModule, self).__init__(db_service.DbService(),pName, pDescription, pReader) # instance the parent class
        self.reader = pReader
        self.register_commands() # register all the commands of the module
        self.functions_list = self.reader.data['lambdas'] 
        self.credentials = file_processor.FileProcessor(os.getcwd()+'/user.yml')

    def config_lambdas(self, pParameters):
        '''
        Downloads the folder of lambda function from the repository

        :param list pParameters: a list of function names to download
        '''
        if len(pParameters) == 0: # if not function listed gets all the functions from klambda file
            functions = self.get_lambdas() 
        else:
            functions = pParameters
        for function in self.functions_list:
            function_name = next(iter(function)) # get first key of dict
            if function_name in functions:
                if self.client.check_item("Klambda_functions", {'name': function_name, 'author': function[function_name]['author']}): # check if already exists
                    functon_info = self.client.get_item("Klambda_functions",{'name': function_name, 'author': function[function_name]['author']}) # gets info from db
                    self.download_function(functon_info['repo_url'] + "/trunk" + functon_info['folder_path'], function_name) # downloads the folder from the url
                    self.write_data(functon_info, function_name) # writes the function info into the klambda file with its checksum
                else:
                    logger.error("The function %s does not exist from the author %s" % (function_name, function[function_name]['author']))

    def update_lambdas(self, pParameters):
        '''
        Updates the folder of the lambda function from the repository

        :param list pParameters: a list of function names to download
        '''
        if len(pParameters) == 0: # if not function listed gets all the functions from klambda file
            functions = self.get_lambdas()
        else:
            functions = pParameters
        for function in self.functions_list:
            function_name = next(iter(function)) # get first key of dict
            if function_name in functions:
                if self.client.check_item("Klambda_functions", {'name': function_name, 'author': function[function_name]['author']}):
                    self.update_function(function_name)
                else:
                    logger.error("The function %s does not exist from the author %s" % (function_name, function[function_name]['author']))

    def create_lambdas(self, pParameters):
        '''
        Uploads a function information and creates it on the db from the klambda file

        :param list pParameters: a list of function names to create
        '''
        if len(pParameters) == 0: # if not function listed gets all the functions from klambda file
            functions = self.get_lambdas()
        else:
            functions = pParameters
        for function in self.functions_list:
            function_name = next(iter(function)) # get first key of dict
            if function_name in functions:
                if self.validate_function(function[function_name]):
                    self.validate_user(function[function_name]['author']) # validates the user logged in
                    if not self.client.check_item("Klambda_functions", {'name': function_name, 'author': function[function_name]['author']}):
                        function[function_name]['name'] = function_name 
                        function[function_name]['version'] = str(function[function_name]['version'])
                        function[function_name]['created_on'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        function[function_name]['last_update'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        function[function_name]['checksum'] = hashlib.sha256(json.dumps(function[function_name]).encode('utf-8')).hexdigest()
                        self.client.put_item("Klambda_functions",function[function_name])
                        self.write_data(function[function_name], function_name) # stores checksum on klambda file
                        logger.info("The function %s created succesfully from the author %s" % (function_name, function[function_name]['author']))
                    else:
                        logger.error("The function %s already exists for the author %s" % (function_name, function[function_name]['author']))
                else:
                    logger.error("The function %s information is incomplete" % function_name)

    def edit_lambdas(self, pParameters):
        '''
        Edits a function information on the db from the klambda file

        :param list pParameters: a list of function names to download
        '''
        if len(pParameters) == 0: # if not function listed gets all the functions from klambda file
            functions = self.get_lambdas()
        else:
            functions = pParameters
        for function in self.functions_list:
            function_name = next(iter(function)) # get first key of dict
            if function_name in functions:
                if self.validate_function(function[function_name]):
                    if self.client.check_item("Klambda_functions", {'name': function_name, 'author': function[function_name]['author']}):
                        item = self.client.get_item("Klambda_functions", {'name': function_name, 'author': function[function_name]['author']})
                        self.validate_user(item['author']) # verify if current user can perfom this action
                        item['runtime'] = function[function_name]['runtime'] 
                        item['description'] = function[function_name]['description'] 
                        item['category'] = function[function_name]['category'] 
                        item['version'] = str(function[function_name]['version'])
                        item['repo_url'] = function[function_name]['repo_url'] 
                        item['folder_path'] = function[function_name]['folder_path'] 
                        item['last_update'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        item['checksum'] = hashlib.md5(json.dumps(item).encode('utf-8')).hexdigest()
                        self.client.put_item("Klambda_functions", item)
                        self.write_data(item, function_name) # stores checksum on klambda file
                        logger.info("The function %s edited succesfully under %s runtime" % (function_name, function[function_name]['runtime']))
                    else:
                        logger.error("The function %s does not exist under %s runtime" % (function_name, function[function_name]['runtime']))
                else:
                    logger.error("The function %s information is incomplete" % function_name)

    def delete_lambdas(self, pParameters):
        '''
        Deletes a function from database 

        :param list pParameters: a list of function names to download
        '''
        if len(pParameters) == 0: # if not function listed gets all the functions from klambda file
            functions = self.get_lambdas()
        else:
            functions = pParameters
        for function in self.functions_list:
            function_name = next(iter(function)) # get first key of dict
            if function_name in functions:
                if self.client.check_item("Klambda_functions", {'name': function_name, 'author': function[function_name]['author']}):
                    item = self.client.get_item("Klambda_functions", {'name': function_name, 'author': function[function_name]['author']})
                    self.validate_user(item['author']) # verify if current user can perfom this action
                    self.client.delete_item("Klambda_functions", {'name': function_name, 'author': function[function_name]['author']})
                    logger.info("The function %s deleted succesfully under %s runtime" % (function_name, function[function_name]['runtime']))
                else:
                    logger.error("The function %s does not exist under %s runtime" % (function_name, function[function_name]['runtime']))
    
    def info_lambdas(self, pParameters):
        '''
        Gets and prints the information of a function

        :param list pParameters: a list of function names to download
        '''
        if len(pParameters) == 0: # if not function listed gets all the functions from klambda file
            functions = self.get_lambdas()
        else:
            functions = pParameters
        for function in self.functions_list:
            function_name = next(iter(function)) # get first key of dict
            if function_name in functions:
                if self.client.check_item("Klambda_functions", {'name': function_name, 'author': function[function_name]['author']}):
                    item = self.client.get_item("Klambda_functions",{'name': function_name, 'author': function[function_name]['author']})
                    self.info_function(item)
                else:
                    logger.error("The function %s does not exist under %s runtime" % (function_name, function[function_name]['runtime']))

    def get_lambdas(self):
        '''
        Gets all the lambdas listed on the klambda file

        :return: the lambdas listed on the klambda file
        :rType: list
        :raises Botocore Client Exception
        '''
        functions = []
        for function in self.functions_list:
            functions.append(next(iter(function)))
        return functions

    def download_function(self, pUrl, pFunctionName):
        '''
        Downloads the folder of a function from a repository

        :param str pUrl: the downloads url direction of the repository
        :param str pFunctionName: the function name
        '''
        r = remote.RemoteClient(pUrl)
        if not os.path.isdir('./'+pFunctionName):
            r.checkout('./'+pFunctionName)
            logger.info("The function %s downloaded succesfully" % pFunctionName)
        else:
            logger.error("The function %s is already configured in your project, please update in order to get last changes" % pFunctionName)

    def update_function(self, pFunctionName):
        '''
        Updates the folder of a function from a repository

        ::param str pFunctionName: the function name
        '''
        if os.path.isdir('./'+pFunctionName):
            l = local.LocalClient('./'+pFunctionName)
            l.update('./'+pFunctionName)
            logger.info("The function %s updated succesfully" % pFunctionName)
        else:
            logger.error("The function %s is not configured in your project" % pFunctionName)

    def info_function(self, pFunction):
        '''
        Prints the information of a function

        :param dict pFunction: function attributes
        '''
        r = remote.RemoteClient(pFunction['repo_url'] + "/trunk" + pFunction['folder_path'])
        info = r.info()
        print("\n--- %s ---" % pFunction['name'])
        print("Author: %s\nrepo_ur: %s\nDescription: %s\nRuntime: %s\nLast updated on: %s\n" % 
            (pFunction['author'],pFunction['repo_url'],pFunction['description'],pFunction['runtime'], info['commit_date']))

    def write_data(self, pData, pFunctionName):
        '''
        Writes data into klamnda file

        :param dict pData: new data to write
        :param str pFunctionName: the name of the function to write
        '''
        lambda_list = self.reader.data['lambdas']
        for function in lambda_list:
            function_name = next(iter(function)) # get first key of dict
            if pFunctionName == function_name:
                function[function_name] = pData
                self.reader.write_file()
                break
    
    def validate_function(self, pFunctionBody):
        '''
        Validates if function body contains all data needed

        :param dict pFunctionBody: dict with function information
        '''
        keys = ['name','author','category','description','folder_path','repo_url','runtime','version']
        for key in keys:
            if not key in pFunctionBody: 
                return False
        return True


    def validate_user(self, pUsername):
        '''
        Validates if current user logged can perform actions on function

        :param str pUsername: username
        '''
        if self.credentials.data['USERNAME'] != pUsername:
            logger.error("Wrong username %s for lambda" % pUsername)
            exit()

    def register_commands(self):
        '''
        Creates the commands for the module and asings a certain action to it
        '''
        CONFIG = cli_command.CLICommand(self.config_lambdas, 
            "downloads the functions listed on the klambda file")
        super(LambdaModule,self).register("config", CONFIG)
        UPDATE = cli_command.CLICommand(self.update_lambdas, 
            "updates the functions listed on the klambda file")
        super(LambdaModule,self).register("update", UPDATE)
        CREATE = cli_command.CLICommand(self.create_lambdas, 
            "uploads the configuration of one or more functions listed on the klambda file to DynamoDB for posterior deployments")
        super(LambdaModule,self).register("create", CREATE)
        EDIT = cli_command.CLICommand(self.edit_lambdas, 
            "edits the configuration of one or more functions listed on the klambda file to DynamoDB for posterior deployments")
        super(LambdaModule,self).register("edit", EDIT)
        DELETE = cli_command.CLICommand(self.delete_lambdas, 
            "deletes the configuration of one or more functions listed on the klambda file to DynamoDB for posterior deployments")
        super(LambdaModule,self).register("delete", DELETE)
        INFO = cli_command.CLICommand(self.info_lambdas, 
            "shows the repository information of one or more functions listed on the klambda file")
        super(LambdaModule,self).register("info", INFO)


