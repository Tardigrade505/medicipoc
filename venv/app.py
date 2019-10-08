import sys
import logging
import pymysql
import importlib
import os
from table_setup import TableSetup

# moduleName = input('table_setup.py')
# importlib.import_module(moduleName)

# rds settings
rds_host = os.environ['ENDPOINT']
name = os.environ['USERNAME']
password = os.environ['PASSWORD']
# db_name = "mydb4"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """

    TableSetup.setup_tables(rds_host, name, password)  # Set up the tables
