# Time-lapse with Python and OpenCV

Take photos from an IP or web camera to create a time-lapse (or a stop motion animation).

Use `capture.py` to connect and take pictures from a camera. Use `render.py` to
create a video from these pictures.

## Requirements

* Python 3
* OpenCV package for python (https://pypi.org/project/opencv-python/)

## capture.py

Opens a video stream to capture a sequence of images.

Usage: `capture.py [-h] [-d DEVICE] [-o DIR]`

**Options**
* `-d DEVICE, --device DEVICE` camera index or IP
* `-o DIR, --output DIR` output directory

By default `capture` will open the first connected camera. If you want to open a different
camera use the `-d, --device` option. It accepts an IP or a device index (0 by default):

* Open Wi-Fi camera: `capture.py -d http://192.168.1.3:4747/video`
* Open second camera: `capture.py -d 1`

`capture` will create a folder in the current directory with the format `YYYYMMDD_HHMMS`
to store the pictures. You could also specify a custom directory using the
`-o, --output` option:

* Save frames to _my-project/_ folder: `python capture.py -o my-project`

The frames will be saved as `000001.jpg`, `000002.jpg`, `000003.jpg`... etc. If
you specify an existing directory with the `-o, --output` option, and this directory
contains a sequence like this, it will start to count from the last frame taken,
this is useful to restore previous sessions.

After the camera is initialized a new window will open showing the camera
input. In this window you can perform the following actions:

**Controls**

* _S_ key to start a time-lapse. This will take a picture automatically in a given
interval (defaults to 30s). Press again to stop.
* _A_ key to decrease the interval.
* _D_ key to increase the interval.
* _C_ key to take a single shot.
* _Q_ key to exit.

Adjust the interval before starting a time-lapse.

## render.py

Creates a video from a sequence of images.

Usage: `render.py [-h] [-f FPS] [-s WIDTH HEIGHT] directory filename`

**Arguments**

* `directory` directory containing a sequence of images (000001.jpg, 000002.jpg...)
* `filename` output video file

**Options**
* `-f FPS, --fps FPS` video frame rate (default: 30fps)
* `-s WIDTH HEIGHT, --size WIDTH HEIGHT` video width and height (default: 640x480)
