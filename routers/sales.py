from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from services.db import get_db
from models.sale import Sale, SaleCreate, SaleInDb

router = APIRouter(prefix='/sales', tags=['sales'])

@router.post('/', response_model=dict)
async def create_sales(sales_in: List[SaleCreate], db: Session = Depends(get_db)):
    try:
        db_sales = [Sale(**sale.model_dump()) for sale in sales_in]
        db.add_all(db_sales)
        db.commit()
        return {"message": "Продажи успешно добавлены", "sales": len(db_sales)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка при сохранении: {str(e)}")

@router.get("/", response_model=List[SaleInDb])
async def list_sales(
    marketplace: Optional[str] = Query(None, description="Фильтр по маркетплейсу"),
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    date_from: Optional[date] = Query(None, description="Начало периода"),
    date_to: Optional[date] = Query(None, description="Конец периода"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(20, ge=1, le=100, description="Размер страницы"),
    db: Session = Depends(get_db)
):
    query = db.query(Sale)
    if marketplace:
        query = query.filter(Sale.marketplace == marketplace)
    if status:
        query = query.filter(Sale.status == status)
    if date_from:
        query = query.filter(Sale.sold_at >= date_from)
    if date_to:
        query = query.filter(Sale.sold_at <= date_to)
    sales = query.offset((page - 1) * page_size).limit(page_size).all()
    return sales
