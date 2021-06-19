import psycopg2
from config import config

def create_tables():
    """ Creating tables in PostgreSQL DB """
    commands = (
        """ 
        CREATE TABLE  stock (
            id SERIAL PRIMARY KEY, 
            symbol TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            exchange TEXT NOT NULL,
            market_cap NUMERIC(24,10) NOT NULL,
            sector TEXT NOT NULL
        )
        """, 
        """ 
        CREATE TABLE price_data (
            id SERIAL PRIMARY KEY,
            stock_id INTEGER NOT NULL,
            date DATE NOT NULL,
            open NUMERIC(10,2) NOT NULL,
            high NUMERIC(10,2) NOT NULL,
            low NUMERIC(10,2) NOT NULL,
            close NUMERIC(10,2) NOT NULL,
            volume INTEGER NOT NULL,
            FOREIGN KEY (stock_id) REFERENCES stock (id)
        )
        """)

    connection = None
    try: 
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        connection.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
     create_tables()