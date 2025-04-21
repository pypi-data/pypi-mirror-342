# stpp_tplot

Simple time series plotting library based on pyspedas and matplotlib.

## Overview

`stpp_tplot` is a Python library that provides convenient functions for plotting time series data, especially for space physics data processed by `pyspedas`. It simplifies the creation of publication-quality plots with features like:

* Multiple panel plots with shared x-axis
* Spectrogram plots with colorbar
* Orbit parameter labels panel
* Customizable plot options

## Installation

```bash
pip install stpp_tplot
```
## Usage
### Plotting with default options: mp
```python
from stpp_tplot import mp, sd, op, xlim
from pyspedas.erg import pwe_ofa, mgf, orb

# Load data
trange = ['2017-03-27', '2017-03-28']
pwe_ofa(trange=trange)
mgf(trange=trange)
orb(trange=trange)

# Plot data
mp(['erg_pwe_ofa_l2_spec_B_spectra_132', 'erg_mgf_l2_mag_8sec_sm'], var_label='erg_orb_l2_pos_rmlatmlt')
```
![alt text](images/image.png)

If you do not need the orbit parameter labels, var_label can be set to None.

```python
mp(['erg_pwe_ofa_l2_spec_B_spectra_132', 'erg_mgf_l2_mag_8sec_sm'], var_label=None)
```
![alt text](images/image-3.png)

### Saving plot: mp(save_path='path')
```python
mp(['erg_pwe_ofa_l2_spec_B_spectra_132', 'erg_mgf_l2_mag_8sec_sm'], var_label='erg_orb_l2_pos_rmlatmlt', save_path='my_plot.png')
```

### Setting the time range: mp(tr=time_range), or xlim(time_range)
```python
time_range = ['2017-03-27T21:00:00', '2017-03-27T21:30:00']
mp(['erg_pwe_ofa_l2_spec_B_spectra_132', 'erg_mgf_l2_mag_8sec_sm'], var_label='erg_orb_l2_pos_rmlatmlt', tr=time_range)
```
or
```python
xlim(time_range)
mp(['erg_pwe_ofa_l2_spec_B_spectra_132', 'erg_mgf_l2_mag_8sec_sm'], var_label='erg_orb_l2_pos_rmlatmlt')
```
![alt text](images/image-13.png)

### Plotting with custom options: op & mp
```python
op('erg_pwe_ofa_l2_spec_B_spectra_132', ylog=0, zlog=1, z_range=[1e-4, 1e2], colormap='viridis')
mp(['erg_pwe_ofa_l2_spec_B_spectra_132'], var_label=None)
```
![alt text](images/image-4.png)

Following are the available options for the `op` function:
 * y_label: y axis label (str, optional)
 * ylog: y axis type (bool, optional)
 * y_range: y axis range (list, optional)
 * y_sublabel: axis subtitle (str, optional)
 * zlog: z axis type (bool, optional)
 * z_range: z axis range (list, optional)
 * z_label: z axis label (str, optional)
 * z_sublabel: axis subtitle (str, optional)
 * spec: spectrogram (0 or 1, optional)
 * colormap: colormap (list, optional)
 * legend_names: legend names (list, optional)
 * line_color: line color (str, optional)
 * line_width: line width (int, optional)
 * line_style: line style (str, optional)

Following are the available options for the `mp` function:
 * plot_title: plot title (str, optional)
 * plot_title_fontsize: plot title font size (int, optional)
 * display: display (bool, optional), if False, the plot will not be displayed
 * save_path: save path (str, optional), if provided, the plot will be saved to the specified path
 * hspace: height space between panels (float, optional)
 * y_tick_step: vertical spacing of the orbit tick marks
 * orb_label_height: height of the orbit parameter labels

### Storing Data: sd
```python
from pyspedas import data_quants
import numpy as np
magt = data_quants['erg_mgf_l2_magt_8sec']
electron_mass = 9.1094e-31
electron_charge = 1.602e-19
fc = 1 / (2*np.pi) * electron_charge * magt * 1e-9 / electron_mass * 1e-3
sd('fc', data={'x': magt.time, 'y':fc})
sd('05fc', data={'x': magt.time, 'y':fc*0.5})
op('fc', line_color='black')
op('05fc', line_color='red')
mp('fc')
```
![alt text](images/image-7.png)

### Overplotting
Give the list of variables to be overplotted as a list of lists.
```python
mp([['fc', '05fc']])
```
![alt text](images/image-8.png)

```python
mp([['fc', 'erg_pwe_ofa_l2_spec_B_spectra_132'], 'fc'], var_label='erg_orb_l2_pos_rmlatmlt')
```
![alt text](images/image-12.png)

### mp options
 * yauto(bool): if True, the y axis range will be set automatically
 * zauto(bool): if True, the z axis range will be set automatically