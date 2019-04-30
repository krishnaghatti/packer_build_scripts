<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [packer-templates](#packer-templates)
- [Purpose](#purpose)
- [Requirements](#requirements)
  - [Software](#software)
- [Usage](#usage)
- [License](#license)
- [Inspiration](#inspiration)
- [Author Information](#author-information)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


## packer-templates
The images to be built and all the related files should be in each of its folder. The build file's name should be `baseAmi.json`

## Purpose
The `build_script.py` script builds from either the given folder or builds all of the images from the folders. As of now the templates only build AWS specific AMIs.
This repository can be used for building various cloud images using [Packer](https://www.packer.io).

## Requirements

### Software

- [Packer](https://www.packer.io)
- python 3.7 or above (the script uses fstrings)

## Usage
To build specific AMI:
```python3 build_script.py build_specific --ami_to_build ubuntu1604```
To build all:
```python3 build_script.py build_all```
To get the current available AMIs:
```python3 build_script.py get_all_ami_ids```

## License

## Inspiration

The folder structure and python script are inspired by the repo : https://github.com/mrlesmithjr/packer-templates and I have modified them to suit my requirement.

## Author Information
