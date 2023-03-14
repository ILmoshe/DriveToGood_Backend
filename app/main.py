"""
Main module for interaction with the app
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("core.server.app:app", host="0.0.0.0", log_level="info", reload=True, workers=4)
