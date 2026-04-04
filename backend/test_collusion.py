import pandas as pd

# Test reading your CSV
try:
    # Try reading line by line to handle variable columns
    with open('database/claims_db.csv', 'r') as f:
        lines = f.readlines()
    
    print(f"Total lines: {len(lines)}")
    for i, line in enumerate(lines[:8]):
        parts = line.strip().split(',')
        print(f"Line {i}: {len(parts)} parts -> {parts}")
    
    # Manual collusion detection
    mobile_counts = {}
    garage_counts = {}
    agent_counts = {}
    
    for i, line in enumerate(lines):
        parts = line.strip().split(',')
        
        # Extract data safely
        user_phone = parts[6] if len(parts) > 6 and parts[6] != '' and parts[6] != 'nan' else ''
        garage_id = parts[8] if len(parts) > 8 and parts[8] != '' and parts[8] != 'nan' else ''
        agent_id = parts[9] if len(parts) > 9 and parts[9] != '' and parts[9] != 'nan' else ''
        claim_id = parts[12] if len(parts) > 12 and parts[12] != '' and parts[12] != 'nan' else f'CLM-{i}'
        
        # Count mobile numbers
        if user_phone:
            if user_phone not in mobile_counts:
                mobile_counts[user_phone] = []
            mobile_counts[user_phone].append(claim_id)
        
        # Count garages
        if garage_id:
            if garage_id not in garage_counts:
                garage_counts[garage_id] = []
            garage_counts[garage_id].append(claim_id)
        
        # Count agents
        if agent_id:
            if agent_id not in agent_counts:
                agent_counts[agent_id] = []
            agent_counts[agent_id].append(claim_id)
    
    print("\nCollusion Analysis:")
    print("Mobile numbers:", mobile_counts)
    print("Garages:", garage_counts)
    print("Agents:", agent_counts)
    
except Exception as e:
    print(f"Error: {e}")
