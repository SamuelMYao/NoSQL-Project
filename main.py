# import configparser, os, sys, pandas as pd
# from sqlalchemy.orm import sessionmaker
# import sqlalchemy
# # from model.models import Demographics, Waveforms, Leads, Base
# import cx_Oracle, pyodbc
import DBConnector, pandas as pd
import streamlit as st


def get_sql_script(fileLocation):
    with open(fileLocation, 'r') as file:
        return file.read()

def run_query(cursor, file_name):
    cursor.execute(get_sql_script(file_name))
    cols = [column[0] for column in cursor.description]  # Extract column names
    data = cursor.fetchall()
    return pd.DataFrame.from_records(data, columns=cols)

def main():
    # Your main logic here
    options = ['','query1.sql', 'query2.sql', 'query3.sql', 'exit']

    conn = DBConnector.DBConnector(connectionType="MySQL").getConnection()
    cursor = conn.cursor()

    st.title('CS315 Project Example')
    selected_query = st.selectbox('select query you would like to display', options)

    if selected_query =='exit':
        cursor.close()
        conn.close()
        st.success('Connection closed.')
        st.stop()
    elif selected_query:
        file_name = f"sql/{selected_query}"
        df = run_query(cursor, file_name)
        df.pivot
        st.dataframe(df)

# Ensures main() runs only when this script is executed directly, not when imported
if __name__ == "__main__":
    main()