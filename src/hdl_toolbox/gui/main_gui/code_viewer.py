""" This file is part of the HDL Toolbox distribution (https://github.com/m47812/hdl_toolbox).
Copyright (c) 2024 Robin Müller.

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>. """

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget

from PyQt6.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt6.QtCore import QRegularExpression

class HDLHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("blue"))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        keyword_patterns = ["\\bentity\\b", "\\bis\\b", "\\bend\\b", "\\bport\\b", "\\bmap\\b", "\\bcomponent\\b",
                    "\\bmodule\\b", "\\binput\\b", "\\boutput\\b", "\\binout\\b", "\\bwire\\b",
                    "\\breg\\b", "\\bassign\\b", "\\balways\\b", "\\bposedge\\b", "\\bnegedge\\b",
                    "\\bif\\b", "\\belse\\b", "\\bcase\\b", "\\bendcase\\b", "\\bfor\\b", "\\bwhile\\b",
                    "\\bfunction\\b", "\\bendfunction\\b", "\\btask\\b", "\\bendtask\\b", "\\bbegin\\b",
                    "\\bend\\b", "\\blogic\\b", "\\binteger\\b", "\\bgenvar\\b", "\\bparameter\\b",
                    "\\blocalparam\\b", "\\bgenerate\\b", "\\bgenvar\\b", "\\bfor\\b", "\\bendgenerate\\b",
                    "\\binput\\b", "\\boutput\\b", "\\binout\\b", "\\bassign\\b", "\\bwire\\b",
                    "\\breg\\b", "\\balways\\b", "\\bposedge\\b", "\\bnegedge\\b", "\\bif\\b",
                    "\\belse\\b", "\\bcase\\b", "\\bendcase\\b", "\\bfor\\b", "\\bwhile\\b",
                    "\\bfunction\\b", "\\bendfunction\\b", "\\btask\\b", "\\bendtask\\b", "\\bbegin\\b",
                    "\\bend\\b", "\\blogic\\b", "\\binteger\\b", "\\bgenvar\\b", "\\bparameter\\b",
                    "\\blocalparam\\b", "\\bgenerate\\b", "\\bgenvar\\b", "\\bfor\\b", "\\bendgenerate\\b", "\\bsignal\\b", "\\bconstant\\b", "\\battribute\\b"]

        self.highlighting_rules = [(QRegularExpression(pattern), keyword_format) for pattern in keyword_patterns]

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)


class CodeViewer(QMainWindow):
    def __init__(self, name, text, parent):
        super().__init__(parent)

        self.setWindowTitle("Code Viewer: " + name)
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)
        highlighter = HDLHighlighter(self.text_edit.document())
        self.text_edit.setReadOnly(True)

        # Set the longer text
        self.text_edit.setPlainText(text)

        # Add a button to copy the content to clipboard
        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.setGeometry(10, 10, 150, 30)
        layout.addWidget(self.copy_button)
        self.copy_button.clicked.connect(self.copy_to_clipboard)

        # Create a QWidget, set its layout, and set it as the central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())