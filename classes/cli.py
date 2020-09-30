import argparse
from modules import lambda_module, base_module, project_module

class CLI():

    modules = {} # will contain all the modules of the different services of AWS

    def __init__(self, pReader):
        self.reader = pReader # file processor instance
        self.load_modules() # loads all the available modules
        self.parser = argparse.ArgumentParser( # creation of parser
            prog='klambda',
            usage='%(prog)s [module||command] [command] [parameters]',
            description="This tool will connect to AWS services, and manage " 
                "the different features through a configuration file",
            epilog="Copyright @Akurey (www.akurey.com)",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=True)
        self.parser.add_argument("--signup", type=str,
                    help='adds a new user indicating username, name, email and password', nargs='*')
        self.subparser = self.parser.add_subparsers(dest='command') # subparser for addind the modules
        self.register_arguments() # will add all the commands for each module

    def load_modules(self): # all the modules will be added here
        '''
        Adds the modules to the module dictionary

        :return: None
        :raises ValueError: if the message_body exceeds 160 characters
        :raises TypeError: if the message_body is not a basestring
        '''
        self.modules['lambda'] = lambda_module.LambdaModule('Lambda', 'creation of lambda functions in Klambda Library', self.reader)
        self.modules['project'] = project_module.ProjectModule('Project', 'creation of Klambda projects', self.reader)

    def register_arguments(self):
        '''
        Adds all the commands listed in the modules, with the name and help related

        :return: None
        '''
        for module in self.modules:
            new_parser = self.subparser.add_parser(module, help=self.modules[module].description)
            for argument in self.modules[module].commands:
                new_parser.add_argument("--" + argument, type=str,
                    help=self.modules[module].commands[argument].help, nargs='*')

    
    
    
    
    

