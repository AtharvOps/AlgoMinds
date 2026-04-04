import pandas as pd
import os
from datetime import datetime

def save_claim(data):
    """
    Save claim data to the CSV database
    """
    try:
        # Define the CSV file path
        csv_file = "database/claims_db.csv"
        
        # Extract relevant fields for CSV storage
        claim_record = {
            'claim_amount': data.get('claim_amount', 0),
            'repair_estimate': data.get('repair_estimates', 0),
            'previous_claims': data.get('previous_claims', 0),
            'policy_validity': data.get('policy_duration', 0),
            'image_uploaded': data.get('image_uploaded', 0),
            'damage_consistency': data.get('damage_consistency', 1),
            'user_phone': data.get('phone_number', ''),
            'aadhar_number': data.get('aadhar_number', ''),
            'garage_id': data.get('garage_id', ''),
            'agent_id': data.get('agent_id', ''),
            'garage_city': data.get('garage_city', ''),
            'accident_location': data.get('accident_location', ''),
            'claim_id': data.get('claim_id', ''),
            'user_id': data.get('user_id', ''),
            'is_fraud': data.get('is_fraud', 0)
        }
        
        # Check if file exists
        file_exists = os.path.exists(csv_file)
        
        # Convert to DataFrame
        df = pd.DataFrame([claim_record])
        
        # Append to CSV
        df.to_csv(csv_file, mode='a', header=not file_exists, index=False)
        
        print(f"Claim {claim_record['claim_id']} saved successfully to database")
        return True
        
    except Exception as e:
        print(f"Error saving claim to database: {e}")
        return False

def get_all_claims():
    """
    Retrieve all claims from the database
    """
    try:
        csv_file = "database/claims_db.csv"
        
        if not os.path.exists(csv_file):
            return pd.DataFrame()
        
        df = pd.read_csv(csv_file)
        return df
        
    except Exception as e:
        print(f"Error reading claims from database: {e}")
        return pd.DataFrame()

def get_claim_by_id(claim_id):
    """
    Retrieve a specific claim by ID
    """
    try:
        df = get_all_claims()
        
        if df.empty:
            return None
        
        claim = df[df['claim_id'] == claim_id]
        
        if claim.empty:
            return None
            
        return claim.iloc[0].to_dict()
        
    except Exception as e:
        print(f"Error retrieving claim {claim_id}: {e}")
        return None

def get_claims_by_user(user_id):
    """
    Retrieve all claims for a specific user
    """
    try:
        df = get_all_claims()
        
        if df.empty:
            return []
        
        user_claims = df[df['user_id'] == user_id]
        return user_claims.to_dict('records')
        
    except Exception as e:
        print(f"Error retrieving claims for user {user_id}: {e}")
        return []

def update_claim_status(claim_id, status, is_fraud=None):
    """
    Update claim status and/or fraud determination
    """
    try:
        csv_file = "database/claims_db.csv"
        
        if not os.path.exists(csv_file):
            return False
        
        df = pd.read_csv(csv_file)
        
        # Find the claim
        claim_index = df[df['claim_id'] == claim_id].index
        
        if claim_index.empty:
            return False
        
        # Update the claim
        if status:
            df.loc[claim_index, 'status'] = status
        
        if is_fraud is not None:
            df.loc[claim_index, 'is_fraud'] = is_fraud
        
        # Save back to CSV
        df.to_csv(csv_file, index=False)
        
        print(f"Claim {claim_id} updated successfully")
        return True
        
    except Exception as e:
        print(f"Error updating claim {claim_id}: {e}")
        return False

def get_claims_statistics():
    """
    Get statistics about claims in the database
    """
    try:
        df = get_all_claims()
        
        if df.empty:
            return {
                'total_claims': 0,
                'fraud_claims': 0,
                'genuine_claims': 0,
                'fraud_rate': 0,
                'total_amount': 0,
                'avg_claim_amount': 0
            }
        
        total_claims = len(df)
        fraud_claims = len(df[df['is_fraud'] == 1])
        genuine_claims = total_claims - fraud_claims
        fraud_rate = (fraud_claims / total_claims * 100) if total_claims > 0 else 0
        total_amount = df['claim_amount'].sum()
        avg_claim_amount = df['claim_amount'].mean()
        
        return {
            'total_claims': total_claims,
            'fraud_claims': fraud_claims,
            'genuine_claims': genuine_claims,
            'fraud_rate': round(fraud_rate, 2),
            'total_amount': round(total_amount, 2),
            'avg_claim_amount': round(avg_claim_amount, 2)
        }
        
    except Exception as e:
        print(f"Error calculating claim statistics: {e}")
        return {
            'total_claims': 0,
            'fraud_claims': 0,
            'genuine_claims': 0,
            'fraud_rate': 0,
            'total_amount': 0,
            'avg_claim_amount': 0
        }
