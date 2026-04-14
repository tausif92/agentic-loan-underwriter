from fastapi import FastAPI
from backend.api.routes import application_routes
from backend.api.routes import application_routes, underwriting_routes


app = FastAPI()

app.include_router(application_routes.router)
app.include_router(underwriting_routes.router)


@app.get("/")
def health_check():
    return {"status": "Loan Underwriter API is running"}
