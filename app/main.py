from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.auth import schema

from app.auth.router import router as auth_router
from app.properties.router import router as property_router
from app.auctions.router import router as auction_router
# from app.homeloan.router import router as loan_router
# from app.email.router import router as email_router
from app.lead.router import router as leads
from app.config import env, fastapi_config
from app.database import engine

app = FastAPI(**fastapi_config)


@app.on_event("shutdown")
def shutdown_db_client():
    engine.dispose()


app.add_middleware(
    CORSMiddleware,
    allow_origins=env.CORS_ORIGINS,
    allow_methods=env.CORS_METHODS,
    allow_headers=env.CORS_HEADERS,
    allow_credentials=True,
)

schema.Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/accounts", tags=["Auth"])
app.include_router(property_router,prefix="/properties", tags=["Properties"])
app.include_router(auction_router,prefix="/auctions", tags=["Auctions"])
# app.include_router(loan_router,prefix="/loan", tags=["Loans"])
# app.include_router(leads, prefix="/leads", tags=["Leads"])
# app.include_router(email_router, prefix="/email", tags=["Email"])