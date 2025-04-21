import configparser


CONST_PATH = r"\\bodit-analysis\FarmersHands\fh-data-analysis-constants.ini"

config = configparser.ConfigParser()

try:
    config.read(CONST_PATH, encoding='utf-8')
except Exception as e:
    print("Unauthorized usage.")
    raise e


""" Base path """
BASEPATH_RAWDATA = config['Paths'].get('BASEPATH_RAWDATA')
BASEPATH_FEATURE = config['Paths'].get('BASEPATH_FEATURE')
BASEPATH_LABEL = config['Paths'].get('BASEPATH_LABEL')
BASEPATH_MODEL = config['Paths'].get('BASEPATH_MODEL')
BASEPATH_FEATLIST = config['Paths'].get('BASEPATH_FEATLIST')
BASEPATH_PRED = config['Paths'].get('BASEPATH_PRED')
BASEPATH_TAG = config['Paths'].get('BASEPATH_TAG')
BASEPATH_PREDTAG = config['Paths'].get('BASEPATH_PREDTAG')


""" Prefix """
PREFIX_RAWDATA = config['Prefix'].get('PREFIX_RAWDATA')
PREFIX_TAG = config['Prefix'].get('PREFIX_TAG')
PREFIX_PREDTAG = config['Prefix'].get('PREFIX_PREDTAG')
PREFIX_FEAT = config['Prefix'].get('PREFIX_FEAT')
PREFIX_LABEL_STATE = config['Prefix'].get('PREFIX_LABEL_STATE')
PREFIX_LABEL_SITSTAND = config['Prefix'].get('PREFIX_LABEL_SITSTAND')
PREFIX_PRED = config['Prefix'].get('PREFIX_PRED')
PREFIX_POST = config['Prefix'].get('PREFIX_POST')


""" fhBasic """
SECTION_TABLE_PATH = config['fhBasic'].get('SECTION_TABLE_PATH')


""" fhRawdata """
ACCEL_SENSITIVITY = config['fhRawdata'].getint('ACCEL_SENSITIVITY')
GYRO_SENSITIVITY = config['fhRawdata'].getfloat('GYRO_SENSITIVITY')
SAMPLE_RATE = config['fhRawdata'].getint('SAMPLE_RATE')

SAMPLE_INTERVAL = config['fhRawdata'].getfloat('SAMPLE_INTERVAL')
ADJUST_FACTOR = config['fhRawdata'].getint('ADJUST_FACTOR')

RAWDATA_INPUT_SIZE = config['fhRawdata'].getint('RAWDATA_INPUT_SIZE')
WINDOW_SHAPE = config['fhRawdata'].get('WINDOW_SHAPE')
WINDOW_SIZE = config['fhRawdata'].getint('WINDOW_SIZE')

""" fhDatabase """
REGION = config['fhDatabase'].get('REGION')
SECRET_NAME = config['fhDatabase'].get('SECRET_NAME')
DB_NAME = config['fhDatabase'].get('DB_NAME')
SERVICE_NAME = config['fhDatabase'].get('SERVICE_NAME')

""" fhFeature """
ACCEL_SENSITIVITY = config['fhFeature'].getint('ACCEL_SENSITIVITY')
GYRO_SENSITIVITY = config['fhFeature'].getfloat('GYRO_SENSITIVITY')

HEADING_PEAK_HEIGHT = config['fhFeature'].getfloat('HEADING_PEAK_HEIGHT')
HEADING_PEAK_DISTANCE = config['fhFeature'].getint('HEADING_PEAK_DISTANCE')
HEADING_WINDOW_LEFT_GAP = config['fhFeature'].getint('HEADING_WINDOW_LEFT_GAP')
HEADING_WINDOW_RIGHT_GAP = config['fhFeature'].getint('HEADING_WINDOW_RIGHT_GAP')

COUGH_MIN_PEAK_HEIGHT = config['fhFeature'].getfloat('COUGH_MIN_PEAK_HEIGHT')
COUGH_MAX_PEAK_HEIGHT = config['fhFeature'].getfloat('COUGH_MAX_PEAK_HEIGHT')
COUGH_PEAK_DISTANCE = config['fhFeature'].getint('COUGH_PEAK_DISTANCE')

COUGH_GNORM_LOW_THR = config['fhFeature'].getint('COUGH_GNORM_LOW_THR')
COUGH_GNORM_HIGH_THR = config['fhFeature'].getint('COUGH_GNORM_HIGH_THR')

COUGH_WINDOW_LEFT_SIZE = config['fhFeature'].getint('COUGH_WINDOW_LEFT_SIZE')
COUGH_WINDOW_RIGHT_SIZE = config['fhFeature'].getint('COUGH_WINDOW_RIGHT_SIZE')

QUAT_BETA = config['fhFeature'].getfloat('QUAT_BETA')
QUAT_INIT_COUNT = config['fhFeature'].getint('QUAT_INIT_COUNT')

FILTER_ORDER = config['fhFeature'].getint('FILTER_ORDER')
FILTER_CUT_OFF_FREQ = config['fhFeature'].getint('FILTER_CUT_OFF_FREQ')

SAMPLE_RATE = config['fhFeature'].getint('SAMPLE_RATE')
COUGH_FEATURE_SIZE = config['fhFeature'].getint('COUGH_FEATURE_SIZE')
COUGH_PEAK_INDEX = config['fhFeature'].getint('COUGH_PEAK_INDEX')