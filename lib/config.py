import os
from pathlib import Path

APP_PATH = os.path.abspath(os.path.join(Path(__file__).resolve().parent, '../'))
CAMPAIGN_PATH = Path(os.path.join(APP_PATH, 'campaign'))
SRC_PATH = Path(os.path.join(APP_PATH, 'src'))
