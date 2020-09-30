import argparse, datetime, os, sys
from classes import cli, event, klambda_user
from services import logger, event_logger, file_processor, cognito_client
from config import klambda_config
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

def main():
    logger.config_logs(ROOT_DIR)
    processor = file_processor.FileProcessor(os.getcwd()+'/klambda.yml') # instance for opening klambda.yml
    credentials = file_processor.FileProcessor(os.getcwd()+'/user.yml')
    cli_tool = cli.CLI(processor) # instance of CLI Tool
    client = cognito_client.CognitoClient()
    args = cli_tool.parser.parse_args() # reads the arguments written by the user
    if args.signup:
        if len(args.signup) == 4:
            user = klambda_user.KlambdaUser(args.signup[0], args.signup[1], args.signup[2], args.signup[3])
            client.sign_up(klambda_config.KlambdaConfig.COGNITO_APP_CLIENT, user)
        exit()
    elif args.command:
        client.initiate_auth(klambda_config.KlambdaConfig.COGNITO_APP_CLIENT, 
                        credentials.data['USERNAME'], 
                        str(credentials.data['PASSWORD'])) # authenticate user
        module = cli_tool.modules[args.command] # gets the module specified by the user
        for com in module.commands: 
            if vars(args)[com] != None: # checks if command has parameters and starts execution
                module.execute(com, vars(args)[com])
                event_body = event.Event(
                    processor.data['project']['name'],
                    processor.data['project']['author'],
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                    credentials.data['USERNAME'],
                    com,
                    module.name)
                event_logger.save_event(event_body)
    else:
        logger.warning("No module nor command typed, please try again...")
        sys.exit()

if __name__ == '__main__':
    main()
    

    
