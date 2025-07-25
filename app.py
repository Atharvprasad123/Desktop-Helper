from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = 'root' 
app.config['MYSQL_DB'] = 'helpdesk'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        problem_description = request.form['problem']
        solution = find_solution(problem_description)
        return render_template('result.html', problem=problem_description, solution=solution)
    return render_template('index.html')

def find_solution(problem_description):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT solution FROM problems WHERE description LIKE %s", [f'%{problem_description}%'])
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else "Problem not found in the database."

if __name__ == '__main__':
    app.run(debug=True)
