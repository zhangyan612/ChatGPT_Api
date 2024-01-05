import configparser
import os


def init_config():
    config = configparser.ConfigParser()
    config.read('.env')

    # Project directory
    # os.environ['PRJ_DIR'] = config.get('prj', 'dir')
    # if not os.environ['PRJ_DIR']:
    #     raise ValueError('No project directory set')

    # openai env variable
    os.environ['OPENAI_BASE_URL'] = config.get('openai', 'base_url')
    os.environ['OPENAI_API_KEY'] = config.get('openai', 'api_key')

    # set variable into system on windows 
    os.system("SETX {0} {1}".format('OPENAI_BASE_URL',os.environ['OPENAI_BASE_URL']))
    os.system("SETX {0} {1}".format('OPENAI_API_KEY',os.environ['OPENAI_API_KEY']))



init_config()