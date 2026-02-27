import os

_HOME_DIR_ABS_PATH = os.path.dirname(os.path.abspath(__file__))
_PROCESSED_DATA_ABS_PATH = os.path.abspath(os.path.join(_HOME_DIR_ABS_PATH, 'processed_data'))
_RAW_DATA_ABS_PATh = os.path.abspath(os.path.join(_HOME_DIR_ABS_PATH, 'raw_data'))