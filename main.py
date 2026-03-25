from fastapi import FastAPI
from routers import ag_model_pistache
import uvicorn
from log_writer.logger import get_logger
#instantiate module level logger
logger = get_logger(__name__)
app = FastAPI()

def configure_router(app: FastAPI):
    try:
        app.include_router(ag_model_pistache.router)
        logger.info(f"router configured successfully")
        return True
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e}")
        return False



if __name__ == '__main__':
    if not configure_router(app):
        raise Exception("Configure FastAPI router failed. Cannot launch app")
    logger.info(f"Loading application...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

