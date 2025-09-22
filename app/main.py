from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.database import Base, engine
from app.controller import productController, userController
from app.controller import cartController
from app.controller import reviewController
from app.controller import orderController

# Initialize app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers and pass get_db
app.include_router(productController.router, prefix="/products", tags=["Products"])
app.include_router(userController.router, prefix="/users", tags=["Users"])
app.include_router(cartController.router, prefix="/cart", tags=["Cart"])
app.include_router(reviewController.router,prefix="/reviews",tags=["Reviews"] )
app.include_router(orderController.router, prefix="/orders",tags=["Orders"])
