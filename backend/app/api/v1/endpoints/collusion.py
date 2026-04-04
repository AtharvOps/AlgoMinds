from fastapi import APIRouter
from services.graph_service import get_collusion_alerts

router = APIRouter()

@router.get("/collusion-alerts")
def get_collusion_alerts_endpoint():
    try:
        alerts = get_collusion_alerts()
        return {"alerts": alerts}
    except Exception as e:
        return {"error": str(e)}
