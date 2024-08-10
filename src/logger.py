import logging
import os

from datetime import datetime

LOG_FILE=f'{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log'    #function to fetch date and time of exception occured
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)  #getcwd= get current working directory
os.makedirs(logs_path,exist_ok=True)  #no issue if some directory already exists, just rewrite it

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # asctime is ascending time
    level=logging.INFO,
) 

