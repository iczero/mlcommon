import time
__startup_time = time.time()

import os
import pathlib

import numpy as np
import scipy
import torch
from torch import nn
import polars as pl
import matplotlib

def __do_init():
    ipy = get_ipython()

    # set up matplotlib integration
    if matplotlib.get_backend() == 'agg':
        # matplotlib probably did not find a display
        print('warning: matplotlib did not find a display')
        ipy.run_line_magic('matplotlib', 'inline')
    else:
        ipy.run_line_magic('matplotlib', 'qt6')

    if torch.cuda.is_available():
        torch.cuda.init()
        torch.set_default_device('cuda')
        # reserve some gpu memory
        torch.tensor(1)
    else:
        print('warning: torch reports gpu is not available')

    # display options
    np.set_printoptions(edgeitems=5)
    torch.set_printoptions(edgeitems=5)

    # run before cell executes
    prev_cols = 0
    def resize_if_needed(_info = None):
        nonlocal prev_cols
        cols = os.get_terminal_size().columns
        if cols != prev_cols:
            np.set_printoptions(linewidth=cols)
            torch.set_printoptions(linewidth=cols)
            prev_cols = cols

    ipy.events.register('pre_run_cell', resize_if_needed)

__do_init()

# late imports
import matplotlib.pyplot as plt

print(f'Initialized in {time.time() - __startup_time:.3f}s')
del __do_init, __startup_time
