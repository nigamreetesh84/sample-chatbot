import click
import sqlite3
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

# Dependency to create a single database connection
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



@app.get('/chatbot/')
def chatbot(user_message: str):
    response = generate_report(user_message)
    return {"response": response}

@click.command()
@click.option('--query', prompt='Enter your query', \
              help='User query for generating the report')
def cli_chatbot(query):
    response = generate_report(query)
    # print(re)
    click.echo("Response: " + response)

def generate_report(query):
    # Your existing code to parse user message and query the database
    # For simplicity, we'll return a static response here
    print(execute_query(query))
    return "Here is your report: Sales report for Q3 2023."


if __name__ == '__main__':
    import uvicorn
    import sys

    if len(sys.argv) > 1:
        cli_chatbot(sys.argv[1:])
    else:
        uvicorn.run(app, host="127.0.0.1", port=8000)
