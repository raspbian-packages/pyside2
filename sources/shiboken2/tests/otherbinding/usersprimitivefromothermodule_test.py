#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

'''Tests user defined primitive type from a required module.'''

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shiboken_paths import init_paths
init_paths()
from other import Number

class UserDefinedPrimitiveTypeFromRequiredModuleTest(unittest.TestCase):

    def testUsersPrimitiveFromRequiredModuleAsArgument(self):
        '''static Number Number::fromComplex(Complex)'''
        cpx = complex(3.0, 1.2)
        number = Number.fromComplex(cpx)
        self.assertEqual(number.value(), int(cpx.real))

    def testUsersPrimitiveFromRequiredModuleAsReturnValue(self):
        '''Complex Number::toComplex()'''
        number = Number(12)
        cpx = number.toComplex()
        self.assertEqual(number.value(), int(cpx.real))

if __name__ == '__main__':
    unittest.main()
