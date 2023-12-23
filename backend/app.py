from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import create_engine
import pymysql
import pandas as pd
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import generate_password_hash
from flask_bcrypt import check_password_hash
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import random
from util import get_session
app = Flask(__name__)
#CORS(app, supports_credentials=True)
CORS(app, supports_credentials=True)    



app.config['SECRET_KEY'] = 'isned@123' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/data'
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  
    password = db.Column(db.String(100), nullable=False)
    customers = db.relationship('Customer', backref='user', lazy=True)


  
class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    credit_score = db.Column(db.Integer)
    country = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    tenure = db.Column(db.Integer)
    balance = db.Column(db.Float)
    products_number = db.Column(db.Integer)
    credit_card = db.Column(db.Integer)
    active_member = db.Column(db.Integer)
    estimated_salary = db.Column(db.Float)
    churn = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  
    
    

def get_connection_string(username, password):
    return f"mysql+pymysql://{username}:{password}@localhost/data"
    
    
    
@app.route('/logout')
def logout():
    response_data = {'message': 'Déconnexion réussie'}
    response = make_response(jsonify(response_data), 200)
    response.set_cookie('session', '', expires=0)
    return response

@app.route('/create_db_user', methods=['POST'])
def create_db_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email') 

        superuser_username = 'root'
        superuser_password = 'root'

        conn = pymysql.connect(
            user=superuser_username,
            password=superuser_password,
            host='localhost',
            database='data',
        )
        
        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'")
            cursor.execute(f"GRANT ALL PRIVILEGES ON data.Customer TO '{username}'@'localhost'")
            conn.commit()
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()

      
        password_hash = generate_password_hash(password)
       
        try:
            new_user = User(username=username, password=password_hash, email=email)  
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'Database user created successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500 

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/login', methods=['POST'])
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
            
            session['username'] = username
            session['user_id'] = user.id  
            session['connection_string']= connection_string
            
            return jsonify(response_data), 200
        else:
            return "Invalid username or password", 401
        

    except Exception as e:
        return jsonify({'error': str(e)}), 406
##############################################pie chart        
@app.route('/get_pie_data', methods=['GET'])
def get_pie_data():
    try:
        user_id = session.get('user_id')
        connection_string = session.get("connection_string")
        Data = get_session(connection_string)
        print(user_id)
        if user_id is None:
            return jsonify({"error": "User not logged in"}), 401

        #customer_data = Customer.query.filter_by(user_id=user_id).all()
        customer_data = Data.execute(text(f"Select * from customer where user_id = {user_id}")).fetchall()
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
#################################################"bar chart"
@app.route('/get_bar_data', methods=['GET'])
def get_bar_data():
    try:
        user_id = session.get('user_id')
        connection_string = session.get("connection_string")
        Data = get_session(connection_string)
        print(user_id)
        if user_id is None:
            return jsonify({"error": "User not logged in"}), 401

        #customer_data = Customer.query.filter_by(user_id=user_id).all()
        customer_data = Data.execute(text(f"Select * from customer where user_id = {user_id}")).fetchall()
        
        age_groups = ['18-25', '26-35', '36-45', '46-55', '56+']
        total_balance = sum([customer.balance or 0 for customer in customer_data])
        
        account_percentages = []
        
        for group in age_groups:
            if group == '56+':
                lower_age = 56
                balance = sum([customer.balance or 0 for customer in customer_data if customer.age and customer.age >= lower_age])
            else:
                lower_age, upper_age = map(int, group.split('-'))
                balance = sum([customer.balance or 0 for customer in customer_data if customer.age and lower_age <= customer.age <= upper_age])
            
            percentage = (balance / total_balance) * 100
            account_percentages.append(round(percentage, 2))
        
        bar_data = {
            'labels': age_groups,
            'data': account_percentages
        }
        return jsonify(bar_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


##########################################dougnout chart 

@app.route('/get_credit_card_data', methods=['GET'])
def get_credit_card_data():
    try:
        user_id = session.get('user_id')
        connection_string = session.get("connection_string")
        Data = get_session(connection_string)
        
        if user_id is None:
            return jsonify({"error": "Utilisateur non connecté"}), 401
        
        customer_data = Data.execute(text(f"SELECT * FROM customer WHERE user_id = {user_id}")).fetchall()
        
        credit_card_counts = {'Oui': 0, 'Non': 0}
        
        for customer in customer_data:
            credit_card = customer.credit_card
            if credit_card == 1:  # Supposons que 1 représente 'Oui' et 0 représente 'Non'
                credit_card_counts['Oui'] += 1
            else:
                credit_card_counts['Non'] += 1
        
        card_labels = list(credit_card_counts.keys())
        card_counts = list(credit_card_counts.values())

        card_data = {
            'labels': card_labels,
            'data': card_counts
        }
        return jsonify(card_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

####################################################line data
@app.route('/get_active_customer_data')
def get_active_customer_data():
    user_id = session.get('user_id')  
    
    user_data = Customer.query.filter_by(user_id=user_id).all() 
    
    for customer in user_data:
        if customer.churn is not None: 
            customer.churn = int(customer.churn)
    
    active_customers = [customer for customer in user_data if customer.churn == 0]
    
    cumulative_counts = {}
    for customer in active_customers:
        if customer.age in cumulative_counts:
            cumulative_counts[customer.age] += 1
        else:
            cumulative_counts[customer.age] = 1
    
    response_data = {
        "ages": list(cumulative_counts.keys()),
        "cumulative_counts": list(cumulative_counts.values())
    }
    
    return jsonify(response_data)
################################################
@app.route('/get_country_churn_rate_data')
def get_country_churn_rate_data():
    user_id = session.get('user_id')  
    
    user_data = Customer.query.filter_by(user_id=user_id).all() 
    
    for customer in user_data:
        if customer.churn is not None: 
            customer.churn = int(customer.churn)
    
    countries = []
    churn_rates = []

    for country in set(customer.country for customer in user_data):
        churn_rates.append({
            'country': country,
            'churn_rate': sum(customer.churn for customer in user_data if customer.country == country) / len(user_data)
        })

    churn_rates.sort(key=lambda x: x['country'])
    
    return jsonify(churn_rates)

@app.route('/get_customers', methods=['GET'])
def get_customers():
    try:
        user_id = session.get('user_id')
        connection_string = session.get("connection_string")
        Data = get_session(connection_string)

        if user_id is None:
            return jsonify({"error": "User not logged in"}), 401

        # customers = Customer.query.filter_by(user_id=user_id).all()
        customers = Data.execute(text(f"Select * from customer where user_id = {user_id}")).fetchall()
        customer_data = []

        for customer in customers:
            customer_info = {
                'id': customer.customer_id,
                'credit_score': customer.credit_score,
                'country': customer.country,
                'gender': customer.gender,
                'age': customer.age,
                'tenure': customer.tenure,
                'balance': customer.balance,
                
                'credit_card': customer.credit_card,
                'active_member': customer.active_member,
                'estimated_salary': customer.estimated_salary,
                'churn': customer.churn
            }
            customer_data.append(customer_info)

        return jsonify(customer_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#######################################ajout de client 
@app.route('/add_customer', methods=['POST'])
def add_customer():
    if 'user_id' not in session:
        return "User not logged in", 401

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    data = request.json
    new_customer = Customer(
        credit_score=data['credit_score'],
        country=data['country'],
        gender=data['gender'],     # Use 'gender' instead of 'sexe'
        age=data['age'],           # Use 'age' instead of 'âge'
        tenure=data['anciennete'], # Use 'anciennete' instead of 'tenure'
        balance=data['solde'],     # Use 'solde' instead of 'balance'
        credit_card=data['carte_de_credit'],
        active_member=data['membre_actif'],
        estimated_salary=data['salaire_estime'],
        churn=data['desabonnement'],
        user_id=user.id
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"message": "Customer added successfully"}), 201


@app.route('/delete_customer/<int:id>', methods=['DELETE'])  # Change the method to DELETE
def delete_customer(id):  # Notice the parameter 'id' here
    if 'user_id' not in session:
        return "User not logged in", 401

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    # No need to process request.json for DELETE method

    if id is None:
        return "Missing customer_id in request", 400

    customer = Customer.query.filter_by(customer_id=id, user_id=user.id).first()
    if not customer:
        return "Customer not found or not authorized", 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted successfully"}), 200


########################################""modifier customer 
@app.route('/update_customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    if 'user_id' not in session:
        return "User not logged in", 401

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    
    
    data = request.json
    customer.credit_score = data['credit_score']
    customer.country = data['country']
    customer.gender = data['gender']
    customer.age = data['age']
    customer.tenure = data['anciennete']
    customer.balance = data['solde']
    #customer.products_number = data['products_number']
    customer.credit_card = data['carte_de_credit']
    
    # Convertir 'yes' en 1, 'no' en 0 pour 'active_member'
    if data['membre_actif'] == 'yes':
        customer.active_member = 1
    else:
        customer.active_member = 0

    customer.estimated_salary = data['salaire_estime']
    
    # Convertir 'yes' en 1, 'no' en 0 pour 'churn'
    if data['desabonnement'] == 'yes':
        customer.churn = 1
    else:
        customer.churn = 0

    db.session.commit()

    return jsonify({"message": "Customer updated successfully"})
@app.route('/get_all_customers', methods=['GET'])
def get_all_customers():
    # Fetch the updated list of customers from the database
    updated_customers = Customer.query.all()
    # Serialize the customer data and return it
    serialized_customers = [customer.serialize() for customer in updated_customers]
    return jsonify(serialized_customers)


if __name__ == '__main__':
    
    app.run(debug=True)
