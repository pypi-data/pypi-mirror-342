def database_query(connection, query, number_of_records):
    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    # set public schema
    cursor.execute("SET search_path TO public;")

    cursor.execute(query)
    result = cursor.fetchmany(number_of_records)

    cursor.close()
    return result
