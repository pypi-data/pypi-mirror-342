from .fhConst import (
    ACCEL_SENSITIVITY,
    GYRO_SENSITIVITY,
    HEADING_PEAK_HEIGHT,
    HEADING_PEAK_DISTANCE,
    HEADING_WINDOW_LEFT_GAP,
    HEADING_WINDOW_RIGHT_GAP,
    COUGH_MIN_PEAK_HEIGHT,
    COUGH_MAX_PEAK_HEIGHT,
    COUGH_PEAK_DISTANCE,
    COUGH_GNORM_LOW_THR,
    COUGH_GNORM_HIGH_THR,
    COUGH_WINDOW_LEFT_SIZE,
    COUGH_WINDOW_RIGHT_SIZE,
    QUAT_BETA,
    QUAT_INIT_COUNT,
    FILTER_ORDER,
    FILTER_CUT_OFF_FREQ,
    SAMPLE_RATE,
    COUGH_FEATURE_SIZE,
    COUGH_PEAK_INDEX
)

import os, importlib.util

pyd_path = r"\\bodit-analysis\FarmersHands\fh-module\fhFeatExtractModule.cp311-win_amd64.pyd"
if not os.path.isfile(pyd_path):
    raise ImportError("잘못된 접근입니다.")

spec = importlib.util.spec_from_file_location("fhFeatExtractModule", pyd_path)
_ext = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_ext)

for name, value in (
    ("ACCEL_SENSITIVITY", ACCEL_SENSITIVITY),
    ("GYRO_SENSITIVITY",  GYRO_SENSITIVITY),
    ("HEADING_PEAK_HEIGHT", HEADING_PEAK_HEIGHT),
    ("HEADING_PEAK_DISTANCE", HEADING_PEAK_DISTANCE),
    ("HEADING_WINDOW_LEFT_GAP", HEADING_WINDOW_LEFT_GAP),
    ("HEADING_WINDOW_RIGHT_GAP", HEADING_WINDOW_RIGHT_GAP),
    ("COUGH_MIN_PEAK_HEIGHT", COUGH_MIN_PEAK_HEIGHT),
    ("COUGH_MAX_PEAK_HEIGHT", COUGH_MAX_PEAK_HEIGHT),
    ("COUGH_PEAK_DISTANCE", COUGH_PEAK_DISTANCE),
    ("COUGH_GNORM_LOW_THR", COUGH_GNORM_LOW_THR),
    ("COUGH_GNORM_HIGH_THR", COUGH_GNORM_HIGH_THR),
    ("COUGH_WINDOW_LEFT_SIZE", COUGH_WINDOW_LEFT_SIZE),
    ("COUGH_WINDOW_RIGHT_SIZE", COUGH_WINDOW_RIGHT_SIZE),
    ("QUAT_BETA", QUAT_BETA),
    ("QUAT_INIT_COUNT", QUAT_INIT_COUNT),
    ("FILTER_ORDER", FILTER_ORDER),
    ("FILTER_CUT_OFF_FREQ", FILTER_CUT_OFF_FREQ),
    ("SAMPLE_RATE", SAMPLE_RATE),
    ("COUGH_FEATURE_SIZE", COUGH_FEATURE_SIZE),
    ("COUGH_PEAK_INDEX", COUGH_PEAK_INDEX)
):
    setattr(_ext, name, value)

def __getattr__(name):
    try:
        return getattr(_ext, name)
    except AttributeError:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

def __dir__():
    public = [n for n in dir(_ext) if not n.startswith("_")]
    return sorted(list(globals().keys()) + public)

__all__ = [n for n in dir(_ext) if not n.startswith("_")] + [
    "ACCEL_SENSITIVITY",
    "GYRO_SENSITIVITY",
    "HEADING_PEAK_HEIGHT",
    "HEADING_PEAK_DISTANCE",
    "HEADING_WINDOW_LEFT_GAP",
    "HEADING_WINDOW_RIGHT_GAP",
    "COUGH_MIN_PEAK_HEIGHT",
    "COUGH_MAX_PEAK_HEIGHT",
    "COUGH_PEAK_DISTANCE",
    "COUGH_GNORM_LOW_THR",
    "COUGH_GNORM_HIGH_THR",
    "COUGH_WINDOW_LEFT_SIZE",
    "COUGH_WINDOW_RIGHT_SIZE",
    "QUAT_BETA",
    "QUAT_INIT_COUNT",
    "FILTER_ORDER",
    "FILTER_CUT_OFF_FREQ",
    "SAMPLE_RATE",
    "COUGH_FEATURE_SIZE",
    "COUGH_PEAK_INDEX"
]
