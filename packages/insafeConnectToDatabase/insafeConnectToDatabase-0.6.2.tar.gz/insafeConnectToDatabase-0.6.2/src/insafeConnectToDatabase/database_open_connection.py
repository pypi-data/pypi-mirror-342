import platform

import psycopg2
import subprocess
import tempfile
import os
import base64

from .util.wait_for_proxy import wait_for_proxy

# Database connection string
CLOUD_SQL_CONNECTION_NAME = "cntxt-product-work-permit:me-central2:work-permit-development"

# Dynamically resolve the path to `cloud-sql-proxy`
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this file
CLOUD_SQL_PROXY_PATH_MAC = os.path.join(SCRIPT_DIR, "cloud-sql-proxy")  # Full path to the script
CLOUD_SQL_PROXY_LINUX_PATH = os.path.join(SCRIPT_DIR, "cloud-sql-proxy-linux")  # Full path to the script

if (platform.system().lower() == "linux"):
    CLOUD_SQL_PROXY_PATH = CLOUD_SQL_PROXY_LINUX_PATH
else:
    CLOUD_SQL_PROXY_PATH = CLOUD_SQL_PROXY_PATH_MAC


def database_open_connection(dbname, user, password):
    gcloud_service_account_key_content = os.getenv("SERVICE_ACCOUNT_KEY")
    if not gcloud_service_account_key_content:
        raise EnvironmentError("The 'SERVICE_ACCOUNT_KEY' environment variable is not set or empty.")

    # decode service account content
    decoded_content = base64.b64decode(gcloud_service_account_key_content)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        SERVICE_ACCOUNT_KEY_PATH = temp_file.name
        temp_file.write(decoded_content)

    try:
        if CLOUD_SQL_CONNECTION_NAME:
            print("Starting Cloud SQL Proxy...")

            # Run the Cloud SQL Proxy as a subprocess
            proxy_process = subprocess.Popen(
                [
                    CLOUD_SQL_PROXY_PATH,
                    CLOUD_SQL_CONNECTION_NAME,
                    "--port=5432",
                    f"--credentials-file={SERVICE_ACCOUNT_KEY_PATH}",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            # Wait for proxy to start
            wait_for_proxy(proxy_process)
        else:
            raise ValueError("CLOUD_SQL_CONNECTION_NAME is not provided")

        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host="localhost",
            port="5432"
        )

        return connection, proxy_process

    except Exception as e:
        print("Error connecting to the database:", e)
