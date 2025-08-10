# app/main.py
from fastapi import FastAPI
from routes import recipe, locality, recommend

app = FastAPI(
    title="Desi Food Finder MCP",
    description="MCP server for Puch AI WhatsApp food bot",
    version="1.0.0"
)

# Register routes
app.include_router(recipe.router)
app.include_router(locality.router)
app.include_router(recommend.router)

@app.get("/")
def root():
    return {"message": "Desi Food Finder MCP is running!"}
