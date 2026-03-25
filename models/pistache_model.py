
from pydantic import BaseModel, ConfigDict

class pistache_input_model(BaseModel):
    """
    Model Parameters that predict the farmer cluster segmentation

    """
    gender: int
    clm_client: int
    seed_price: float
    prep_plow: float
    plant: float
    labor: float
    weed: float
    harvest_labor: float
    marmites_harvested: float

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "clm_client": 0,
                    "gender": 1,
                    "harvest_labor": 400,
                    "labor": 400,
                    "marmites_harvested": 91,
                    "plant": 500,
                    "prep_plow": 1000,
                    "seed_price": 5000,
                    "weed": 350
                },
                {
                    "clm_client": 0,
                    "gender": 0,
                    "harvest_labor": 250,
                    "labor": 250,
                    "marmites_harvested": 110,
                    "plant": 375,
                    "prep_plow": 750,
                    "seed_price": 5000,
                    "weed": 1250
                }
            ]
        }
    )

