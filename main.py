import DBConnector
import pandas as pd
import streamlit as st

def get_sql_script(fileLocation):
    with open(fileLocation, 'r') as file:
        return file.read()

def run_query(cursor, file_name):
    cursor.execute(get_sql_script(file_name))
    cols = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    return pd.DataFrame.from_records(data, columns=cols)

def main():
    options = ['', 'query1.sql', 'query2.sql', 'query3.sql', 'exit']

    conn = DBConnector.DBConnector(connectionType="MySQL").getConnection()
    cursor = conn.cursor()

    st.title('MyUniversity')
    selected_query = st.selectbox('Select query you would like to display', options)

    if selected_query == 'exit':
        cursor.close()
        conn.close()
        st.success('Connection closed.')
        st.stop()
    elif selected_query:
        file_name = f"sql/{selected_query}"
        df = run_query(cursor, file_name)

        st.subheader("Raw Data")
        st.dataframe(df)

        if not df.empty:
            st.subheader("Pivot Table")

            cols = df.columns.tolist()
            index_col = st.selectbox('Select index column', cols, key='index')
            columns_col = st.selectbox('Select columns column', cols, key='columns')
            values_col = st.selectbox('Select values column', cols, key='values')
            aggfunc = st.selectbox('Select aggregation function', ['sum', 'mean', 'count', 'max', 'min'])

            try:
                pivot_df = pd.pivot_table(
                    df,
                    index=index_col,
                    columns=columns_col,
                    values=values_col,
                    aggfunc=aggfunc
                )
                st.dataframe(pivot_df)
            except Exception as e:
                st.error(f"Pivot failed: {e}")

if __name__ == "__main__":
    main()
