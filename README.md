# NDVI Image Processing

This repository contains a Python-based implementation for processing and analyzing NDVI (Normalized Difference Vegetation Index) images. NDVI is widely used in remote sensing to assess vegetation health by analyzing satellite or aerial imagery.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Introduction
NDVI is calculated using the formula:
\[
NDVI = \frac{(NIR - RED)}{(NIR + RED)}
\]
Where:
- **NIR**: Near-Infrared band values
- **RED**: Red band values

This project automates the calculation of NDVI values from input images, visualizes the results, and provides insights into vegetation density.

## Features
- **NDVI Calculation**: Automatically compute NDVI values from input images.
- **Visualization**: Generate color-mapped NDVI images to highlight vegetation health.
- **Batch Processing**: Handle multiple images simultaneously.
- **Customizable**: Easy to modify and extend for specific use cases.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.7 or higher
- pip package manager

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Preyapradhan/NDVI_Image_Processing.git
   cd NDVI_Image_Processing
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Command-Line Usage
1. Prepare your input images (e.g., satellite images with NIR and RED bands).
2. Run the NDVI processing script:
   ```bash
   python ndvi_processing.py --input "path/to/images" --output "path/to/save/results"
   ```
3. View the processed images in the specified output directory.

### Script Example
Here is an example of how to use the script programmatically:
```python
from ndvi_processor import calculate_ndvi, visualize_ndvi

# Load NIR and RED band images
nir_image = "path/to/nir_image.tif"
red_image = "path/to/red_image.tif"

# Calculate NDVI
ndvi_image = calculate_ndvi(nir_image, red_image)

# Visualize and save
visualize_ndvi(ndvi_image, output_path="path/to/output.png")
```

## File Structure
```
NDVI_Image_Processing/
├── data/                # Example input data (NIR and RED band images)
├── results/             # Output directory for processed NDVI images
├── ndvi_processing.py   # Main script for NDVI computation
├── ndvi_processor.py    # Module containing core processing functions
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── LICENSE              # License information
```

## Examples
Here are some example outputs:
- Input: Satellite image bands (NIR and RED)
- Output: NDVI visualization highlighting vegetation density

![image](https://github.com/user-attachments/assets/89520e70-6183-4251-be2f-1dac26a61a5a)


![image](https://github.com/user-attachments/assets/5928f81d-1363-4abb-923d-006257f9742d)








