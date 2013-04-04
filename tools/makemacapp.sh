#!/bin/sh
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
#  * Neither the name of I Heart Engineering, Falkor Systems, nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
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

# Clean
sudo rm -rf build dist

# Make app
python setup.py py2app 

cd dist

# Sign
codesign --force --verify --verbose \
    --sign "3rd Party Mac Developer Application" \
    --entitlements ../DeFisheye.entitlements \
    DeFisheye.app

codesign --force --verify --verbose \
  --sign "3rd Party Mac Developer Application" \
  --entitlements ../DeFisheye.entitlements \
  DeFisheye.app/Contents/Frameworks/Python.framework/Versions/2.7

codesign --force --verify --verbose \
  --sign "3rd Party Mac Developer Application" \
  --entitlements ../DeFisheye.entitlements \
  DeFisheye.app/Contents/MacOS/python

codesign -vvv -d DeFisheye.app

productbuild \
    --component DeFisheye.app \
    /Applications \
    --sign "3rd Party Mac Developer Installer" \
    DeFisheye.pkg

# Test
sudo installer -store -pkg DeFisheye.pkg -target /
