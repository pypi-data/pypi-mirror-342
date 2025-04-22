# get the version
from importlib.metadata import version
__version__ = version('deepGreen')
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from . import utils
from . import vsl
from .model import GrowthModel
from .data import Dataset
from .trainer import Trainer
from .predictor import Predictor
