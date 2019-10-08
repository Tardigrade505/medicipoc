import os
import logging
import json
import pymysql
import json_response as json_response
import constants


def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """
    http_method = event.get('httpMethod')
    resource = event.get('resource')
    if http_method == "GET" and "handle" in resource:
        return get_user(event)
    elif http_method == "POST":
        return create_user(event)
    elif http_method == "DELETE":
        return delete_user(event)


def get_user(event):
    user_handle = event.get('pathParameters').get('user_handle')
    return UsersEndpoint().get_user(constants.db_name, user_handle)


def create_user(event):  # TODO: need some kind of validation of the payload
    users_endpoint = UsersEndpoint()
    body = json.loads(event.get('body'))
    return users_endpoint.create_user(constants.db_name,
                                      body.get('handle'),
                                      body.get('username'),
                                      body.get('name'),
                                      body.get('password'),
                                      body.get('email'),
                                      body.get('phone'),
                                      body.get('address'),
                                      body.get('dob'),
                                      body.get('ssn'))


def delete_user(event):
    return None


class UsersEndpoint:
    def __init__(self):
        self.db_host = os.environ['ENDPOINT']
        self.db_username = os.environ['USERNAME']
        self.db_password = os.environ['PASSWORD']
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def create_user(self, db_name, handle, username, name, password, email, phone, address, dob, ssn):
        conn = pymysql.connect(self.db_host, user=self.db_username, passwd=self.db_password, db=db_name,
                               connect_timeout=5)
        try:
            with conn.cursor() as cur:
                sql_command = f'insert into User (Handle, Username, Name, Password, Email, Phone, Address, DOB, SSN) ' \
                              f'values("{handle}",' \
                              f'"{username}",' \
                              f'"{name}",' \
                              f'"{password}",' \
                              f'"{email}",' \
                              f'"{phone}",' \
                              f'"{address}",' \
                              f'"{dob}",' \
                              f'"{ssn}")'
                cur.execute(sql_command)
                conn.commit()
                response = json_response.JsonResponse(201, {}, {"Message": "New user created!"})
                return response.to_json()
        except pymysql.MySQLError as e:
            self.logger.error("ERROR: failed to insert new user into db")
            self.logger.error(e)
            response = json_response.JsonResponse(500, {},
                                                  {"Error": "Failed to create new user with error: " + str(e)})
            return response.to_json()
        finally:
            conn.close()

    def get_user(self, db_name, user_handle):
        conn = pymysql.connect(self.db_host, user=self.db_username, passwd=self.db_password, db=db_name,
                               connect_timeout=5)
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:  # Using a dictionary cursor for the get
                sql_command = f'select * from User where Handle = "{user_handle}"'
                cur.execute(sql_command)
                user_body = cur.fetchall()
                print("User body: " + str(user_body))
                conn.commit()
                return json_response.JsonResponse(200, {}, user_body).to_json()
        except pymysql.MySQLError as e:
            self.logger.error(f"ERROR: failed to get user with handle {user_handle} with error: " + str(e))
            return json_response.JsonResponse(500, {}, {"Error": "Failed to get user with error: " + str(e)}).to_json()


