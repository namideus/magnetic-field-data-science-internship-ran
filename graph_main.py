# Summer internship 2022
# Applied Mathematics and Informatics department, AUCA
#
# Created by: Yiman Altynbek uulu

import sys
import os  
import matplotlib
from pathlib import Path  
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from my_libs import *

# Matplotlib
class MplCanvas(FigureCanvasQTAgg):
	def __init__(self, parent=None, width=5, height=4, dpi=200):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		self.axes.set_xlabel('date', fontsize=15)
		self.axes.set_ylabel('T, nT', fontsize=15)
		super(MplCanvas, self).__init__(fig)

# PyQt GUI
class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("Internship 2022")

		self.canvas = MplCanvas(self, width=6, height=4, dpi=111)

		# Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
		self.toolbar = NavigationToolbar(self.canvas, self)

		# Open CSV button
		self.openCSVBtn = QtWidgets.QPushButton()
		self.openCSVBtn.setIcon(QtGui.QIcon('open_file.png'))
		self.openCSVBtn.setText("Open CSV file")
		self.openCSVBtn.setObjectName("openCSVBtn")
		self.openCSVBtn.clicked.connect(self.open_csv_file)

		# Open MAG button
		self.openMAGBtn = QtWidgets.QPushButton()
		self.openMAGBtn.setIcon(QtGui.QIcon('open_file.png'))
		self.openMAGBtn.setText("Open MAG file")
		self.openMAGBtn.setObjectName("openMAGBtn")
		self.openMAGBtn.clicked.connect(self.open_mag_file)

		# Interpolate button
		self.interpolateBtn = QtWidgets.QPushButton()
		self.interpolateBtn.setText("Interpolate")
		self.interpolateBtn.setObjectName("interpolateBtn")
		self.interpolateBtn.clicked.connect(self.interpolate)

		# Seasonal decompose button
		self.seasonDecomposeBtn = QtWidgets.QPushButton()
		self.seasonDecomposeBtn.setText("Seasonal decompose")
		self.seasonDecomposeBtn.setObjectName("seasonDecomposeBtn")
		self.seasonDecomposeBtn.clicked.connect(self.make_seasonal_decompose)

		# Seasonal decompose button
		self.saveCvsBtn = QtWidgets.QPushButton()
		self.saveCvsBtn.setText("Save as CVS")
		self.saveCvsBtn.setObjectName("saveCvsBtn")
		self.saveCvsBtn.clicked.connect(self.save_to_cvs)

		# Method options
		self.cbMethods = QtWidgets.QComboBox()
		self.cbMethods.addItems(["linear","quadratic","cubic","spline","polynomial"])

		# Order options
		self.cbOrders = QtWidgets.QComboBox()
		self.cbOrders.addItems(["1","2","3","4","5","6","7"])

		# Main layout
		mainLayout = QtWidgets.QHBoxLayout()

		# Options layout
		optionsLayout = QtWidgets.QVBoxLayout()
		optionsLayout.addWidget(self.openCSVBtn)
		optionsLayout.addWidget(self.openMAGBtn)
		optionsLayout.addWidget(self.cbMethods)
		optionsLayout.addWidget(self.cbOrders)
		optionsLayout.addWidget(self.interpolateBtn)
		optionsLayout.addWidget(self.seasonDecomposeBtn)
		optionsLayout.addWidget(self.saveCvsBtn)
		optionsLayout.addStretch(0)
		optionsLayout.setContentsMargins(0, 0, 0, 0)
		optionsLayout.setSpacing(0)

		# Toolbar and canvas layout
		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(self.toolbar)
		layout.addWidget(self.canvas)

		mainLayout.addLayout(layout)
		mainLayout.addLayout(optionsLayout)

		# Create a placeholder widget to hold our toolbar and canvas.
		widget = QtWidgets.QWidget()
		widget.setLayout(mainLayout)
		self.setCentralWidget(widget)
		self.showMaximized()

	# Plot 
	def plot(self, interpolate = False):
		self.canvas.axes.cla()
		self.canvas.axes.grid(False)  
		self.canvas.axes.set_xlabel('date', fontsize=15)
		self.canvas.axes.set_ylabel('T, nT', fontsize=15)
		if interpolate:
			self.canvas.axes.plot(self.data['T_interp'], color='red', linewidth=1.5)
		self.canvas.axes.plot(self.data['T'], color='k', linewidth=1.5)
		self.canvas.draw()
	
	# Apply interpolation	
	def interpolate(self):
		if hasattr(self, 'data'):
			try:
				self.method = self.cbMethods.currentText()
				self.order = int(self.cbOrders.currentText())
				self.data = make_interpolation(self.old_data, method=self.method, order=self.order)
				self.plot(interpolate = True)
			except:
				print('Exception: ', sys.exc_info()[0])

	# Seasonal decompose
	def make_seasonal_decompose(self):
		if hasattr(self, 'data'):
			try:
				self.data = make_seasonal_decompose(self.old_data, 
					start_date = '2019-05-23 05:30:00',
					end_date = '2019-05-25 06:24:30'
				)
				self.plot(interpolate = True)
			except:
				print('Exception: ', sys.exc_info()[0])

	# Open mag file
	def open_mag_file(self):
		self.file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open", "", "Files (*)")
		if self.file_name[0]:
			self.data = read_mag_file(self.file_name[0])
			self.old_data = self.data
			self.plot()

	# Open csv file
	def open_csv_file(self):
		self.file_name = QtWidgets.QFileDialog.getOpenFileName(None, "Open", "", "Files (*.csv)")
		if self.file_name[0]:
			self.data = read_csv_file(self.file_name[0])
			self.old_data = self.data
			self.plot()

	# Save data to cvs
	def save_to_cvs(self):
		self.data.to_csv('out.csv')  
	
# Main
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
