from sqlalchemy.orm import Session
from app.models import Sale

def create_sale(db: Session, sale_data: dict):
    sale = Sale(**sale_data)
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale

def get_total_revenue(db: Session):
    return db.query(Sale).with_entities(Sale.revenue*Sale.quantity).all()

def get_all_sales(db: Session):
    return db.query(Sale.item, Sale.revenue*Sale.quantity).all()

def get_sales_by_category(db: Session):
    return db.query(Sale.category, Sale.revenue*Sale.quantity).all()
