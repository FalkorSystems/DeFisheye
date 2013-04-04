#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Software License Agreement (BSD License)
#
# Copyright (c) 2013, I Heart Engineering
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of I Heart Engineering, nor Falkor Systems, nor
#    the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

import sys
import os
import yaml
import platform
import argparse
import subprocess
from PySide import QtGui, QtCore
import cv2
import numpy
import time

class State:
    INPUT = 0
    PROCESS = 1
    SUCCESS = 2
    END = 3
    current = INPUT

class gui(QtGui.QWidget):
    def __init__(self):
        super(gui, self).__init__()
        self.setGeometry(300, 300, 600, 150)
        self.setWindowTitle('DeFisheye')   
        self.state = "ACTIVE"

        self.layout = QtGui.QGridLayout()

        self.camera_label = QtGui.QLabel("Camera: ")

        self.camera_combo = QtGui.QComboBox()
        self.camera_combo.activated.connect(self.combo_activated)

        self.layout.addWidget(self.camera_label, 0, 0)
        self.layout.addWidget(self.camera_combo, 0, 1, 1, 2)

        self.active_calibration = None
        self.calibration = []

        self.input_label = QtGui.QLabel("Input Video: ")
        self.input_file = QtGui.QLineEdit()
        self.input_file.setMinimumWidth(240)
        self.input_file.setMaximumWidth(1024)
        self.input_button = QtGui.QPushButton("...")
        self.input_button.setMinimumWidth(24)
        self.input_button.setMaximumWidth(24)
        self.input_button.clicked.connect(self._input_dialog)

        self.layout.addWidget(self.input_label, 2, 0);
        self.layout.addWidget(self.input_file, 2, 1);
        self.layout.addWidget(self.input_button, 2, 2);

        self.output_label = QtGui.QLabel("Output Video: ")
        self.output_file = QtGui.QLineEdit()
        self.output_file.setMinimumWidth(240)
        self.output_file.setMaximumWidth(1024)
        self.output_button = QtGui.QPushButton("...")
        self.output_button.setMinimumWidth(24)
        self.output_button.setMaximumWidth(24)
        self.output_button.clicked.connect(self._output_dialog)

        self.layout.addWidget(self.output_label, 3, 0);
        self.layout.addWidget(self.output_file, 3, 1,);
        self.layout.addWidget(self.output_button, 3, 2);

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addLayout(self.layout)
        self.vbox.addSpacing(12)
        self.vbox.addStretch(1)

        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok
                                            | QtGui.QDialogButtonBox.Cancel);
        self.buttonBox.accepted.connect(self.process)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setAutoDefault(True)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDefault(True)
        self.buttonBox.rejected.connect(self.end)
        self.vbox.addWidget(self.buttonBox)

        self.setLayout(self.vbox)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setFocus()

    def end(self):
        if (State.current < State.SUCCESS):
            State.current = State.END
        self.buttonBox.close()
        self.close()
         
    def process(self):
        if not os.path.exists(self.input_file.text()):
            QtGui.QMessageBox.critical(None, self.tr("Error"), self.tr("Can not process video.\nInput file does not exists."))
        ext = os.path.splitext(self.output_file.text())[1]
        if (ext != ".ogv" and ext != ".avi"):
            QtGui.QMessageBox.critical(None, self.tr("Error"), self.tr("Can not process video.\nOutput file must be supported (*.avi or *.ogv) filetype."))
        print "Processing Video"
        print "================"
        print "Input File:  " + self.input_file.text()
        print "Output File: " + self.output_file.text()
        print "Calibration: " + self.active_calibration
        self.prog = QtGui.QProgressDialog("Processing Video", "Cancel", 0, 100, self)
        self.prog.setWindowTitle('DeFisheye')   
        self.prog.canceled.connect(self.end)
        self.prog.show()
        self.prog.setValue(0)
        defisheye(self.input_file.text(),self.output_file.text(),self.active_calibration,progress_gui,self)
        self.close()


    def combo_activated(self, value):
        self.active_calibration = self.calibration[value]
        print self.active_calibration

    def tag_constructor(self, loader, tag_suffix, node):
        return tag_suffix + ' ' + repr(node.value)

    def load_configs(self,dir):
        try:
            files = os.listdir(dir)
        except Exception, e:
            print e, ": Invalid directory"
            sys.exit(os.EX_OSFILE)

        for filename in files[:]:
            filepath = "%s/%s"%(dir,filename)
            print "Filepath: %s"%filepath
            yaml.add_multi_constructor('', self.tag_constructor)
            try:
                cfg = yaml.load(file(filepath, 'r'))
            except yaml.YAMLError, e:
                print "ERROR: configuration file:", e
            self.camera_combo.addItem(u'%s    [ %s ]'%(cfg['camera_name'],cfg['camera_mode']))
            self.calibration.append(filepath)

    def _input_dialog(self):
        filename, filter = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Input Video File', dir=os.getenv("HOME"), filter="Video (*.mp4)")
        if os.path.exists(filename):
            self.input_file.setText(filename)

    def _output_dialog(self):
        filename, filter = QtGui.QFileDialog.getSaveFileName(parent=self, caption='Output Video File', dir=os.getenv("HOME"), filter="Video (*.avi *.ogv)")
        #if os.path.exists(filename):
        self.output_file.setText(filename)

def defisheye_usage():
    print """DeFisheye - Video Rectification Tool
------------------------------------------------------------
usage: defisheye [--version] COMMAND [ARGS]"""
    sys.exit(os.EX_USAGE)

def progress_gui(gui,status):
    if (State.current >= State.SUCCESS):
        gui.prog.close()
        gui.close()
    else:
        gui.prog.setValue(int(status*100))
        QtGui.QApplication.processEvents()

def progress_text(status):
    global last_status
    try:
        last_status
    except:
        last_status = 0.0
        sys.stdout.write("Processing: [                    ]\rProcessing: [")
        sys.stdout.flush()
    if (status == 1.0):
        sys.stdout.write('.')
        print ""
    elif (status-last_status >= 0.05):
        sys.stdout.write('.')
        sys.stdout.flush()
        last_status = last_status + 0.05

def cvmat_constructor(loader, node):
    data = loader.construct_mapping(node,deep=True)
    matrix = cv2.cv.CreateMat(data['rows'], data['cols'], cv2.CV_32FC1)
    for r in range(data['rows']):
        for c in range(data['cols']):
            cv2.cv.SetReal2D(matrix, r, c, data['data'][c+r*data['cols']])
    return numpy.asarray(matrix)

def load_calibration(filename):
    yaml.add_constructor('tag:yaml.org,2002:opencv-matrix', cvmat_constructor)
    try:
        return yaml.load(file(filename, 'r'))
    except yaml.YAMLError, e:
        print "ERROR: configuration file:", e

def defisheye(input_filename,output_filename,calibration_filename,update=None,gui=None):
    cfg = load_calibration(calibration_filename)
    cameraMatrix = cfg["camera_matrix"]
    distCoeffs = cfg["distortion_coefficients"]
    imageSize = (cfg["image_width"],cfg["image_height"])

    video_in = cv2.VideoCapture(input_filename)
    video_frames = int(video_in.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    video_fps = video_in.get(cv2.cv.CV_CAP_PROP_FPS)
    video_width = int(video_in.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    video_height = int(video_in.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    print "Frames: " + str(video_frames)
    print "FPS: " + str(video_fps)
    print "Width: " + str(video_width)
    print "Height: " + str(video_height)

    if platform.system() == "Darwin":
        fourcc = cv2.cv.CV_FOURCC('F', 'M', 'P', '4')
    else:
        fourcc = cv2.cv.CV_FOURCC('T','H','E','O')

    video_out = cv2.VideoWriter(
        filename=output_filename,
        fourcc=fourcc,
        fps=video_fps,
        frameSize=(video_width,video_height),
        isColor=1)

    #(map1, map2) = cv2.initUndistortRectifyMap(cameraMatrix, distCoeffs, None, cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, imageSize, 0)[0], imageSize, cv2.CV_16SC2);
    (map1, map2) = cv2.initUndistortRectifyMap(numpy.asarray(cameraMatrix), numpy.asarray(distCoeffs), None, numpy.asarray(cameraMatrix), imageSize, cv2.CV_16SC2);

    for f in range(video_frames):
        if (gui != None):
            QtGui.QApplication.processEvents()
        if (State.current == State.END):
            break
        if (update != None):
            # pos = video_in.get(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO)
            pos = float(f)/video_frames
            if (gui != None):
                update(gui,pos)
            else:
                update(pos)

        image_in = video_in.read()[1]
        if image_in is None:
            print "Frame ", f, " end."
            break
        image_rect = cv2.remap(image_in, map1, map2, cv2.INTER_CUBIC)
        video_out.write(image_rect)
    if (State.current < State.SUCCESS):
        State.current = State.SUCCESS
    if (gui != None):
        update(gui,1)
        if (State.current == State.SUCCESS):
            QtGui.QMessageBox.information(None, "DeFisheye", "Processing completed.")
        QtGui.QApplication.processEvents()
    else:
        print ""
        print "Processing Completed."

################################
if __name__ == '__main__':
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os_name = platform.system()
    if (os_name != "Darwin" and os_name != "Linux"):
        print "Error: Unsupported System"
        sys.exit(os.EX_SOFTWARE)
    if (os_name == "Darwin"):
        config_dir = os.path.expanduser("%s/config"%(script_dir))
    if (os_name == "Linux"):
        config_dir = "/usr/share/defisheye/config"
        if not os.path.exists(config_dir):
            config_dir = os.path.expanduser("~/.defisheye")
            if not os.path.exists(config_dir):
                config_dir = os.path.expanduser("%s/config"%(script_dir))

    parser = argparse.ArgumentParser(prog='defisheye',epilog='Video Correction Tool')
    parser.add_argument('-c','--calibration', help='Calibration File', nargs=1, default=None)
    parser.add_argument('--gui', help='QT GUI Mode', action='store_true')
    parser.add_argument('input', help='Input Video', nargs='?')
    parser.add_argument('output', help='Output Video', nargs='?')
    args = parser.parse_args()

    print "DeFisheye"
    print "---------"

    if (args.gui == True or sys.stdout.isatty() == False):
        app = QtGui.QApplication(sys.argv)
        win = gui()
        if (args.input == None):
            input_filename, filter = QtGui.QFileDialog.getOpenFileName(parent=win, caption='Input Video File', dir=os.getenv("HOME"), filter="Video (*.mp4)")
            if os.path.exists(input_filename):
                win.input_file.setText(input_filename)
            print input_filename
        else:
            input_filename = os.path.abspath(os.path.expanduser(args.input))
            win.input_file.setText(input_filename)

        output_filename = os.path.splitext(input_filename)[0]
        if (input_filename != None and input_filename != ""):
            if (platform.system() == "Linux"):
                output_filename = output_filename + "-rect.ogv"
            else:
                output_filename = output_filename + "-rect.avi"
        else:
            output_filename = ""
        win.output_file.setText(output_filename)
        win.load_configs(config_dir)
        win.combo_activated(0)

        win.show()
        sys.exit(app.exec_())
    else:
        if (args.input == None):
            print "Error: Input file must be specified in CLI mode"
            sys.exit(os.EX_USAGE)
        input_filename = os.path.abspath(os.path.expanduser(args.input))
        if (args.output == None):
            output_filename = os.path.splitext(input_filename)[0]
            if (platform.system() == "Linux"):
                output_filename = output_filename + "-rect.ogv"
            else:
                output_filename = output_filename + "-rect.avi"
        else:
            output_filename = os.path.abspath(os.path.expanduser(args.output))
        if (args.calibration == None):
            print "Error: Calibration file must be specified in CLI mode"
            sys.exit(os.EX_USAGE)
        else:
            calibration_filename = os.path.abspath(os.path.expanduser(args.calibration[0]))
        print "Input:       " + input_filename
        print "Output:      " + output_filename
        print "Calibration: " + calibration_filename
        defisheye(input_filename,output_filename,calibration_filename,progress_text)
