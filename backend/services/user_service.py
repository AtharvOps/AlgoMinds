import pandas as pd
import os
from datetime import datetime
import hashlib

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(user_data):
    """
    Save user data to the CSV database
    """
    try:
        # Define the CSV file path
        csv_file = "database/user_db.csv"
        
        # Check if user already exists
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            if user_data['email'] in df['email'].values:
                return {"success": False, "message": "Email already exists"}
            if user_data['username'] in df['username'].values:
                return {"success": False, "message": "Username already exists"}
        
        # Hash the password
        hashed_password = hash_password(user_data['password'])
        
        # Extract relevant fields for CSV storage
        user_record = {
            'user_id': user_data.get('user_id', ''),
            'username': user_data.get('username', ''),
            'email': user_data.get('email', ''),
            'password': hashed_password,
            'full_name': user_data.get('full_name', ''),
            'phone': user_data.get('phone', ''),
            'role': user_data.get('role', 'user'),
            'is_active': True,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_login': None
        }
        
        # Check if file exists
        file_exists = os.path.exists(csv_file)
        
        # Convert to DataFrame
        df = pd.DataFrame([user_record])
        
        # Append to CSV with proper header handling
        df.to_csv(csv_file, mode='a', header=not file_exists, index=False)
        
        print(f"User {user_record['username']} saved successfully to {csv_file}")
        return {"success": True, "message": "User registered successfully"}
        
    except Exception as e:
        print(f"Error saving user to database: {e}")
        return {"success": False, "message": "Registration failed"}

def authenticate_user(email, password):
    """
    Authenticate user login
    """
    try:
        csv_file = "database/user_db.csv"
        
        if not os.path.exists(csv_file):
            return {"success": False, "message": "No users found"}
        
        df = pd.read_csv(csv_file)
        
        # Find user by email
        user = df[df['email'] == email]
        
        if user.empty:
            return {"success": False, "message": "Invalid email or password"}
        
        # Check password
        stored_password = user.iloc[0]['password']
        input_password = hash_password(password)
        
        if stored_password != input_password:
            return {"success": False, "message": "Invalid email or password"}
        
        # Check if user is active
        if not user.iloc[0]['is_active']:
            return {"success": False, "message": "Account is inactive"}
        
        # Update last login
        df.loc[df['email'] == email, 'last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            df.to_csv(csv_file, index=False)
        except Exception as save_error:
            print(f"Warning: Could not update last_login: {save_error}")
            # Continue even if save fails
        
        # Return user data (without password)
        user_data = {
            "user_id": user.iloc[0]['user_id'],
            "username": user.iloc[0]['username'],
            "email": user.iloc[0]['email'],
            "full_name": user.iloc[0]['full_name'],
            "phone": user.iloc[0]['phone'],
            "role": user.iloc[0]['role'],
            "last_login": user.iloc[0]['last_login']
        }
        
        return {"success": True, "message": "Login successful", "user": user_data}
        
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return {"success": False, "message": "Login failed"}

def get_all_users():
    """
    Retrieve all users from the database
    """
    try:
        csv_file = "database/user_db.csv"
        
        if not os.path.exists(csv_file):
            return pd.DataFrame()
        
        df = pd.read_csv(csv_file)
        # Remove password column for security
        if 'password' in df.columns:
            df = df.drop('password', axis=1)
        return df
        
    except Exception as e:
        print(f"Error reading users from database: {e}")
        return pd.DataFrame()

def get_user_by_id(user_id):
    """
    Retrieve a specific user by ID
    """
    try:
        df = get_all_users()
        
        if df.empty:
            return None
        
        user = df[df['user_id'] == user_id]
        
        if user.empty:
            return None
            
        return user.iloc[0].to_dict()
        
    except Exception as e:
        print(f"Error retrieving user {user_id}: {e}")
        return None

def get_user_statistics():
    """
    Get statistics about users in the database
    """
    try:
        df = get_all_users()
        
        if df.empty:
            return {
                'total_users': 0,
                'active_users': 0,
                'admin_users': 0,
                'regular_users': 0,
                'new_users_today': 0
            }
        
        total_users = len(df)
        active_users = len(df[df['is_active'] == True])
        admin_users = len(df[df['role'] == 'admin'])
        regular_users = len(df[df['role'] == 'user'])
        
        # New users today
        today = datetime.now().strftime('%Y-%m-%d')
        new_users_today = len(df[df['created_at'].str.startswith(today)])
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'admin_users': admin_users,
            'regular_users': regular_users,
            'new_users_today': new_users_today
        }
        
    except Exception as e:
        print(f"Error calculating user statistics: {e}")
        return {
            'total_users': 0,
            'active_users': 0,
            'admin_users': 0,
            'regular_users': 0,
            'new_users_today': 0
        }

def update_user_status(user_id, is_active):
    """
    Update user active status
    """
    try:
        csv_file = "database/user_db.csv"
        
        if not os.path.exists(csv_file):
            return False
        
        df = pd.read_csv(csv_file)
        
        # Find the user
        user_index = df[df['user_id'] == user_id].index
        
        if user_index.empty:
            return False
        
        # Update the user
        df.loc[user_index, 'is_active'] = is_active
        
        # Save back to CSV
        df.to_csv(csv_file, index=False)
        
        print(f"User {user_id} status updated successfully")
        return True
        
    except Exception as e:
        print(f"Error updating user {user_id}: {e}")
        return False
