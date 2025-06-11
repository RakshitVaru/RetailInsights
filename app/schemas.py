from pydantic import BaseModel

class SaleSchema(BaseModel):
    item: str
    category: str
    revenue: float
    quantity: int
