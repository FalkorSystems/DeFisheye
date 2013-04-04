#!/usr/bin/python
# -*- coding: utf-8 -*-
# Software License Agreement (BSD License)
#
# Copyright (c) 2013, I Heart Engineering, Falkor Systems, Inc.
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
#  * Neither the name of I Heart Engineering nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
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

import platform

if (platform.system() == "Darwin"):
    from setuptools import setup

    APP = ['defisheye']
    DATA_FILES = ['config']
    OPTIONS = {'argv_emulation': True,
               'packages': 'PySide,yaml',
               'includes': 'cv,cv2',
               'argv_inject': '--gui',
               'iconfile': 'pixmaps/defisheye.icns',
               'plist': {
                   'CFBundleIdentifier': 'com.falkorsystems.defisheye',
                   'CFBundleName': 'DeFisheye',
                   'CFBundleVersion': '0.1.0',
                   'CFBundleShortVersionString': '0.1.0',
                   'CFBundleDocumentTypes': [ { 'CFBundleTypeName': 'MP4' } ],
                   'LSApplicationCategoryType': 'public.app-category.video',
               }
    }

    setup(
        name='DeFisheye',
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

else:
    from distutils.core import setup
    setup(name = "defisheye",
        version = "0.0.1",
        description = "Fisheye Distortion Removal Tool",
        author = "I Heart Engineering",
        author_email = "code@iheartengineering.com",
        url = "http://www.iheartengineering.com",
        license = "BSD-3-clause",
        scripts = ["defisheye"],
        data_files=[('/usr/share/applications', ["DeFisheye.desktop"]),
                    ('/usr/share/defisheye/config',["config/gp_h3_720p.yml"]),
                    ('/usr/share/defisheye/config',["config/gp_h3_960p.yml"]),
                    ('/usr/share/icons/hicolor/scalable/apps',
                        ["pixmaps/defisheye.svg"]),
                    ('/usr/share/icons/hicolor/128x128/apps',
                        ["pixmaps/128x128/defisheye.png"]),
                    ('/usr/share/icons/hicolor/64x64/apps',
                        ["pixmaps/64x64/defisheye.png"]),
                    ('/usr/share/icons/hicolor/32x32/apps',
                        ["pixmaps/32x32/defisheye.png"]),
                    ('/usr/share/icons/hicolor/16x16/apps',
                        ["pixmaps/16x16/defisheye.png"]),
                   ],
        long_description = """This tool remove distortion from videos shot with a fisheye lens.""" 
        #classifiers = []     
    ) 
