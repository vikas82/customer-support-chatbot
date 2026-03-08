from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict

app = FastAPI(title="Mock Support APIs")

# In-memory demo "database"
ORDERS: Dict[str, dict] = {
    "A1001": {"order_id": "A1001", "status": "In Transit", "eta_days": 2, "carrier": "BlueDart"},
    "A1002": {"order_id": "A1002", "status": "Delivered", "eta_days": 0, "carrier": "Delhivery"},
    "A1003": {"order_id": "A1003", "status": "Delayed", "eta_days": 5, "carrier": "EKart"},
    "A1004": {"order_id": "A1004", "status": "Processing", "eta_days": 7, "carrier": "FedEx"},
    "A1005": {"order_id": "A1005", "status": "Cancelled", "eta_days": None, "carrier": "UPS"},
    "A1006": {"order_id": "A1006", "status": "In Transit", "eta_days": 3, "carrier": "DHL"},
    "A1007": {"order_id": "A1007", "status": "Delivered", "eta_days": 0, "carrier": "India Post"},
}

REFUNDS: Dict[str, dict] = {
    "R2001": {"refund_id": "R2001", "status": "Processing", "timeline_days": 7},
    "R2002": {"refund_id": "R2002", "status": "Completed", "timeline_days": 0},
    "R2003": {"refund_id": "R2003", "status": "Initiated", "timeline_days": 10},
    "R2004": {"refund_id": "R2004", "status": "Rejected", "timeline_days": None},
    "R2005": {"refund_id": "R2005", "status": "Processing", "timeline_days": 5},
    "R2006": {"refund_id": "R2006", "status": "Completed", "timeline_days": 0},
    "R2007": {"refund_id": "R2007", "status": "Initiated", "timeline_days": 8},
}

class OrderRequest(BaseModel):
    order_id: str

class RefundRequest(BaseModel):
    refund_id: str


@app.post("/order")
def get_order(req: OrderRequest):
    if req.order_id not in ORDERS:
        return ORDERS
    return ORDERS.get(req.order_id, {"order_id": req.order_id, "status": "Not Found"})

@app.post("/refund")
def get_refund(req: RefundRequest):
    return REFUNDS.get(req.refund_id, {"refund_id": req.refund_id, "status": "Not Found"})
