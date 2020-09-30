import logging, os

def setup_logger(pName, pFile, pLevel=logging.INFO):
    '''
    Set ups the logging module 

    :param str pName: name of logger
    :param str pFile: path of the file to write logs
    :param pLevel: level of the logging (INFO, ERROR, DEBUG, WARNING)
    '''
    l = logging.getLogger(pName) # set up the logger name
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s') # format of the logs to write
    fileHandler = logging.FileHandler(pFile, mode='w', encoding=None, delay=False) # output file of lofs, mode append
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(pLevel) # sets level of logger
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

def config_logs(pPath):
    '''
    Configures all loggers for each level

    :param str pPath: path of the root of the project to create logs folder
    '''
    logs_dir = pPath + "/logs"
    setup_logger('error', logs_dir +  "/logs_error.log", logging.ERROR)
    setup_logger('info', logs_dir +  "/logs_info.log", logging.INFO)
    setup_logger('debug', logs_dir + "/logs_debug.log", logging.DEBUG)
    setup_logger('warning', logs_dir + "/logs_warning.log", logging.WARNING)

def info(pMessage):
    '''
    Logs message into INFO level
    :param str pMessage: message to log
    '''
    logger = logging.getLogger('info')
    logger.info(pMessage)

def debug(pMessage):
    '''
    Logs message into DEBUG level
    :param str pMessage: message to log
    '''
    logger = logging.getLogger('debug')
    logger.debug(pMessage)

def warning(pMessage):
    '''
    Logs message into WARNING level
    :param str pMessage: message to log
    '''
    logger = logging.getLogger('warning')
    logger.warning(pMessage)  

def error(pMessage):
    '''
    Logs message into ERROR level
    :param str pMessage: message to log
    '''
    logger = logging.getLogger('error')
    logger.error(pMessage)  

