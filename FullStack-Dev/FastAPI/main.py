import uvicorn
from app.app import app

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=8000, workers=1, reload=True)