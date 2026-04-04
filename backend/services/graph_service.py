import pandas as pd

def check_collusion(data):
    risk = 0
    reasons = []

    try:
        df = pd.read_csv("database/claims.csv")
        
        # Check for mobile number reuse
        if data.get("user_phone"):
            phone_matches = df[df['user_phone'] == data["user_phone"]]
            if len(phone_matches) >= 2:
                risk += 50
                reasons.append(f"Mobile number used in {len(phone_matches)} claims")
        
        # Check for garage-agent collusion
        if data.get("garage_id") and data.get("agent_id"):
            garage_agent_matches = df[
                (df['garage_id'] == data["garage_id"]) &
                (df['agent_id'] == data["agent_id"])
            ]
            if len(garage_agent_matches) > 1:
                risk += 40
                reasons.append(f"Garage-Agent pair used in {len(garage_agent_matches)} claims")
        
        # Check for garage reuse
        if data.get("garage_id"):
            garage_matches = df[df['garage_id'] == data["garage_id"]]
            if len(garage_matches) > 2:
                risk += 30
                reasons.append(f"Garage used in {len(garage_matches)} claims")
        
        # Check for agent reuse
        if data.get("agent_id"):
            agent_matches = df[df['agent_id'] == data["agent_id"]]
            if len(agent_matches) > 2:
                risk += 30
                reasons.append(f"Agent used in {len(agent_matches)} claims")
        
        # Check for garage city concentration
        if data.get("garage_city"):
            city_matches = df[df['garage_city'] == data["garage_city"]]
            if len(city_matches) > 3:
                risk += 20
                reasons.append(f"High claim concentration in {data['garage_city']}")
        
        # Check for accident location concentration
        if data.get("accident_location"):
            location_matches = df[df['accident_location'] == data["accident_location"]]
            if len(location_matches) > 2:
                risk += 25
                reasons.append(f"High claim frequency at {data['accident_location']}")

    except Exception as e:
        print(f"Error in collusion detection: {e}")
        pass

    return risk, reasons

def get_collusion_alerts():
    """Get all collusion alerts for admin dashboard using real data"""
    try:
        # Read CSV manually to handle variable column counts
        with open('database/claims.csv', 'r') as f:
            lines = f.readlines()
        
        alerts = []
        
        print(f"CSV shape: {len(lines)} lines")
        
        # Skip header line and process data
        for i, line in enumerate(lines[1:], 1):  # Skip header
            parts = line.strip().split(',')
            
            if len(parts) < 15:  # Ensure we have enough columns
                continue
                
            # Extract data based on position (claims.csv structure)
            claim_id = parts[0] if len(parts) > 0 else ""
            user_id = parts[1] if len(parts) > 1 else ""
            user_phone = parts[8] if len(parts) > 8 and parts[8] != '' and parts[8] != 'nan' else ""
            garage_id = parts[10] if len(parts) > 10 and parts[10] != '' and parts[10] != 'nan' else ""
            agent_id = parts[11] if len(parts) > 11 and parts[11] != '' and parts[11] != 'nan' else ""
            garage_city = parts[12] if len(parts) > 12 and parts[12] != '' and parts[12] != 'nan' else ""
            
            # Count patterns for collusion detection
            if user_phone:
                phone_claims = [claim_id]
                alerts.append({
                    "type": "Mobile Number Reuse",
                    "severity": "Medium",
                    "description": f"Mobile {user_phone} used in claims",
                    "claims": phone_claims[:5],
                    "count": 1
                })
            
            if garage_id and agent_id:
                alerts.append({
                    "type": "Garage-Agent Pair",
                    "severity": "Medium",
                    "description": f"Garage {garage_id} + Agent {agent_id} combination",
                    "claims": [claim_id],
                    "count": 1
                })
        
        # Sort by severity and count
        severity_order = {"High": 3, "Medium": 2, "Low": 1}
        alerts.sort(key=lambda x: (severity_order.get(x["severity"], 0), x["count"]), reverse=True)
        
        return alerts[:10]  # Return top 10 alerts
        
    except Exception as e:
        print(f"Error getting collusion alerts: {e}")
        return []