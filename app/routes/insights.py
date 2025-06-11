from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Base, Sale
from app.crud import create_sale, get_total_revenue, get_all_sales, get_sales_by_category
from app.schemas import SaleSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import io

router = APIRouter()

DATABASE_URL = "sqlite:///./retail.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        required_columns = {"item", "category", "revenue", "quantity"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail="Missing required columns")

        for _, row in df.iterrows():
            create_sale(db, row.to_dict())

        return {"message": "Data uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sales/total")
def total_revenue(db: Session = Depends(get_db)):
    total = get_total_revenue(db)
    return {"total_revenue": sum([x[0] for x in total])}

@router.get("/sales/top-items")
def top_items(db: Session = Depends(get_db)):
    result = get_all_sales(db)
    df = pd.DataFrame(result, columns=["item", "revenue"])
    top = df.groupby("item").sum().sort_values("revenue", ascending=False).head(10).reset_index()
    return top.to_dict(orient="records")

@router.get("/sales/by-category")
def sales_by_category(db: Session = Depends(get_db)):
    result = get_sales_by_category(db)
    df = pd.DataFrame(result, columns=["category", "revenue"])
    summary = df.groupby("category").sum().reset_index()
    return summary.to_dict(orient="records")