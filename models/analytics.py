from pydantic import BaseModel
from typing import Dict, List, Optional

class AnalyticsSummaryItem(BaseModel):
    total_revenue: float
    total_cost: float
    gross_profit: float
    margin_percent: float
    total_orders: int
    avg_order_value: float
    return_rate: float

class AnalyticsSummaryResponse(BaseModel):
    summary: Dict[str, AnalyticsSummaryItem]

class TopProductItem(BaseModel):
    product_name: str
    revenue: float
    quantity: int
    profit: float

class TopProductsResponse(BaseModel):
    top_products: List[TopProductItem]
