# 1.0 Problem Domain
Building on the R generated pistache ML model
Make the prediction model useful in identifying cluster of new participating farmers

# 2.0 Solution Vision
- Host model as a referenced model
- Allow User/System to submit data via JSON (one farmer at a time)
- Evaluate the data and return the predicted cluster with additional insight

- Intended as a JSON solution from system, not from a USER input
  - modify the use cases to reflect "system"

# 3.0 Technical Solution
insert sequence diagram > here

## 3.1 Workflow
### Use Case: Predict based on system input
1. As a User/System, I want to submit input ag data and receive a model prediction based on the ML model so that I night identify the cluster to which the pistache farmer might belong  
   1. Predict endpoint (in /routers/ag_model_pistache.py) receives the input data
   2. validated with model
   3. passed to services/predict - identify cluster and return
   4. cluster identified and known insight added to response 
   4. returned to User/System with useful information
2. As a Modeller, I want to re-train the ML model so that the model remains up-to-date and relevant
   1. Obtain new data - ensure it conforms with data structure
   2. Run jupyter notebook or train_ML_mdoel.py to evaluate and generate a new model file
        - CAREFUL with .py file: will overwrite existing model. 
        - Need a routine to backup existing with date
        - Add model config YAML fie to identify which model version to use
   4. Run application and test to ensure the new model is loaded into the system and the system performs as expected

# 4.0 Outcomes
## 4.1 Learnings
