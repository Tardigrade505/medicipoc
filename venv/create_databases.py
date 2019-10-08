import pymysql
import logging
import sys
import os
import constants
from table_setup import TableSetup
import json_response as json_response

# rds settings
rds_host = os.environ['ENDPOINT']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']


def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """
    conn = pymysql.connect(rds_host, user=username, passwd=password, connect_timeout=5)
    try:
        with conn.cursor() as cur:
            cur.execute("CREATE DATABASE IF NOT EXISTS " + constants.db_name)
            conn.commit()
            TableSetup.logger.info("SUCCESS: Created new DB " + constants.db_name)
    except pymysql.MySQLError as e:
        TableSetup.logger.error(e)
        return json_response.JsonResponse(500, "Failed to create database with error: " + str(e)).to_json()
    finally:
        conn.close()

    return TableSetup.setup_tables(rds_host, username, password, constants.db_name)
