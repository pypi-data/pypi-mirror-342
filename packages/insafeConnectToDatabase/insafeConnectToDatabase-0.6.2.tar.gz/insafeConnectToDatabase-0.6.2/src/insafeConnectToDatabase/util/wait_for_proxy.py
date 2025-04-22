import time
import socket


def wait_for_proxy(proxy_process):
    """Wait until the proxy binds to the specified host and port."""
    print("Waiting for Cloud SQL Proxy to initialize...")
    import time
    time.sleep(5)

    if proxy_process.poll() is not None:  # Check if the process exited prematurely
        stdout, stderr = proxy_process.communicate()
        print("Cloud SQL Proxy failed to start!")
        print("Error output:", stderr.decode())
        print("Standard output:", stdout.decode())
        raise RuntimeError("Failed to launch Cloud SQL Proxy.")

    print("Cloud SQL Proxy started successfully!")
