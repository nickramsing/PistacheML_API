from fastapi import APIRouter, Request, HTTPException
from models.pistache_model import pistache_input_model
from services.predict_ag_model import predict_ag_model
import numpy as np
from log_writer.logger import get_logger
#instantiate module level logger
logger = get_logger(__name__)
router = APIRouter()

# Define the prediction endpoint using a POST request
@router.post("/predict")
def predict_cluster(input_data: pistache_input_model):
    '''
    Receives a pistache input model data and returns identified cluster
        manages input from User/system
        sends data to services.predict cluster for evaluation
    :param input_data:
    :return: predicted cluster
    '''
    try:
        logger.info(f"Receiving data from User/system... ")
        logger.info(f"input data parameters: {input_data}")
        # Convert input Pydantic model data to a numpy array for the ML model
        features = np.array([
            [input_data.gender,
             input_data.clm_client,
             input_data.seed_price,
             input_data.prep_plow,
             input_data.plant,
             input_data.labor,
             input_data.weed,
             input_data.harvest_labor,
             input_data.marmites_harvested
             ]
        ])

        logger.info(f"Requesting a prediction based on input data... ")
        prediction = predict_ag_model(data_params=features)
        logger.info(f"Predicted cluster: {prediction}")

        #todo: store input data and predicted cluster -- JSON or small database
        # only storing to log file at this time
        logger.info(f"HOW DEAL WITH SESSIONS: input data: {input_data} cluster: {prediction}")

        # Return the result as a JSON response
        logger.info(f"Responding with model prediction... ")
        return {"prediction": prediction}
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e}")
        raise HTTPException(status_code=500, detail=str(e))