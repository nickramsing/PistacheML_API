from datetime import datetime
from pathlib import Path
from typing import Dict, List
import json
import joblib
from fastapi import HTTPException
from services.manage_model_config_params import load_model_configs, load_model_config_recommendation
from log_writer.logger import get_logger
#instantiate module level logger
logger = get_logger(__name__)

#==================================
# Load prediction model into memory
#  Start
#===================================
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
ag_model = load_ag_model(model_file=load_model_configs())

#==================================
# Load prediction model into memory
#  End
#===================================

def predict_ag_model(data_params) -> dict:
    '''
    Predicts the model outcome for the given data parameters

    :param: data_params
    :return: prediction package as a Dict - formated in provide_recommendation()
    '''
    try:
        # Make a prediction
        logger.info(f"Attempting to predict a cluster based on model... ")
        logger.info(f"Data parameters: {data_params}")
        prediction = ag_model.predict(data_params)
        #return prediction
        logger.info(f"Prediction: {prediction.tolist()}")
        response = provide_recommendation(predicted_cluster=prediction,
                                          data_params=data_params)
        #return int(prediction[0])
        return response
    except RuntimeError as re:
        logger.error(f"EXCEPTION: RuntimeError: Model file not found! Execute train_model.py first.  {re}")
        raise RuntimeError("Model file not found! Please run train_model.py first.")
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e}")
        raise HTTPException(status_code=500, detail=str(e))


#==================================
# Load RECOMMENDATION insight into memory
#  Start
#===================================
def load_recommendation_model(model_file: Path) -> dict:
    '''
    Load the saved RECOMMENDATIONS  globally when the app starts
    Avoids reloading the model for every request, improving performance

    :param: Recommendation insights file
    :outcome: Dictionary with Recommendation insights loaded in app memory
    '''
    try:
        logger.info(f"Loading RECOMMENDATIONS insights model... ")
        with open(model_file, 'r') as file:
            recommendation_model = json.load(file)
        logger.info(f"ML RECOMMENDATIONS insights loaded... ")
        return recommendation_model
    except RuntimeError as re:
        logger.error(f"EXCEPTION: RuntimeError: RECOMMENDATION Insights file not found! Ensure file is loaded.  {re}")
        raise RuntimeError("RECOMMENDATION Insights file not found! Please load the file and check the run model_config.yaml file.")
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e}")
        raise e

### Obtain the Recommendation model file
recommendation_model = load_recommendation_model(model_file=load_model_config_recommendation())

#==================================
# Load RECOMMENDATION insight into memory
#  End
#===================================

def provide_recommendation(predicted_cluster: List,
                           data_params: Dict) -> dict:
    '''
    Provides the model recommendations based on the identified cluster
        uses the recommendation JSON file to identify cluster descriptions and recommendations

    :params:
        predicted_cluster: Cluster identified by the prediction model - from predict_ag_model()
        data_params: not used here, but passed to be part of the formatted response
    :return: prediction package as a Dict - formated in construct_response()
    '''
    try:
        logger.info(f"Cluster identified: Providing known insight... ")
        #todo: catch: if list is more than ONE item!!  Raise Exception and log
        cluster = int(predicted_cluster[0])
        cluster_info = next((rec for rec in recommendation_model if rec["cluster"] == cluster), None)
        if cluster_info:
            response = construct_response(success=True,
                                          data_params=data_params,
                                          predicted_cluster=cluster,
                                          cluster_recs=cluster_info)
        else:
            response = construct_response(success=False,
                                          data_params=None,
                                          predicted_cluster=None,
                                          cluster_recs=None)
        #todo: store in db
        return response
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e}")
        raise HTTPException(status_code=500, detail=str(e))

def construct_response(success: bool,
                       data_params: Dict,
                       predicted_cluster: int,
                       cluster_recs: Dict) -> dict:
    '''
    Formats the model response recommendations based supplied parameters
    Created as separate function to allow for flexibility in model adaptation

    :params:
        success: bool - determines what is constructed in the response
        data_params: passed to be part of the formatted response
        predicted_cluster: passed to be formatted in the response
        cluster_recs: passed to be formatted in the response

    :return: prediction package as a Dict - formated response
    '''
    try:
        logger.info(f"Constructing recommendation response... ")
        if success:
            response = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "data_received": data_params,
                    "cluster_identified": predicted_cluster,
                    "cluster_description": cluster_recs["description"],
                    "cluster_recommendations": cluster_recs["recommendations"]
            }
        else:
            response = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data_received": data_params,
                "cluster_identified": None,
                "cluster_description": "no cluster identified - outside cluster scope",
                "cluster_recommendations": "no cluster recommendations"
            }
        logger.info(f"Formatted response: {response} ")
        return response
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e}")
        raise HTTPException(status_code=500, detail=str(e))
