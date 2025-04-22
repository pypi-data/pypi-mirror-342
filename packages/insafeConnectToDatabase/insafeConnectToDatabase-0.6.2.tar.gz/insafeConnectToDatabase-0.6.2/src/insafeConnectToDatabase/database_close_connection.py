def database_close_connection(connection, proxyConnection):
    connection.close()

    proxyConnection.terminate()
    proxyConnection.wait()
    print("DB Connection & Proxy Connection disabled")
