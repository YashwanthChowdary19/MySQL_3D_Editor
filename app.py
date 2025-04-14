from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)
current_db = None  # This will store the current database

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_db
    output = ''
    error = ''
    if request.method == 'POST':
        query = request.form['query'].strip()
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Yash@9346659926',
                database=current_db if current_db else None
            )
            cursor = conn.cursor()
            if query.lower().startswith('use '):
                current_db = query.split()[1].strip(';')
                output = f"Switched to database `{current_db}`"
            else:
                cursor.execute(query)
                if cursor.description:
                    rows = cursor.fetchall()
                    headers = [i[0] for i in cursor.description]
                    output = {'headers': headers, 'rows': rows}
                else:
                    conn.commit()
                    output = f"Query executed successfully. {cursor.rowcount} rows affected."
            cursor.close()
            conn.close()
        except Exception as e:
            error = str(e)
    return render_template('index.html', output=output, error=error)

if __name__ == '__main__':
    app.run(debug=True)
