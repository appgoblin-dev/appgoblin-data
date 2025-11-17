"""Create SQLAlchemy database connection engine."""

import sqlalchemy
from sqlalchemy.engine import Engine
from sshtunnel import SSHTunnelForwarder

from helper_scripts.config import CONFIG, get_logger

logger = get_logger(__name__)


class PostgresCon:
    """Class for managing the connection to PostgreSQL."""

    def __init__(
        self, db_name: str, db_ip: str, db_port: str, server_name: str
    ) -> None:
        """
        Initialize the PostgreSQL connection.

        Args:
            db_name (str): Name of the database.
            db_ip (str): IP address of the database server.
            db_port (str): Port number of the database server.
        """
        self.db_name = db_name
        self.db_ip = db_ip
        self.db_port = db_port
        self.engine: Engine

        try:
            self.db_pass = CONFIG[server_name]["db_password"]
            self.db_user = CONFIG[server_name]["db_user"]
        except KeyError as error:
            logger.error(f"Loading db_auth for {server_name}, error: {error}")
            raise

    def set_engine(self) -> None:
        """Set up the SQLAlchemy engine."""
        try:
            db_login = f"postgresql+psycopg://{self.db_user}:{self.db_pass}"
            db_uri = f"{db_login}@{self.db_ip}:{self.db_port}/{self.db_name}"
            logger.info(f"Adscrawler connecting to PostgreSQL {self.db_name}")
            self.engine = sqlalchemy.create_engine(
                db_uri,
                connect_args={"connect_timeout": 10, "application_name": "adscrawler"},
            )
        except Exception as error:
            logger.error(
                f"Failed to connect {self.db_name} @ {self.db_ip}, error: {error}",
            )
            raise


def get_db_connection(use_ssh_tunnel: bool = False) -> PostgresCon:
    """
    Get a database connection, optionally using an SSH tunnel.

    Args:
        use_ssh_tunnel (bool): Whether to use an SSH tunnel for the connection.

    Returns:
        PostgresCon: A PostgreSQL connection object.
    """
    server_name = "madrone-write"
    host = CONFIG[server_name]["host"]
    database_name = CONFIG[server_name]["db_name"]

    if use_ssh_tunnel:
        ssh_port = CONFIG[server_name].get("ssh_port", 22)
        server = open_ssh_tunnel(host, server_name, ssh_port)
        server.start()
        db_port = str(server.local_bind_port)
        host = "127.0.0.1"
    else:
        db_port = "5432"

    conn = PostgresCon(database_name, host, db_port, server_name)
    conn.set_engine()
    return conn


def open_ssh_tunnel(
    remote_host: str, server_name: str, ssh_port: int
) -> SSHTunnelForwarder:
    """
    Open an SSH tunnel to the remote server.

    Args:
        remote_host (str): The remote host to connect to.
        server_name (str): The name of the server in the configuration.
        ssh_port (int): The SSH port to use.

    Returns:
        SSHTunnelForwarder: An SSH tunnel object.
    """
    return SSHTunnelForwarder(
        (remote_host, ssh_port),
        ssh_username=CONFIG[server_name]["os_user"],
        remote_bind_address=("127.0.0.1", 5432),
        ssh_pkey=CONFIG[server_name].get("ssh_pkey"),
        ssh_private_key_password=CONFIG[server_name].get("ssh_pkey_password"),
    )
