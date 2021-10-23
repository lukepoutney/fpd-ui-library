variables = {}
checkboxes = {}
graphs = {}


import sys
print(sys.version)
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["PYTHONUNBUFFERED"] = "TRUE"
try:
    os.chdir("fpdui")
except:
    pass
try:
    os.chdir("saved files")
except:
    pass
from functools import partial

import numpy as np
import scipy as sp
import h5py
import pickle

import fpd
from fpd.fpd_file import MerlinBinary, DataBrowser
import fpd.fpd_processing as fpdp

print('fpd package version:', fpd.__version__)

from tkinter import filedialog
from tkinter import *

import matplotlib
import matplotlib.pylab as plt
import matplotlib.image as mplimg
from matplotlib import cm
from matplotlib.widgets import RectangleSelector
from matplotlib.widgets import Slider
import matplotlib.pyplot as mplplt

from fpd.synthetic_data import disk_image, poisson_noise, shift_array, shift_im, shift_images, fpd_data_view

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


from settings import *
from save_page import *
save_page = Save_page()

from options import *

from ransac_tools import *

from dpc_explorer_class import DPC_Explorer
from consoledirector import *

from ui_functions import *
from file_functions import *
from browse_functions import *
from dpc_functions import *
from df_functions import *

from start_page import *
import ctypes

import sys
