import pymysql
import logging
import sys
import json_response as json_response


class TableSetup:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    table_names = ["User", "Account", "Budget", "Goal"]

    @staticmethod
    def setup_tables(rds_host, username, db_password, db_name):

        conn = pymysql.connect(rds_host, user=username, passwd=db_password, db=db_name, connect_timeout=5)
        TableSetup.logger.info("SUCCESS: Connection to RDS MySQL database " + db_name + " succeeded")

        try:
            with conn.cursor() as cur:
                cur.execute("create table User ( Handle  varchar(255) NOT NULL,"
                            "Username varchar(255) NOT NULL,"
                            "Name varchar(255) NOT NULL,"
                            "Password varchar(255) NOT NULL,"
                            "Email varchar(255) NOT NULL,"
                            "Phone varchar(255) NOT NULL,"
                            "Address varchar(255) NOT NULL,"
                            "DOB varchar(255) NOT NULL,"
                            "SSN varchar(255) NOT NULL,"
                            "PRIMARY KEY (Handle) )")
                cur.execute("create table Account ( Account_Number varchar(255) NOT NULL,"
                            "Account_Balance DOUBLE NOT NULL,"
                            "Routing_Number varchar(255) NOT NULL,"
                            "Bank_Name varchar(255) NOT NULL,"
                            "Owner_Name varchar(255) NOT NULL,"
                            "User_Handle varchar(255) NOT NULL,"
                            "FOREIGN KEY (User_Handle) references User(Handle) on delete cascade,"
                            "PRIMARY KEY (Account_Number) )")
                cur.execute("create table Budget (  Budget_ID INT NOT NULL,"
                            "Category varchar(255) NOT NULL,"
                            "Budget_Ceiling DOUBLE NOT NULL,"
                            "Budget_Amount DOUBLE NOT NULL,"
                            "Name varchar(255) NOT NULL,"
                            "User_Handle varchar(255) NOT NULL,"
                            "FOREIGN KEY (User_Handle) references User(Handle) on delete cascade,"
                            "PRIMARY KEY (Budget_ID) )")
                cur.execute("create table Goal ( Goal_ID INT NOT NULL,"
                            "Name varchar(255) NOT NULL,"
                            "Goal_Ceiling DOUBLE NOT NULL,"
                            "Goal_Amount DOUBLE NOT NULL,"
                            "User_Handle varchar(255) NOT NULL,"
                            "FOREIGN KEY (User_Handle) references User(Handle) on delete cascade,"
                            "PRIMARY KEY (Goal_ID) )")
                # cur.execute('insert into User (Handle, Username) values("dummyHandle", "dummy111")')
                conn.commit()
                return json_response.JsonResponse(201, {}, {"Message": "Successfully created tables!"}).to_json()
                # item_count = 0
                # cur.execute("select * from User")
                # for row in cur:
                #     item_count += 1
                #     TableSetup.logger.info(row)
                #     # print(row)
                # conn.commit()
        except pymysql.MySQLError as e:
            TableSetup.logger.error("ERROR: Unexpected error when performing db actions")
            TableSetup.logger.error(e)
            return json_response.JsonResponse(500, {},
                                              {"Error": "Failed to setup tables with error: " + str(e)}).to_json()
        finally:
            conn.close()

