from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Connect to the SQLite database
DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Reflect the database schema
metadata.reflect(bind=engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def inspect_database():
    """Display tables and their columns."""
    print("\nDatabase Information:")
    for table_name in metadata.tables:
        print(f"Table: {table_name}")
        table = metadata.tables[table_name]
        for column in table.columns:
            print(f"  - Column: {column.name} ({column.type})")
    print("\n")

def access_table_data(table_name):
    """Access and display records in a table."""
    if table_name not in metadata.tables:
        print(f"Table '{table_name}' does not exist!")
        return

    table = metadata.tables[table_name]
    with engine.connect() as conn:
        result = conn.execute(table.select())
        print(f"Data in '{table_name}':")
        for row in result:
            print(row)

def delete_records(table_name, condition):
    """
    Delete records from a table based on a condition.
    Example condition: table.c.id == 1
    """
    if table_name not in metadata.tables:
        print(f"Table '{table_name}' does not exist!")
        return

    table = metadata.tables[table_name]
    with engine.connect() as conn:
        conn.execute(table.delete().where(condition))
        print(f"Deleted records from '{table_name}' where {condition}.")

if __name__ == "__main__":
    # Step 1: Inspect the database schema
    inspect_database()

    # Step 2: Access data from a table (change "your_table_name" to a real table name)
    table_name = "your_table_name"
    access_table_data(table_name)

    # Step 3: Delete records (update "your_table_name" and condition)
    from sqlalchemy import and_
    delete_condition = and_(metadata.tables[table_name].c.id > 10)  # Example: Delete records where id > 10
    delete_records(table_name, delete_condition)

    # Step 4: Verify changes by re-accessing the data
    access_table_data(table_name)

    # Close the session
    session.close()
