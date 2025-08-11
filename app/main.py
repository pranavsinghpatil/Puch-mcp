# app/main.py
from fastapi import FastAPI
from .routes import recipe, locality, recommend, auth

app = FastAPI(
    title="Desi Food MCP",
    description="MCP server for Puch AI WhatsApp food bot",
    version="1.0.0"
)

# Register routes
app.include_router(recipe.router)
app.include_router(locality.router)
app.include_router(recommend.router)
app.include_router(auth.router)

print("✨ Desi Food MCP server is running... Visit http://localhost:8000/docs for API documentation.")

@app.get("/")
def root():
    return {"message": "Desi Food MCP is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
