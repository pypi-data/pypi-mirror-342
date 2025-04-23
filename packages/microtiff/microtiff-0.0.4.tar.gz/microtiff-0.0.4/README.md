# microtiff
A Python module and CLI tool for converting proprietary microscopy formats to TIFF with JSON metadata sidecar files.

## Installation
Microtiff is installable via PIP:
```pip install microtiff```

## Supported data types
Both supported modules and modules working with errata are listed below.

| Sensor | Status | Errata/Notes |
| --- | --- | --- |
| Imaging FlowCytobot/IFCB (.adc, .hdr, .roi) | :white_check_mark: | |
| LISST-Holo (.pgm) | :white_check_mark: | Only extracts raw interference field, does not reconstruct images. Metadata export broken. |
| LISST-Holo2 (.pgm) | :white_check_mark: | See above |
| FlowCam | :x: | In active development |

## Dependencies
- pillow
- numpy

## Acknowledgements
Made with the help of: [Sari Giering](https://github.com/sarigiering), [Will Major](https://github.com/obg-wrm) and [Mojtaba Masoudi](https://github.com/Mojtabamsd)
