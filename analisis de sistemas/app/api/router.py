from fastapi import APIRouter
from .routes import products, locations, stocks, movements

api_router = APIRouter()
api_router.include_router(products.router)
api_router.include_router(locations.router)
api_router.include_router(stocks.router)
api_router.include_router(movements.router)
