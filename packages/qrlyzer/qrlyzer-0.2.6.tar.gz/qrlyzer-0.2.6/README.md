# qrlyzer 
[![CI](https://github.com/netlifeas/qrlyzer/actions/workflows/CI.yml/badge.svg)](https://github.com/netlifeas/qrlyzer/actions/workflows/CI.yml) [![Tests](https://github.com/netlifeas/qrlyzer/actions/workflows/tests.yml/badge.svg)](https://github.com/netlifeas/qrlyzer/actions/workflows/tests.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qrlyzer?link=https%3A%2F%2Fpypi.org%2Fproject%2Fqrlyzer%2F) [![Sigstore Signed](https://img.shields.io/badge/signed%20with-sigstore-4b8bbe?logo=sigstore&logoColor=white)](https://github.com/netlifeas/qrlyzer/releases)


qrlyzer is a lightweight Python module for reading QR codes from images. It offers an optional auto-resizing feature that leverages fast_image_resize to utilize SIMD instructions for enhanced performance.

## Getting Started

### Installing

qrlyzer is available on PyPi. Install it with:

```bash
python -m pip install qrlyzer
```

### Basic usage:

#### Detecting QR codes from an image file

```python
import qrlyzer

# From path
qr_codes = qrlyzer.detect_and_decode("my_image.jpg")
print(f"Found QR codes: {qr_codes}")
```
#### Detecting QR codes from image bytes
```python
# From bytes
from PIL import Image
im = Image.open("my_image.jpg")
im = im.convert("L")
qr_codes = qrlyzer.detect_and_decode_from_bytes(im.to_bytes(), im.width, im.height)
print(f"Found QR codes: {qr_codes}")
```

#### Using auto-resizing
Pass the ```auto_resize``` parameter to enable automatic resizing (from 100px to 1280px in the largest direction. 5 steps). These dimensions seem to be a good detection range for the libraries used.
```python
# Auto-scaling
qrlyzer.detect_and_decode("my_image.jpg", auto_resize=True)
```
Note: This can in some cases increase accuracy as well as speed, especially for large images where there is a QR code. If an image does not contain a QR code or the QR code is unreadable it will be slower.

## Uses 

* [maturin](https://www.maturin.rs/) - Build & PyO3 bindings
* [rqrr](https://github.com/WanzenBug/rqrr/) - Reading QR codes
* [rxing](https://github.com/rxing-core/rxing/) - Reading QR codes
* [fast_image_resize](https://github.com/cykooz/fast_image_resize/) - Image resizing 

## Authors

* **Nikolai Ugelvik** - *Initial work* - [NikolaiUgelvik](https://github.com/NikolaiUgelvik)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Thanks to all the contributors to the maturin, rqrr, rxing & fast_image_resize projects.

