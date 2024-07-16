import pymysql

# host = 'localhost'
# port = 3306 
# user = 'root'  
# database = 'Biofilm' 




import pymysql

def main():
    # Connection parameters
    host = 'braid01.ncgr.org'
    user = 'root'
    password = 'eDK-pGuCk5nn'  
    database = 'Biofilm'

    try:
        # Establish a connection to the MySQL database
        connection = pymysql.connect(host=host, user=user, password=password, database=database)
        print("Successfully connected to the database.")

        # Create a cursor object
        cursor = connection.cursor()

        # Example query (modify according to your data)
        query = "SELECT * FROM user_info;"  # Adjust the query to your needs

        # Execute the query
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()
        for row in results:
            print(row)

    except pymysql.MySQLError as e:
        print(f"Error connecting to the MySQL Server: {e}")
    finally:
        if connection:
            # Ensure the connection is closed
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    main()


# connection = pymysql.connect(
#     host=host,
#     port=port,
#     user=user,
#     password=password,
#     database=database
# )

# try:
#     with connection.cursor() as cursor:

#         sql = "select * from organisms limit 1;"
#         cursor.execute(sql)
#         result = cursor.fetchone()
#         print( result)
# finally:
#     connection.close()