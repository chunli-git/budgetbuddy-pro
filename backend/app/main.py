from fastapi import FastAPI

app = FastAPI(title="BudgetBuddy Pro API")

@app.get("/")
def root():
    return {"message": "BudgetBuddy Pro API is running"}