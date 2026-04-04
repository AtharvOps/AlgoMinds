import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from services.user_service import save_user, authenticate_user
    print("✅ user_service imported successfully")
    
    # Test saving a user
    test_user = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'full_name': 'Test User',
        'phone': '1234567890',
        'role': 'user',
        'user_id': 'test-123'
    }
    
    result = save_user(test_user)
    print(f"Save result: {result}")
    
    # Test authentication
    auth_result = authenticate_user('test@example.com', 'password123')
    print(f"Auth result: {auth_result}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
