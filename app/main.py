# app/main.py
from fastapi import FastAPI
import os
from app.routes import recipe, locality, recommend, auth, mcp  # <-- absolute import

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
app.include_router(mcp.router)

print("✨ Desi Food MCP server is running... Visit /docs for API documentation.")

@app.get("/")
def root():
    return {"message": "Desi Food MCP is running!"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))  # Railway assigns PORT dynamically
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
