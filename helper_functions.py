import sqlite3


def drop(cursor, connection, table_name):
    """delete the table if it does already exist"""
    try:
        query = "DROP TABLE %s;" % (table_name)
        cursor.execute(query)
        connection.commit()  
        print("old table (", table_name, ") dropped")
        # by default in pgdb, all executed queries for connection 1 up to here form a transaction
        # we can also explicitly start transaction by executing BEGIN TRANSACTION
    except sqlite3.Error as e:
        print("ROLLBACK: %s table does not exists or other error." % (table_name))
        print("Error message:", e.args[0])
        connection.rollback()
        pass

def init_table(cursor, connection, attributes, table_name):
    """ initializes the table """
    try:
        # Create table sales and add initial tuples
        query = "CREATE TABLE %s%s;" % (table_name, attributes)
        cursor.execute(query)

        # this commits all executed queries forming a transaction up to this point
        connection.commit()

        print('query: ', query, " executed, table created: ", table_name)
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection.rollback()