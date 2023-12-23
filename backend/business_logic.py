'''import pandas as pd
from data_access import DataAccess

class BusinessLogic:
    def __init__(self):
        self.data_access = DataAccess()

    def get_pie_data(self):
        data = self.data_access.get_customer_data()

        # Compter le nombre de clients pour chaque pays
        country_counts = data['country'].value_counts()

        # Récupérer les noms des pays et le nombre de clients pour chaque pays
        countries = country_counts.index.tolist()
        counts = country_counts.values.tolist()

        # Préparer les données pour le graphique circulaire
        pie_data = {
            'labels': countries,
            'data': counts
        }

        return pie_data

    def get_bar_data(self):
        data = self.data_access.get_customer_data()

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
        return bar_data
    
    def get_doughnut_data(self):
        data = self.data_access.get_customer_data()

        # Compter le nombre de clients actifs (active_member = 1) et inactifs (active_member = 0)
        active_counts = data['active_member'].value_counts()

        # Récupérer les noms des catégories (actifs et inactifs) et le nombre de clients pour chaque catégorie
        categories = active_counts.index.tolist()
        counts = active_counts.values.tolist()

        # Transformer les catégories 0 et 1 en "female" et "male"
        categories = ["Female" if cat == 0 else "Male" for cat in categories]

        # Retourner les données nécessaires sous forme de JSON
        doughnut_data = {
            'labels': categories,
            'data': counts
        }
        return doughnut_data
    
    def get_active_customer_data(self):
        data = self.data_access.get_customer_data()

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
        
        return response_data'''
        
from data_access import DataAccess

class BusinessLogic:
    def __init__(self):
        self.data_access = DataAccess()

    def get_pie_data(self, user_id):
        data = self.data_access.get_customer_data(user_id)

        country_counts = data['country'].value_counts()

        countries = country_counts.index.tolist()
        counts = country_counts.values.tolist()

        pie_data = {
            'labels': countries,
            'data': counts
        }

        return pie_data
