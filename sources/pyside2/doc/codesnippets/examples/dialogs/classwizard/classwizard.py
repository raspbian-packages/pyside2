/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

//! [0] //! [1]
def __init__(self, parent):
    QWizard.__init__(self, parent):
    self.addPage(IntroPage())
    self.addPage(ClassInfoPage())
    self.addPage(CodeStylePage())
    self.addPage(OutputFilesPage())
    self.addPage(ConclusionPage())
//! [0]

    self.setPixmap(QWizard.BannerPixmap, QPixmap(":/images/banner.png"))
    self.setPixmap(QWizard.BackgroundPixmap, QPixmap(":/images/background.png"))

    self.setWindowTitle(self.tr("Class Wizard"))
//! [2]

//! [1] //! [2]

//! [3]
def accept(self):
//! [3] //! [4]
    className = self.field("className")
    baseClass = self.field("baseClass")
    macroName = self.field("macroName")
    baseInclude = self.field("baseInclude")

    outputDir = self.field("outputDir")
    header = self.field("header")
    implementation = self.field("implementation")
//! [4]

...

//! [5]
    QDialog.accept(self)
//! [5] //! [6]
}
//! [6]

//! [7]
class IntroPage (QWizardPage):

    def __init__(self, parent):
        QWizardPage.__init__(self, parent)

        self.setTitle(tr("Introduction"))
        self.setPixmap(QWizard.WatermarkPixmap, QPixmap(":/images/watermark1.png"))

        label = QLabel(self.tr("This wizard will generate a skeleton C++ class " \
                                    "definition, including a few functions. You simply " \
                                    "need to specify the class name and set a few " \
                                    "options to produce a header file and an " \
                                    "implementation file for your new C++ class."))
        label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
}
//! [7]

//! [8] //! [9]
class ClassInfoPage(QWizardPage):

    def __init__(self, parent):
        QWizardPage.__init__(self, parent)
//! [8]
        self.setTitle(self.tr("Class Information"))
        self.setSubTitle(self.tr("Specify basic information about the class for which you " \
                                 "want to generate skeleton source code files."))
        self.setPixmap(QWizard.LogoPixmap, QPixmap(":/images/logo1.png"))

//! [10]
        classNameLabel = QLabel(self.tr("&Class name:"))
        classNameLineEdit = QLineEdit()
        classNameLabel.setBuddy(classNameLineEdit)

        baseClassLabel = QLabel(self.tr("B&ase class:"))
        baseClassLineEdit = QLineEdit()
        baseClassLabel.setBuddy(baseClassLineEdit)

        qobjectMacroCheckBox = QCheckBox(self.tr("Generate Q_OBJECT &macro"))

//! [10]
        groupBox = QGroupBox(self.tr("C&onstructor"))
//! [9]

        qobjectCtorRadioButton = QRadioButton(self.tr("&QObject-style constructor"))
        qwidgetCtorRadioButton = QRadioButton(self.tr("Q&Widget-style constructor"))
        defaultCtorRadioButton = QRadioButton(self.tr("&Default constructor"))
        copyCtorCheckBox = QCheckBox(self.tr("&Generate copy constructor and operator="))

        defaultCtorRadioButton.setChecked(True)

        defaultCtorRadioButton.toggled[bool].connect(copyCtorCheckBox.setEnabled)

//! [11] //! [12]
        registerField("className*", classNameLineEdit)
        registerField("baseClass", baseClassLineEdit)
        registerField("qobjectMacro", qobjectMacroCheckBox)
//! [11]
        registerField("qobjectCtor", qobjectCtorRadioButton)
        registerField("qwidgetCtor", qwidgetCtorRadioButton)
        registerField("defaultCtor", defaultCtorRadioButton)
        registerField("copyCtor", copyCtorCheckBox)

        groupBoxLayout = QVBoxLayout()
//! [12]
        groupBoxLayout.addWidget(qobjectCtorRadioButton)
        groupBoxLayout.addWidget(qwidgetCtorRadioButton)
        groupBoxLayout.addWidget(defaultCtorRadioButton)
        groupBoxLayout.addWidget(copyCtorCheckBox)
        groupBox.setLayout(groupBoxLayout)

        layout = QGridLayout()
        layout.addWidget(classNameLabel, 0, 0)
        layout.addWidget(classNameLineEdit, 0, 1)
        layout.addWidget(baseClassLabel, 1, 0)
        layout.addWidget(baseClassLineEdit, 1, 1)
        layout.addWidget(qobjectMacroCheckBox, 2, 0, 1, 2)
        layout.addWidget(groupBox, 3, 0, 1, 2)
        self.setLayout(layout)
//! [13]

//! [13]

//! [14]
class CodeStylePage(QWizardPage):

    def __init__(self, parent):
        QWizardPage.__init__(self, parent)
        self.setTitle(tr("Code Style Options"))
        self.setSubTitle(tr("Choose the formatting of the generated code."))
        self.setPixmap(QWizard.LogoPixmap, QPixmap(":/images/logo2.png"))

        commentCheckBox = QCheckBox(self.tr("&Start generated files with a comment"))
//! [14]
        commentCheckBox.setChecked(True)

        protectCheckBox = QCheckBox(self.tr("&Protect header file against multiple " \
                                        "inclusions"))
        protectCheckBox.setChecked(True)

        macroNameLabel = QLabel(self.tr("&Macro name:"))
        macroNameLineEdit = QLineEdit()
        macroNameLabel.setBuddy(macroNameLineEdit)

        includeBaseCheckBox = QCheckBox(self.tr("&Include base class definition"))
        baseIncludeLabel = QLabel(self.tr("Base class include:"))
        baseIncludeLineEdit = QLineEdit()
        baseIncludeLabel.setBuddy(baseIncludeLineEdit)

        protectCheckBox.toggled[bool].connect(macroNameLabel.setEnabled)
        protectCheckBox.toggled[bool].connect(macroNameLineEdit.setEnabled)
        includeBaseCheckBox.toggled[bool].connect(baseIncludeLabel.setEnabled)
        includeBaseCheckBox.toggled[bool].connect(baseIncludeLineEdit.setEnabled)

        self.registerField("comment", commentCheckBox)
        self.registerField("protect", protectCheckBox)
        self.registerField("macroName", macroNameLineEdit)
        self.registerField("includeBase", includeBaseCheckBox)
        self.registerField("baseInclude", baseIncludeLineEdit)

        layout = QGridLayout()
        layout.setColumnMinimumWidth(0, 20)
        layout.addWidget(commentCheckBox, 0, 0, 1, 3)
        layout.addWidget(protectCheckBox, 1, 0, 1, 3)
        layout.addWidget(macroNameLabel, 2, 1)
        layout.addWidget(macroNameLineEdit, 2, 2)
        layout.addWidget(includeBaseCheckBox, 3, 0, 1, 3)
        layout.addWidget(baseIncludeLabel, 4, 1)
        layout.addWidget(baseIncludeLineEdit, 4, 2)
//! [15]
        self.setLayout(layout)
}
//! [15]

//! [16]
    def initializePage(self):
        className = self.field("className")
        self.macroNameLineEdit.setText(className.upper() + "_H")

        baseClass = self.field("baseClass")

        self.includeBaseCheckBox.setChecked(len(baseClass))
        self.includeBaseCheckBox.setEnabled(len(baseClass))
        self.baseIncludeLabel.setEnabled(len(baseClass))
        self.baseIncludeLineEdit.setEnabled(len(baseClass))

        if not baseClass:
            self.baseIncludeLineEdit.clear()
        elsif QRegExp("Q[A-Z].*").exactMatch(baseClass):
            baseIncludeLineEdit.setText("<" + baseClass + ">")
        else:
            baseIncludeLineEdit.setText("\"" + baseClass.lower() + ".h\"")
//! [16]

//! [17]
    def initializePage(self):
        className = field("className")
        self.headerLineEdit.setText(className.lower() + ".h")
        self.implementationLineEdit.setText(className.lower() + ".cpp")
        self.outputDirLineEdit.setText(QDir.convertSeparators(QDir.tempPath()))
//! [17]
