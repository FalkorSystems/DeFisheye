# DeFisheye

Remove the Fisheye from a video, using OpenCV camera calibrations

# Version 0.1.0

# Release Notes

## <Date>: Initial release

# General notes

* Camera calibrations are stored in the ```config/``` directory
* On Linux we write OGG files
* On Mac we write AVI files
* If you would like an additional calibration that we don't already have, please ask
* If you'd like to calibrate a camera yourself, use XXXX

# Usage
```
usage: defisheye [-h] [-c CALIBRATION] [--gui] [input] [output]

positional arguments:
  input                 Input Video
  output                Output Video

optional arguments:
  -h, --help            show this help message and exit
  -c CALIBRATION, --calibration CALIBRATION
                        Calibration File
  --gui                 QT GUI Mode

Video Correction Tool
```

# Mac Instructions

## Install Python

http://www.python.org/download/releases/2.7.3/

## Then PySide and Qt

http://qt-project.org/wiki/PySide_Binaries_MacOSX

## Then using Homebrew, install ffmpeg and opencv

```bash
brew install x264
brew install ffmpeg
brew install opencv
```

## Now install pyyaml and py2app
```bash
sudo pip install pyyaml
curl -O http://peak.telecommunity.com/dist/ez_setup.py
sudo python ez_setup.py -U setuptools


hg clone https://bitbucket.org/ronaldoussoren/py2app
cd py2app
hg checkout branch-0.7
patch < ../patches/py2app.patch
cd ..
sudo pip install -e py2app
```

## Make the mac app
```bash
./tools/makemacapp.sh
```
