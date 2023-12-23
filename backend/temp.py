from flask import Flask, jsonify
from flask_cors import CORS  
from sqlalchemy import create_engine
import pandas as pd


# Configuration de la connexion à la base de données SQLite
#db_url = "sqlite:///C:\\Users\\GIS PLUS\\Desktop\\isned" 
#engine = create_engine(db_url)
# Configuration de la connexion à la base de données MariaDB
db_url = "mysql+mysqlconnector://root:root@localhost:3306/data"
engine = create_engine(db_url)
# Charger les données à partir de la base de données dans un DataFrame pandas
data = pd.read_sql("SELECT * FROM Customers", engine)


app = Flask(__name__)
CORS(app) 


@app.route('/get_pie_data')
def get_pie_data():
    # Compter le nombre de clients pour chaque pays
    country_counts = data['country'].value_counts()

    # Récupérer les noms des pays et le nombre de clients pour chaque pays
    countries = country_counts.index.tolist()
    counts = country_counts.values.tolist()

    # Retourner les données nécessaires sous forme de JSON
    pie_data = {
        'labels': countries,
        'data': counts
    }
    return jsonify(pie_data)

@app.route('/get_bar_data')
def get_bar_data():
    
    age_groups = ['18-25', '26-35', '36-45', '46-55', '56+']
    total_balance = data['balance'].sum()
    account_percentages = []
    
    for group in age_groups:
        if group == '56+':
            lower_age = 56
            balance = data[data['age'] >= lower_age]['balance'].sum()
        else:
            lower_age, upper_age = map(int, group.split('-'))
            balance = data[(data['age'] >= lower_age) & (data['age'] <= upper_age)]['balance'].sum()
        
        percentage = (balance / total_balance) * 100
        account_percentages.append(round(percentage, 2))
    
    bar_data = {
        'labels': age_groups,
        'data': account_percentages
    }
    return jsonify(bar_data)


@app.route('/get_active_customer_data')
def get_active_customer_data():
    # Convertir la colonne 'churn' en un format numérique
    data['churn'] = pd.to_numeric(data['churn'], errors='coerce')
    
    # Filtrer les clients actifs (churn = 0)
    active_customers = data[data['churn'] == 0]
    
    # Calculer le nombre cumulatif de clients actifs par rapport à l'âge
    active_customers['cumulative_count'] = active_customers.groupby('age')['customer_id'].cumcount() + 1
    
    response_data = {
        "ages": active_customers['age'].unique().tolist(),
        "cumulative_counts": active_customers.groupby('age')['cumulative_count'].max().tolist()
    }
    
    return jsonify(response_data)
@app.route('/get_gender_data')
def get_gender_data():
    # Compter le nombre d'hommes et de femmes
    gender_counts = data['gender'].value_counts()

    # Récupérer les genres et le nombre correspondant
    genders = gender_counts.index.tolist()
    counts = gender_counts.values.tolist()

    # Retourner les données nécessaires sous forme de JSON
    gender_data = {
        'labels': genders,
        'data': counts
    }
    return jsonify(gender_data)





@app.route('/get_doughnut_data')
def get_doughnut_data():
    # Compter le nombre de clients actifs (active_member = 1) et inactifs (active_member = 0)
    active_counts = data['active_member'].value_counts()

    # Récupérer les noms des catégories (actifs et inactifs) et le nombre de clients pour chaque catégorie
    categories = active_counts.index.tolist()
    counts = active_counts.values.tolist()

    # Retourner les données nécessaires sous forme de JSON
    doughnut_data = {
        'labels': categories,
        'data': counts
    }
    return jsonify(doughnut_data)


@app.route('/get_bar2_data')
def get_bar2_data():
    active_status_counts = data['active_member'].value_counts()

    labels = active_status_counts.index.tolist()
    counts = active_status_counts.values.tolist()

    status_data = {
        'labels': labels,
        'data': counts
    }
    return jsonify(status_data)


if __name__ == '__main__':
    app.run(debug=True)
    


'''from flask import Flask, jsonify
from flask_cors import CORS
from business_logic import BusinessLogic

app = Flask(__name__)

CORS(app)

business_logic = BusinessLogic()

@app.route('/get_pie_data')
def get_pie_data():
    pie_data = business_logic.get_pie_data()
    return jsonify(pie_data)

@app.route('/get_bar_data')
def get_bar_data():
    bar_data = business_logic.get_bar_data()
    return jsonify(bar_data)


@app.route('/get_doughnut_data')
def get_doughnut_data():
    doughnut_data = business_logic.get_doughnut_data()
    return jsonify(doughnut_data)

@app.route('/get_active_customer_data')
def get_active_customer_data():
    line_data = business_logic.get_active_customer_data()
    return jsonify(line_data)

if __name__ == '__main__':
    app.run(debug=True)
'''
'''from flask import Flask, jsonify, request
from flask_cors import CORS
from business_logic import BusinessLogic

app = Flask(__name__)
CORS(app)

business_logic = BusinessLogic()

@app.route('/get_pie_data', methods=['GET'])
def get_pie_data():
    user_id = request.args.get('user_id')
    pie_data = business_logic.get_pie_data(user_id)
    return jsonify(pie_data)

if __name__ == '__main__':
    app.run(debug=True)'''
'''class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)

# API endpoint to create a database user


@app.route('/create_db_user', methods=['POST'])
def create_db_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        # Replace with your actual database superuser credentials
        superuser_username = 'root'
        superuser_password = 'root'

        # Connect to the database as the superuser
        conn = pymysql.connect(
            user=superuser_username,
            password=superuser_password,
            host='localhost',
            database='data',
            auth_plugin='mysql_native_password'  # Specify the authentication method
        )

        # Create a cursor and execute the CREATE USER command
        cursor = conn.cursor()
        cursor.execute(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'")
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'Database user created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        # Se connecter en tant qu'utilisateur à la base de données
        conn = pymysql.connect(
            user=username,
            password=password,
            host='localhost',
            database='data',
        )

        # Créer un curseur et exécuter une requête pour vérifier la connexion
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        if result:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Connected successfully'}), 200
        else:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/get_customers', methods=['GET'])
def get_customers():
    try:
        # Replace with your database credentials
        db_username = 'aaa'
        db_password = 'aaa123'
        db_host = 'localhost'
        db_name = 'data'

        conn = pymysql.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
        )

        cursor = conn.cursor()

        # Get parameter from the request (example: 'country')
        country_param = request.args.get('country')

        # Construct the SQL query with the provided parameter
        query = f"SELECT * FROM customers WHERE country = '{country_param}'"
        cursor.execute(query)

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convert the result to a list of dictionaries
        customers_data = [{'id': row[0], 'name': row[1], 'country': row[2]} for row in result]

        return jsonify(customers_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


'''


'''@app.route('/create_db_user', methods=['POST'])
def create_db_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        # Créer un hachage sécurisé du mot de passe
        password_hash = generate_password_hash(password).decode('utf-8')

        # Créer un nouvel utilisateur de base de données dans la table "database_user"
        new_db_user = DatabaseUser(username=username, password=password_hash)
        db.session.add(new_db_user)
        db.session.commit()

        return jsonify({'message': 'Database user created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
        
@app.route('/database_access', methods=['POST'])
def database_access():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        # Recherche de l'utilisateur de base de données dans la base de données
        db_user = DatabaseUser.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password, password):
            # Connectez-vous à la base de données en utilisant les informations de l'utilisateur
            db_connection = create_engine(f"mysql+pymysql://{username}:{password}@localhost:3306/data")
            # Effectuez des opérations sur la base de données en utilisant db_connection

            return jsonify({'message': 'Database access granted'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        '''
'''class DatabaseUser(db.Model):
    __tablename__ = 'database_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)'''
'''@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        connection_string = get_connection_string(username, password)
        app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
            return jsonify(message='Invalid credentials'), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500     '''   
        
        
###################################################"creation user simple "
'''@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')  

        # Créer un hachage sécurisé du mot de passe
        password_hash = generate_password_hash(password).decode('utf-8')

        # Créer un nouvel utilisateur dans la table "user" avec l'e-mail et le mot de passe hashé
        new_user = User(username=username, password=password_hash, email=email)
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        # Recherche de l'utilisateur dans la base de données
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return jsonify({'message': 'Connected successfully'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500'''
    
#############################################creation du user data base"    
'''@app.route('/create_db_user', methods=['POST'])
def create_db_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        superuser_username = 'root'
        superuser_password = 'root'

        conn = pymysql.connect(
            user=superuser_username,
            password=superuser_password,
            host='localhost',
            database='data',
            #auth_plugin='mysql_native_password'
        )

        # Create a cursor and execute the CREATE USER command
        cursor = conn.cursor()
        cursor.execute(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON data.* TO '{username}'@'localhost'")
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'Database user created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# Dictionary to store user engines'''
'''user_engines = {}

@app.route('/login_db_user', methods=['POST'])
def login_db():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        conn = pymysql.connect(
            user=username,
            password=password,
            host='localhost',
            database='data',
        )

        engine = create_engine(f'mysql+pymysql://{username}:{password}@localhost/data')

        user_engines[username] = engine

        conn.close()

        return jsonify({'message': 'Login successful'}), 200
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 401
    
    
print('aaaaaaaaaaaaaaaaaaaaaaa',user_engines )'''

'''db_url = "mysql+mysqlconnector://root:root@localhost:3306/data"
engine = create_engine(db_url)
data = pd.read_sql("SELECT * FROM customer", engine)
    
#############################select all customer 
@app.route('/get_customers', methods=['GET'])
def get_all_customers():
    try:
        customers = data.to_dict(orient='records')

        return jsonify(customers), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500    
    
    
@app.route('/get_pie_data')
def get_pie_data():
    # Compter le nombre de clients pour chaque pays
    country_counts = data['country'].value_counts()

    # Récupérer les noms des pays et le nombre de clients pour chaque pays
    countries = country_counts.index.tolist()
    counts = country_counts.values.tolist()

    # Retourner les données nécessaires sous forme de JSON
    pie_data = {
        'labels': countries,
        'data': counts
    }
    return jsonify(pie_data)

@app.route('/get_bar_data')
def get_bar_data():
    
    age_groups = ['18-25', '26-35', '36-45', '46-55', '56+']
    total_balance = data['balance'].sum()
    account_percentages = []
    
    for group in age_groups:
        if group == '56+':
            lower_age = 56
            balance = data[data['age'] >= lower_age]['balance'].sum()
        else:
            lower_age, upper_age = map(int, group.split('-'))
            balance = data[(data['age'] >= lower_age) & (data['age'] <= upper_age)]['balance'].sum()
        
        percentage = (balance / total_balance) * 100
        account_percentages.append(round(percentage, 2))
    
    bar_data = {
        'labels': age_groups,
        'data': account_percentages
    }
    return jsonify(bar_data)
@app.route('/get_doughnut_data')
def get_doughnut_data():
    # Compter le nombre de clients actifs (active_member = 1) et inactifs (active_member = 0)
    active_counts = data['active_member'].value_counts()

    # Mapper les valeurs 0 et 1 aux étiquettes "female" et "male"
    active_counts.index = active_counts.index.map({0: 'Female', 1: 'Male'})

    # Récupérer les noms des catégories (actifs et inactifs) et le nombre de clients pour chaque catégorie
    categories = active_counts.index.tolist()
    counts = active_counts.values.tolist()

    # Retourner les données nécessaires sous forme de JSON
    doughnut_data = {
        'labels': categories,
        'data': counts
    }
    return jsonify(doughnut_data)

@app.route('/get_gender_data')
def get_gender_data():
    # Compter le nombre d'hommes et de femmes
    gender_counts = data['gender'].value_counts()

    # Récupérer les genres et le nombre correspondant
    genders = gender_counts.index.tolist()
    counts = gender_counts.values.tolist()

    # Retourner les données nécessaires sous forme de JSON
    gender_data = {
        'labels': genders,
        'data': counts
    }
    return jsonify(gender_data)

@app.route('/get_active_customer_data')
def get_active_customer_data():
    # Convertir la colonne 'churn' en un format numérique
    data['churn'] = pd.to_numeric(data['churn'], errors='coerce')
    
    # Filtrer les clients actifs (churn = 0)
    active_customers = data[data['churn'] == 0]
    
    # Calculer le nombre cumulatif de clients actifs par rapport à l'âge
    active_customers['cumulative_count'] = active_customers.groupby('age')['customer_id'].cumcount() + 1
    
    response_data = {
        "ages": active_customers['age'].unique().tolist(),
        "cumulative_counts": active_customers.groupby('age')['cumulative_count'].max().tolist()
    }
    
    return jsonify(response_data)    '''
  
  
  
'''@app.route('/get_pie_data')
def get_pie_data():
    # Compter le nombre de clients pour chaque pays
    country_counts = data['country'].value_counts()

    # Récupérer les noms des pays et le nombre de clients pour chaque pays
    countries = country_counts.index.tolist()
    counts = country_counts.values.tolist()

    # Retourner les données nécessaires sous forme de JSON
    pie_data = {
        'labels': countries,
        'data': counts
    }
    return jsonify(pie_data)
    
    
@app.route('/add_customer', methods=['POST'])
def add_customer():
    if 'username' in session:
        try:
            username = session['username']
            password = session['password']
            connection_string = get_connection_string(username, password)
            app.config['SQLALCHEMY_DATABASE_URI'] = connection_string

            user = User.query.filter_by(username=username).first()

            credit_score = request.json.get('credit_score')
            country = request.json.get('country')
            gender = request.json.get('gender')
            age = request.json.get('age')
            tenure = request.json.get('tenure')
            balance = request.json.get('balance')
            products_number = request.json.get('products_number')
            credit_card = request.json.get('credit_card')
            active_member = request.json.get('active_member')
            estimated_salary = request.json.get('estimated_salary')
            churn = request.json.get('churn')

            new_customer = Customer(
                credit_score=credit_score,
                country=country,
                gender=gender,
                age=age,
                tenure=tenure,
                balance=balance,
                products_number=products_number,
                credit_card=credit_card,
                active_member=active_member,
                estimated_salary=estimated_salary,
                churn=churn,
                id_user=user.id
            )

            db.session.add(new_customer)
            db.session.commit()

            return "Customer added successfully."
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return "Please log in first."    '''
'''@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            response_data = {
                'message': 'Logged in successfully',
                'idUser': user.id
            }
            
            connection_string = get_connection_string(username, password)
            engine = create_engine(connection_string)
            Session = scoped_session(sessionmaker(engine))
           # print(Session.query(Customer.credit_score).filter(Customer.customer_id==15571873).first())
            session['username'] = username
            session['user_id'] = user.id  
            
            return jsonify(response_data), 200
        else:
            return "Invalid username or password", 401
        

    except Exception as e:
        return jsonify({'error': str(e)}), 500'''          
        
        
'''@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            response_data = {
                'message': 'Logged in successfully',
                'idUser': user.id
            }
            
            connection_string = get_connection_string(username, password)
            engine = create_engine(connection_string)
            data_base = scoped_session(sessionmaker(engine))
            session['username'] = username
            session['user_id'] = user.id  
            session['data_base']=data_base
            
            return jsonify(response_data), 200
        else:
            return "Invalid username or password", 401
        

    except Exception as e:
        return jsonify({'error': str(e)}), 500
##############################################pie chart        
@app.route('/get_pie_data', methods=['GET'])
def get_pie_data():
    try:
        user_id = session.get('user_id')
        Data = session.get("data_base")
        print(user_id)
        if user_id is None:
            return jsonify({"error": "User not logged in"}), 401

        customer_data = Customer.query.filter_by(user_id=user_id).all()
        customer_data = Data.query
        country_counts = {}
        for customer in customer_data:
            country = customer.country
            if country in country_counts:
                country_counts[country] += 1
            else:
                country_counts[country] = 1

        countries = list(country_counts.keys())
        counts = list(country_counts.values())

        pie_data = {
            'labels': countries,
            'data': counts
        }
        return jsonify(pie_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
        
        
# Create an empty dictionary to hold user-specific SQLAlchemy instances
#user_db_instances = {}


'''@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            response_data = {
                'message': 'Logged in successfully',
                'idUser': user.id
            }
            
            # # Check if an SQLAlchemy instance for this user already exists
            if username in user_db_instances:
                db = user_db_instances[username]
            else:
                connection_string = get_connection_string(username, password)
                engine = create_engine(connection_string)
                # what engine.execute() is doing under the hood:
                Session =scoped_session(sessionmaker(engine)) 
                a=Session.query(Customer.credit_score).filter(Customer.customer_id==15571873).first()
               
                #  app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
                #  db = SQLAlchemy(app)
                user_db_instances[username] = db
            
            session['username'] = username
            return jsonify(response_data), 200
        else:
            return "Invalid username or password", 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
'''@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            response_data = {
                'message': 'Logged in successfully',
                'idUser': user.id
            }
            
            connection_string = get_connection_string(username, password)
            engine = create_engine(connection_string)
            #data_ba = scoped_session(sessionmaker(engine))
            session['username'] = username
            session['user_id'] = user.id  
            #Session['user_id']=user.id
            
            return jsonify(response_data), 200
        else:
            return "Invalid username or password", 401
        

    except Exception as e:
        return jsonify({'error': str(e)}), 500
##############################################pie chart        
@app.route('/get_pie_data', methods=['GET'])
def get_pie_data():
    try:
        user_id = session.get('user_id')
        print(user_id)
        if user_id is None:
            return jsonify({"error": "User not logged in"}), 401

        customer_data = Customer.query.filter_by(user_id=user_id).all()
  
        country_counts = {}
        for customer in customer_data:
            country = customer.country
            if country in country_counts:
                country_counts[country] += 1
            else:
                country_counts[country] = 1

        countries = list(country_counts.keys())
        counts = list(country_counts.values())

        pie_data = {
            'labels': countries,
            'data': counts
        }
        return jsonify(pie_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500'''        
'''@app.route('/get_gender_data', methods=['GET'])
def get_gender_data():
    try:
        user_id = session.get('user_id')
        connection_string = session.get("connection_string")
        Data = get_session(connection_string)
        
        if user_id is None:
            return jsonify({"error": "User not logged in"}), 401
        
        #customer_data = Customer.query.filter_by(user_id=user_id).all()
        customer_data = Data.execute(text(f"Select * from customer where user_id = {user_id}")).fetchall()
        
        gender_counts = {'Male': 0, 'Female': 0}
        
        for customer in customer_data:
            gender = customer.gender
            if gender == 'Male':
                gender_counts['Male'] += 1
            elif gender == 'Female':
                gender_counts['Female'] += 1
        
        genders = list(gender_counts.keys())
        counts = list(gender_counts.values())

        gender_data = {
            'labels': genders,
            'data': counts
        }
        return jsonify(gender_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500'''        