def commit_sql(conn,sql,values):
    cursor = conn.cursor()
    for value in values:
        cursor.execute(sql,value)
    conn.commit()