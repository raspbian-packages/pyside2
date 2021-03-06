#############################################################################
##
## Copyright (C) 2016 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the test suite of Qt for Python.
##
## $QT_BEGIN_LICENSE:GPL-EXCEPT$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3 as published by the Free Software
## Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_paths import init_test_paths
init_test_paths(False)

from helper.helper import adjust_filename
from helper.timedqapplication import TimedQApplication

from PySide2 import QtCore, QtGui, QtQuick

class ProxyObject(QtCore.QObject):
    def __init__(self):
        super(ProxyObject,self).__init__()
        self._o = None
        self._receivedName = ""

    @QtCore.Slot(result='QObject*')
    def getObject(self):
        if self._o:
            return self._o

        self._o = QtCore.QObject()
        self._o.setObjectName("PySideObject")
        return self._o

    @QtCore.Slot(str)
    def receivedObject(self, name):
        self._receivedName = name


class TestConnectionWithInvalidSignature(TimedQApplication):

    def testSlotRetur(self):
        view = QtQuick.QQuickView()
        proxy = ProxyObject()

        context = view.rootContext()
        context.setContextProperty("proxy", proxy)
        view.setSource(QtCore.QUrl.fromLocalFile(adjust_filename('bug_726.qml', __file__)))
        root = view.rootObject()
        button = root.findChild(QtCore.QObject, "buttonMouseArea")
        view.show()
        button.entered.emit()
        self.assertEqual(proxy._receivedName, "PySideObject")

if __name__ == '__main__':
    unittest.main()
