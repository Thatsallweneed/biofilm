from sshtunnel import SSHTunnelForwarder
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_ssh_tunnel():
    try:
        server = SSHTunnelForwarder(
            ('braid01.ncgr.org', 42935),
            ssh_username='achalumuru',
            ssh_password='your_ssh_password',
            remote_bind_address=('127.0.0.1', 3306),
            local_bind_address=('127.0.0.1', 33306)
        )
        server.start()
        logger.info("SSH tunnel established successfully on local port %s.", server.local_bind_port)
        input("SSH tunnel is active. Press Enter to close it...")
        server.stop()
    except Exception as e:
        logger.error("Failed to create SSH tunnel: %s", e)

if __name__ == '__main__':
    create_ssh_tunnel()
