import pickle
import joblib
from fastapi import HTTPException

from log_writer.logger import get_logger
#instantiate module level logger
logger = get_logger(__name__)

'''
Load the saved model globally when the app starts
Avoids reloading the model for every request, improving performance

:param: ML model file
:outcome: ML model file loaded in app memory
'''

try:
    logger.info(f"Loading ML model... ")
    ag_model = joblib.load(filename='models/ag_model.pkl')
    #todo: consider file management of pkl file:
    #todo: use config file for name of file. use date and versioning to manage which file to use.
    #todo: include this in the README.md file as it concerns model management and versioning
    logger.info(f"ML model loaded... ")
except RuntimeError as re:
    logger.error(f"EXCEPTION: RuntimeError: Model file not found! Execute train_model.py first.  {re}")
    raise RuntimeError("Model file not found! Please run train_model.py first.")
except Exception as e:
    logger.error(f"EXCEPTION OCCURRED:  {e}")
    raise e


def predict_ag_model(data_params):
    '''
    Predicts the model outcome for the given data parameters

    :param: data_params
    :return: prediction
    '''
    try:
        # Make a prediction
        logger.info(f"Attempting to predict a cluster based on model... ")
        logger.info(f"Data parameters: {data_params}")
        prediction = ag_model.predict(data_params)
        #return prediction
        logger.info(f"Prediction: {prediction.tolist()}")
        return int(prediction[0])
    except RuntimeError as re:
        logger.error(f"EXCEPTION: RuntimeError: Model file not found! Execute train_model.py first.  {re}")
        raise RuntimeError("Model file not found! Please run train_model.py first.")
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e}")
        raise HTTPException(status_code=500, detail=str(e))


def provide_insight(predicted_cluster):
    try:
        logger.info(f"Cluster identified: Providing known insight... ")
        #todo: Create meaningful text insight to share: what does this mean?
        #todo: Create JSON model to hold current model's 1) clusters,
        #   2) characteristics of cluster, and
        #   3) recommended action
        return "No insight yet!"
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e}")
        raise e

