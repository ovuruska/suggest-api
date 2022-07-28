
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("DEBUG",False)
    if debug:
        uvicorn.run("app:app", host="0.0.0.0", port=port, log_level="info",reload=True)
    else:
        uvicorn.run("app:app", host="0.0.0.0", port=port, log_level="info")