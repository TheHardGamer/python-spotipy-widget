import sys
from time import sleep
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import spotipy
from threading import Thread
from spotipy.oauth2 import SpotifyOAuth
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="", client_secret="", redirect_uri="http://127.0.0.1:9090",scope="user-modify-playback-state,user-read-playback-state"))

class FramelessWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Now Playing!")
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.w=QWebEngineView()
		self.pal = self.palette()
		self.pal.setColor(self.backgroundRole(), Qt.black)
		self.setPalette(self.pal)
		self.w.load(QtCore.QUrl('')) #Widget URL from widgetapp.stream
		self.setAutoFillBackground(True)
		self.w.page().setBackgroundColor(Qt.green)
		self.next = QPushButton("Next", self)
		self.back = QPushButton("Back", self)
		self.play = QPushButton("Play", self)
		self.pause = QPushButton("Pause", self)
		self.updateDev = QPushButton("Update Devices", self)
		self.devices = QComboBox(self)
		self.devicesmap = dict()
		curr_devices = spotify.devices()
		for device in curr_devices["devices"]:
			self.devicesmap[device["name"]] = device["id"]
			self.devices.addItem(device["name"])
		self.next.setFixedSize(QtCore.QSize(50, 50))
		self.next.clicked.connect(self.nextTrack)
		self.back.setFixedSize(QtCore.QSize(50, 50))
		self.play.setFixedSize(QtCore.QSize(50, 50))
		self.pause.setFixedSize(QtCore.QSize(50, 50))
		self.back.clicked.connect(self.prevTrack)
		self.play.clicked.connect(self.startPlayback)
		self.pause.clicked.connect(self.pausePlayback)
		self.updateDev.clicked.connect(self.devicesUpdater_)
		self.layo = QVBoxLayout(self)
		self.hor = QHBoxLayout(self)
		self.layo.addLayout(self.hor)
		self.layo.addWidget(self.w)
		self.layo.addWidget(self.updateDev)
		self.hor.addWidget(self.next)
		self.hor.addWidget(self.back)
		self.hor.addWidget(self.devices)
		self.hor.addWidget(self.play)
		self.hor.addWidget(self.pause)
		self.offset = None

	def devicesUpdater_(self):
		print("Updating Devices...")
		self.devices.clear()
		self.devicesmap.clear()
		curr_devices = spotify.devices()
		for device in curr_devices["devices"]:
			self.devicesmap[device["name"]] = device["id"]
			self.devices.addItem(device["name"])

	def pausePlayback(self):
		Thread(target=spotify.pause_playback(device_id=self.devicesmap[self.devices.currentText()]), daemon=True).start()

	def startPlayback(self):
		Thread(target=spotify.start_playback(device_id=self.devicesmap[self.devices.currentText()]), daemon=True).start()

	def nextTrack(self):
		Thread(target=spotify.next_track(device_id=self.devicesmap[self.devices.currentText()]),daemon=True).start()

	def prevTrack(self):
		Thread(target=spotify.previous_track(device_id=self.devicesmap[self.devices.currentText()]),daemon=True).start()

	def mousePressEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			self.offset = event.pos()
		else:
			super().mousePressEvent(event)

	def mouseMoveEvent(self, event):
		if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
			self.move(self.pos() + event.pos() - self.offset)
		else:
			super().mouseMoveEvent(event)

	def mouseReleaseEvent(self, event):
		self.offset = None
		super().mouseReleaseEvent(event)

app=QtWidgets.QApplication(sys.argv)
app.setApplicationName("Now Playing By THG")
win = FramelessWidget()
win.resize(615,350)
win.show()
app.exec_()