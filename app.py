from flask import Flask,redirect,render_template,url_for,request,session,flash
from werkzeug.security import generate_password_hash,check_password_hash
import MySQLdb 


def db_connect():
    conn = MySQLdb.connect(host='sql12.freesqldatabase.com', user='sql12754839', password='XXXtEDvlUW', database='sql12754839')
    return conn


app = Flask(__name__)
app.secret_key = "MySecretKeyIsHerecAnYOuCopy"

@app.route('/')

def home():
    return render_template('index.html')
@app.route('/signup', methods=['POST', 'GET'])
def getstarted():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            # flash('Please enter your email or password')
            return redirect('/login')
        hashed_password = generate_password_hash(password)
        conn = db_connect()
        cursor = conn.cursor()
        querry = "insert into users(name, email, password)values(%s, %s,%s)" 
        try:
            cursor.execute(querry,(name,email,hashed_password))
            conn.commit()
            # flash("Registered successfully!")
            return redirect('/login')
        except MySQLdb.Error as e:
            # flash(f"Error: {e}")
            conn.rollback()
            
            return redirect(url_for('signup'))
        
        
        
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # print("started")
        email = request.form.get('email')
        password = request.form.get('password')
        # print(email, password)
        if not email or not password:
            return redirect('/login')
        conn = db_connect()
        cursor = conn.cursor()
        try:
            querry = "select * from users where email=%s"
            cursor.execute(querry,(email,))
            user = cursor.fetchone()
            # print(user)
            if user and check_password_hash(user[3], password):
                
                session['username'] = user[2]
                session['name'] = user[1]
                return redirect('/dashboard')
            else:
                # flash('Invalid email or password')
                return redirect('/login')
        except MySQLdb.Error as e:
            # flash(f"Error: {e}")
            print(e)
            return redirect(url_for('login'))
        finally:
            cursor.close()
            conn.close()   
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', s = session['name'])
    return """
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #ffffff, #f4eaff);
            }
            p {
                font-size: 1.5rem;
                color: #333;
                margin-bottom: 1rem;
            }
            a {
                text-decoration: none;
                padding: 0.5rem 1.5rem;
                border-radius: 25px;
                background: linear-gradient(45deg, #ff3589, #ff774a);
                color: white;
                font-weight: bold;
                transition: transform 0.2s ease;
            }
            a:hover {
                transform: scale(1.05);
            }
        </style>
        <p>Please LogIn</p>
        <p>I know there are some smart people who will try to do this but sorry </p>
        <a href='/login'>Login</a>
    """

@app.route('/logout')

def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)