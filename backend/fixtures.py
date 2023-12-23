from app import db
from app import User, Customer


def add_customers_to_user():
    user_id = 26  

    customer_data = [
        {'customer_id': 15634602, 'credit_score': 619, 'country': 'France', 'gender': 'Female', 'age': 42, 'tenure': 2, 'balance': 0, 'products_number': 1, 'credit_card': 1, 'active_member': 1, 'estimated_salary': 101348.88, 'churn': 1},
        {'customer_id': 15647311, 'credit_score': 608, 'country': 'Spain', 'gender': 'Female', 'age': 41, 'tenure': 1, 'balance': 83807.86, 'products_number': 1, 'credit_card': 0, 'active_member': 1, 'estimated_salary': 112542.58, 'churn': 0},
        {'customer_id': 15701354, 'credit_score': 699, 'country': 'France', 'gender': 'Female', 'age': 39, 'tenure': 1, 'balance': 0, 'products_number': 2, 'credit_card': 0, 'active_member': 0, 'estimated_salary': 93826.63, 'churn': 0},
        {'customer_id': 15737888, 'credit_score': 850, 'country': 'Spain', 'gender': 'Female', 'age': 43, 'tenure': 2, 'balance': 125510.82, 'products_number': 1, 'credit_card': 1, 'active_member': 1, 'estimated_salary': 79084.1, 'churn': 0},
        {'customer_id': 15574012, 'credit_score': 645, 'country': 'Spain', 'gender': 'Male', 'age': 44, 'tenure': 8, 'balance': 113755.78, 'products_number': 2, 'credit_card': 1, 'active_member': 0, 'estimated_salary': 149756.71, 'churn': 1},
        {'customer_id': 15592531, 'credit_score': 822, 'country': 'France', 'gender': 'Male', 'age': 50, 'tenure': 7, 'balance': 0, 'products_number': 2, 'credit_card': 1, 'active_member': 1, 'estimated_salary': 10062.8, 'churn': 0},
        {'customer_id': 15656148, 'credit_score': 376, 'country': 'Germany', 'gender': 'Female', 'age': 29, 'tenure': 4, 'balance': 115046.74, 'products_number': 4, 'credit_card': 1, 'active_member': 0, 'estimated_salary': 119346.88, 'churn': 1},
       
    ]

    for customer_info in customer_data:
        customer = Customer(
            customer_id=customer_info['customer_id'],
            credit_score=customer_info['credit_score'],
            country=customer_info['country'],
            gender=customer_info['gender'],
            age=customer_info['age'],
            tenure=customer_info['tenure'],
            balance=customer_info['balance'],
            products_number=customer_info['products_number'],
            credit_card=customer_info['credit_card'],
            active_member=customer_info['active_member'],
            estimated_salary=customer_info['estimated_salary'],
            churn=customer_info['churn'],
            user_id=user_id  
        )
        db.session.add(customer)

    db.session.commit()

