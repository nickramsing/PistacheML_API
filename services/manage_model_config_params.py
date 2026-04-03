from os import supports_dir_fd
from pathlib import Path
try:
    import yaml
except ImportError:
    raise ImportError("PyYAML is required to read the ag model files. Be sure PyYAML is installed and loaded.")
from log_writer.logger import get_logger
#instantiate module level logger
logger = get_logger(__name__)
'''
Purpose: holds functions to load the model config files
file location should be: /models/files/
'''

data_folder = Path(__file__).resolve().parent.parent / "models" / "files"
model_config_path = data_folder / "model_config.yaml"

def _load_config(config_path: Path) -> dict:
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def load_model_configs() -> Path:
    if not model_config_path.exists():
        logger.error(f"EXCEPTION: RuntimeError: model config file not found! load model_config.yaml first.")
        raise FileNotFoundError(f"Model config file not found at {model_config_path}")
    try:
        config = _load_config(model_config_path)

        model_file = config.get("model_file", "models/files/ag_model_2026-03-28.pkl")
        model_file = Path(__file__).resolve().parent.parent / model_file
        return model_file
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e}")
        raise e

def load_model_config_recommendation() -> Path:
    if not model_config_path.exists():
        logger.error(f"EXCEPTION: RuntimeError: model config file not found! load model_config.yaml first.")
        raise FileNotFoundError(f"Model config file not found at {model_config_path}")
    try:
        config = _load_config(model_config_path)

        rec_file = config.get("recommendation_file", "models/files/ag_model_action_2026-03-28.json")
        rec_file = Path(__file__).resolve().parent.parent / rec_file
        return rec_file
    except Exception as e:
        logger.error(f"EXCEPTION OCCURRED:  {e}")
        raise e