<!-- This file is a placeholder for customizing description of your plugin 
on the napari hub if you wish. The readme file will be used by default if
you wish not to do any customization for the napari hub listing.

If you need some help writing a good description, check out our 
[guide](https://github.com/chanzuckerberg/napari-hub/wiki/Writing-the-Perfect-Description-for-your-Plugin)
-->

# Apple Tree Segmentation

A tool for apple tree segmentation using MOLMO and Segment Anything Model 2. This tool support images in png and jpg format. Segmentation masks could be corrected using annotation tools.

Image processing method is divided in two parts :
1- MOLMO detect tree based on foliage
2- Based on this detection, SAM2 label tree

This napari plugin was generated with copier using the napari-plugin-template.

## Installation

## Usage

## License & Attribution

This project integrates code from
- SAM2 by Meta
- MOLMO from AllenAI
