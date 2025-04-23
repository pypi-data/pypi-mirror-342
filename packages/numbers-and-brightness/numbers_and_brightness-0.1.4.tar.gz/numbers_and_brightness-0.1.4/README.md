# Numbers-and-brightness
Numbers and brightness analysis for microscopic image analysis implemented in python.

Functions both as a python package and command-line tool.

## Installation
Numbers and brightness can be installed as follows:
```shell
pip install numbers_and_brightness
```

## Usage
### Python package
Numbers and brightness can be used as follows:

```python
from numbers_and_brightness.numbers_and_brightness import numbers_and_brightness_analysis
numbers_and_brightness_analysis(file = "./Images/image.tif")
```

Or in batch processing mode:

```python
from numbers_and_brightness.numbers_and_brightness import numbers_and_brightness_batch
numbers_and_brightness_batch(folder = "./Images")
```

### Command line
The package can also be accessed using the command line:

```shell
C:\Users\User> numbers_and_brightness --file "Images/image.tif"
C:\Users\User> numbers_and_brightness --folder "Images"
```

### Graphical user interface
The package contains a GUI that can be accessed as follows:
#### Python
```python
from numbers_and_brightness.gui import nb_gui
nb_gui()
```

#### Command line
```shell
C:\Users\User> numbers_and_brightness
```

#### Desktop shortcut
Additionally, a desktop (and start menu) shortcut can be created using the following command:
```shell
C:\Users\User> numbers_and_brightness --shortcut
```

![](./assets/images/gui.png)

### Parameters
The package contains the following parameters. These parameters can be altered by passing the parameter to the function, or to the cli as '--parameter'

- background : int, default = 0
    - background noise in the signal. Will be included in the calculations as $k_0$ as described by Digman et al., 2008.
- segment : bool, default = False
    - perform automatic segmentation of the cells using cellpose
- diameter : int, default = 75
    - expected diameter of the cell, passed to cellpose model
- flow_threshold : float, default = 0.4
    - flow threshold, passed to cellpose model
-  cellprob_threshold : float, default = 4
    - cellprob threshold, passed to cellpose model
- analysis : bool, default = False
    - perform analysis by plotting intensity of cell against apparent brightness
- erode : int, default = 2
    - erode the edges of the cell mask to ensure only pixels inside the cell are used for the analysis
- bleach_corr : bool, default = False
    - perform bleaching correction on the input image before analysis
    - bleach correction is performed by fitting a linear formula to the intensity over time, which is then used to correct the intensity

#### Examples:
```shell
C:\Users\User> numbers_and_brightness --folder "Images" --analysis true
```
```python
from numbers_and_brightness.numbers_and_brightness import numbers_and_brightness_batch
numbers_and_brightness_batch(folder = "./Images", analysis = True)
```
## Core calculations
All calculations are derived from Digman et al., 2008.

Here `img` represents a numpy array of shape  `(t, y, x)`.

#### Intensity
Intensity is calculated as:<br>

$$\langle k \rangle = \frac{\sum_i k_i}{K}$$

In python:
```python
average_intensity = np.mean(img, axis=0)
```
#### Variance
Variance is calculated as:<br>

$$\sigma^2 = \frac{\sum_i (k_i - \langle k \rangle)^2}{K}$$

In python:
```python
variance = np.var(img, axis=0)
```
#### Apparent brightness
Apparent brightness is calculated as:<br>

$$B = \frac{\sigma^2}{\langle k \rangle}$$

In python:
```python
apparent_brightness = variance / average_intensity
```
#### Apparent number
Apparent number is calculated as:<br>

$$N = \frac{\langle k \rangle^2}{\sigma^2}$$

In python:
```python
apparent_number = average_intensity**2 / variance
```
#### Brightness
Brightness is calculated as:<br>

$$\varepsilon = \frac{\sigma^2 - \langle k \rangle}{\langle k \rangle - k_0}$$

In python:
```python
brightness = (variance - average_intensity) / (average_intensity - background)
```
#### Number
Number is calculated as:<br>

$$n = \frac{(\langle k \rangle - k_0)^2}{\sigma^2 - \langle k \rangle}$$

In python:
```python
number = ((average_intensity-background)**2) / np.clip((variance - average_intensity), 1e-6, None)
```
Here the denominator is clipped (limited) to a value of 1e-6 to prevent extremely high number values.

## Output
For each image, the package generates a new folder containing extensive output:<br>

![](./assets/images/output.png)

## Examples:

![](./assets/images/number.png)

![](./assets/images/eroded_mask.png)

### Automatic batch processing
![](./assets/images/output_csv.png)

### Interactive data inspection
![](./assets/images/brightness_x_intensity.png)
