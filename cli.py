import click
import sys
import sqlite3

# Function to process user input and generate appropriate SQL commands
def process_input(query_type, value=None):
    if query_type == "gender":
        return "SELECT DISTINCT sex FROM employee;"
    elif query_type == "female-branch":
        return f"SELECT * FROM employee WHERE sex = 'F' AND branch_id = {value};"
    elif query_type == "female-birth-salary":
        return f"SELECT * FROM employee WHERE sex = 'F' AND (birth_day > '{value}' OR salary > 80000);"
    else:
        return "Invalid query type."
    

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Dependency to close the database connection after the request is completed
def close_db_connection(conn: sqlite3.Connection):
    conn.close()

# Fetch employee names from the database
def execute_query(query):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        employee_names = cursor.fetchall()
        conn.close()
        return employee_names
    except Exception as e:
        return {"error": str(e)}

def print_data(obj):
    # import pdb
    # pdb.set_trace()
    for i in obj:
        try:
            print(f"Name : {i['first_name'] + ' '+ i['last_name']}")
        except Exception as e:
            print(e)

@click.command()
@click.option('--query-type', type=click.Choice(['gender', 'female-branch', 'female-birth-salary']), help='Type of query: gender, female-branch, female-birth-salary')
@click.option('--value', type=int, help='Optional value for the query (e.g., branch_id, birth year)')
def chatbot(query_type, value=None):
    """Chatbot CLI to execute specific queries on the company database.
    python cli.py --query-type gender
    python cli.py --query-type female-branch --value 2
    python cli.py --query-type female-birth-salary --value 1970
        
    """
    if query_type:
        sql_query = process_input(query_type, value)
        click.echo("Chatbot: Executing query...")
        click.echo("Chatbot: " + sql_query)
        data_obj = execute_query(sql_query)
        print_data(data_obj)

if __name__ == '__main__':
    chatbot()

