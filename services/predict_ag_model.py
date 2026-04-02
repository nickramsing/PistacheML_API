import pickle
from pathlib import Path

import joblib
from fastapi import HTTPException

from log_writer.logger import get_logger
#instantiate module level logger
logger = get_logger(__name__)

try:
    import yaml
except ImportError:
    raise ImportError("PyYAML is required to read the ag model files. Be sure PyYAML is installed and loaded.")

#todo: config file to load: model_file from the configuration file
#todo: use config file for name of file. use date and versioning to manage which file to use.
model_file="models/files/ag_model_2026-03-28.pkl"


def load_ag_model(model_file: Path):
    '''
    Load the saved model globally when the app starts
    Avoids reloading the model for every request, improving performance

    :param: ML model file
    :outcome: ML model file loaded in app memory
    '''
    try:
        logger.info(f"Loading ML model... ")
        ag_model = joblib.load(model_file)
        logger.info(f"ML model loaded... ")
        return ag_model
    except RuntimeError as re:
        logger.error(f"EXCEPTION: RuntimeError: Model file not found! Execute train_model.py first.  {re}")
        raise RuntimeError("Model file not found! Please run train_model.py first.")
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e}")
        raise e

### Obtain the ag_model
ag_model = load_ag_model(model_file=model_file)




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

