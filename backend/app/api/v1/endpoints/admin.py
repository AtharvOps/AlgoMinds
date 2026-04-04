from fastapi import APIRouter
import pandas as pd
import os
from datetime import datetime, timedelta
from services.graph_service import get_collusion_alerts

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats():
    try:
        # Read claims data
        if os.path.exists("database/claims.csv"):
            df = pd.read_csv("database/claims.csv")
        else:
            # Return mock data if no database exists
            return {
                "totalClaims": 0,
                "approvalRate": 0.0,
                "fraudScore": 0.0,
                "pendingClaims": 0
            }
        
        # Calculate stats
        total_claims = len(df)
        
        # Calculate approval rate (non-fraudulent claims)
        if 'is_fraud' in df.columns:
            approved_claims = len(df[df['is_fraud'] == 0])
            approval_rate = (approved_claims / total_claims * 100) if total_claims > 0 else 0
            fraud_claims = len(df[df['is_fraud'] == 1])
            fraud_score = (fraud_claims / total_claims * 100) if total_claims > 0 else 0
        else:
            approval_rate = 75.0  # Default mock value
            fraud_score = 25.0
        
        # Pending claims (mock - you can implement status tracking)
        pending_claims = max(0, total_claims // 10)  # Rough estimate
        
        return {
            "totalClaims": total_claims,
            "approvalRate": round(approval_rate, 1),
            "fraudScore": round(fraud_score, 1),
            "pendingClaims": pending_claims
        }
    
    except Exception as e:
        return {"error": str(e)}

@router.get("/claims")
def get_claims_data():
    try:
        if os.path.exists("database/claims.csv"):
            df = pd.read_csv("database/claims.csv")
        else:
            return {
                "fraudData": [{"name": "Genuine", "value": 0, "color": "#10b981"}, 
                              {"name": "Fraud", "value": 0, "color": "#ef4444"}],
                "monthlyData": [],
                "suspiciousClaims": [],
                "userTable": []
            }
        
        # Prepare fraud distribution data
        if 'is_fraud' in df.columns:
            genuine_count = len(df[df['is_fraud'] == 0])
            fraud_count = len(df[df['is_fraud'] == 1])
        else:
            genuine_count, fraud_count = 100, 30  # Mock data
        
        fraud_data = [
            {"name": "Genuine", "value": genuine_count, "color": "#10b981"},
            {"name": "Fraud", "value": fraud_count, "color": "#ef4444"}
        ]
        
        # Prepare monthly data (mock - you can implement proper date parsing)
        monthly_data = [
            {"month": "Jan", "genuine": 85, "fraud": 15},
            {"month": "Feb", "genuine": 92, "fraud": 18},
            {"month": "Mar", "genuine": 78, "fraud": 22},
            {"month": "Apr", "genuine": 88, "fraud": 20},
            {"month": "May", "genuine": 95, "fraud": 25},
            {"month": "Jun", "genuine": 102, "fraud": 28}
        ]
        
        # Prepare suspicious claims (high fraud score claims)
        suspicious_claims = []
        if 'fraud_score' in df.columns and len(df) > 0:
            high_risk = df[df['fraud_score'] > 180].head(4)
            for _, claim in high_risk.iterrows():
                suspicious_claims.append({
                    "id": claim.get('claim_id', f'CLM-{claim.name}'),
                    "user": claim.get('user_id', 'Unknown'),
                    "amount": claim.get('claim_amount', 0),
                    "risk": "High",
                    "reason": "High fraud score detected"
                })
        else:
            # Mock suspicious claims
            suspicious_claims = [
                {"id": "CLM-1234", "user": "John Doe", "amount": 45000, "risk": "High", "reason": "Unusual claim pattern"},
                {"id": "CLM-1235", "user": "Jane Smith", "amount": 32000, "risk": "Medium", "reason": "Inconsistent damage report"}
            ]
        
        # Prepare user table data
        user_table = []
        if len(df) > 0:
            sample_claims = df.head(6)
            for _, claim in sample_claims.iterrows():
                fraud_score = claim.get('fraud_score', 50)
                if fraud_score > 180:
                    risk_level = "High"
                    status = "Fraud"
                elif fraud_score > 100:
                    risk_level = "Medium"
                    status = "Under Review"
                else:
                    risk_level = "Low"
                    status = "Genuine"
                
                user_table.append({
                    "name": claim.get('user_id', f'User-{claim.name}'),
                    "claimAmount": claim.get('claim_amount', 0),
                    "riskLevel": risk_level,
                    "status": status
                })
        else:
            # Mock user table
            user_table = [
                {"name": "John Doe", "claimAmount": 45000, "riskLevel": "High", "status": "Fraud"},
                {"name": "Jane Smith", "claimAmount": 32000, "riskLevel": "Medium", "status": "Under Review"}
            ]
        
        return {
            "fraudData": fraud_data,
            "monthlyData": monthly_data,
            "suspiciousClaims": suspicious_claims,
            "userTable": user_table
        }
    
    except Exception as e:
        return {"error": str(e)}