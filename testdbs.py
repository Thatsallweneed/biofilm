# import mysql.connector
# from sshtunnel import SSHTunnelForwarder
# import os

# def connect_via_ssh_tunnel():
#     """ Connect to MySQL database over SSH and insert data """
#     try:
#         # Setup SSH tunnel
#         with SSHTunnelForwarder(
#             ('braid01.ncgr.org', 42935),  # Remote server IP and SSH port
#             ssh_username='achalumuru',
#             ssh_password=os.getenv('EArxW_@VK4FY'),  # Use environment variable for security
#             remote_bind_address=('127.0.0.1', 3306)  # Localhost and the default MySQL port
#         ) as tunnel:
#             connection = mysql.connector.connect(
#                 user='root',
#                 password=os.getenv('eDK-pGuCk5nn'),  # Use environment variable for security
#                 host='127.0.0.1',  # Connect to the forwarded port on localhost
#                 port=tunnel.local_bind_port,  # Port assigned by sshtunnel
#                 database='Biofilm'
#             )

#             # Connected successfully to MySQL
#             print('Connected to database via SSH tunnel')
#             cursor = connection.cursor()
#             sql_insert_query = """
#             INSERT INTO user_info (firstname, lastname, email, password, created_at, updated_at, has_upload_image_access, isadmin)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             # Data to insert
#             values = ('samee', 'ssss', 'sameeer@example.com', '$2b$10$examplehashedpassword', '2024-07-01 9:30:00', '2024-07-01 9:30:00', 1, 0)
#             cursor.execute(sql_insert_query, values)
#             connection.commit()  # Commit the transaction
#             print('Record inserted successfully.')

#             cursor.close()
#             connection.close()

#     except Exception as e:
#         print('Error:', e)

# if __name__ == '__main__':
#     connect_via_ssh_tunnel()


# sql_pass = "eDK-pGuCk5nn"
# server_pass = "EArxW_@VK4FY"









# # from sshtunnel import SSHTunnelForwarder
# # import logging

# # # Configure logging
# # logging.basicConfig(level=logging.DEBUG)
# # logger = logging.getLogger(__name__)

# # def create_ssh_tunnel():
# #     try:
# #         server = SSHTunnelForwarder(
# #             ('braid01.ncgr.org', 42935),
# #             ssh_username='achalumuru',
# #             ssh_password=server_pass,
# #             remote_bind_address=('127.0.0.1', 3306),
# #             local_bind_address=('127.0.0.1', 33306)
# #         )
# #         server.start()
# #         logger.info("SSH tunnel established successfully on local port %s.", server.local_bind_port)
# #         input("SSH tunnel is active. Press Enter to close it...")
# #         server.stop()
# #     except Exception as e:
# #         logger.error("Failed to create SSH tunnel: %s", e)

# # if __name__ == '__main__':
# #     create_ssh_tunnel()



