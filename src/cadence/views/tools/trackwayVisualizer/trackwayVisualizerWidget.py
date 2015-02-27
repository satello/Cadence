__author__ = 'Wilson'

from PySide import QtGui
from pyaid.string.StringUtils import StringUtils
from pyglass.widgets.PyGlassWidget import PyGlassWidget
from pyglass.dialogs.PyGlassBasicDialogManager import PyGlassBasicDialogManager

from cadence.CadenceEnvironment import CadenceEnvironment
from cadence.enums.TrackPropEnum import TrackPropEnum
from cadence.enums.SourceFlagsEnum import SourceFlagsEnum
from cadence.svg.CadenceDrawing import CadenceDrawing
from cadence.views.tools.trackwayVisualizer.TrackwayVisualizer import TrackwayVisualizer
from cadence.views.tools.trackNodeUtils.TrackNodeUtils import TrackNodeUtils

class TrackwayVisualizerWidget(PyGlassWidget):

    RESOURCE_FOLDER_PREFIX = ['tools']

    def __init__(self, parent, **kwargs):
        super(TrackwayVisualizerWidget, self).__init__(parent, **kwargs)

        self._uiLock  = False
        self._session = None

        # create an instance of a TrackwayManager to deal with the database and the Maya scene
        self._trackwayVisualizer = TrackwayVisualizer()

        # provide conventional arrow icons for the navigation buttons
        self.firstBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'first.png')))
        self.prevBtn.setIcon( QtGui.QIcon(self.getResourcePath('mediaIcons', 'prev.png')))
        self.nextBtn.setIcon( QtGui.QIcon(self.getResourcePath('mediaIcons', 'next.png')))
        self.lastBtn.setIcon( QtGui.QIcon(self.getResourcePath('mediaIcons', 'last.png')))

        self.firstBtn.clicked.connect(self.handleFirstTrackBtn)
        self.prevBtn.clicked.connect(self.handlePrevBtn)
        self.nextBtn.clicked.connect(self.handleNextBtn)
        self.lastBtn.clicked.connect(self.handleLastTrackBtn)

        self.widthUncInput.valueChanged.connect(self.handleWidthUnc)
        self.lengthUncInput.valueChanged.connect(self.handleLengthUnc)
        self.rotationUncInput.valueChanged.connect(self.handleRotationUnc)

        self.firstUncBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'first.png')))
        self.prevUncBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'prev.png')))
        self.nextUncBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'next.png')))
        self.lastUncBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'last.png')))

        self.firstUncBtn.connect(self.handleFirstUncBtn)
        self.prevUncBtn.connect(self.handlePrevUncBtn)
        self.nextUncBtn.connect(self.handleNextUncBtn)
        self.lastUncBtn.connect(self.handleLastUncBtn)

        self.displayWidthCkbx.clicked.connect(self.handleDisplayWidth)
        self.displayHeightCkbx.clicked.connect(self.handleDisplayHeight)
        self.displayRotationCkbx.clicked.connect(self.handleDisplayRotation)

        self.widthUnc, self.lengthUnc, self.rotUnc = 0.0, 0.0, 0.0
        self.displayWidth, self.displayHeight, self.displayRotation = False, False, False

    def handleFirstTrackBtn(self):
        """ Get the first track, select the corresponding node, and focus the camera on it. """

        track = self._trackwayVisualizer.getFirstTrack()
        if track is None:
            return

        self._trackwayVisualizer.selectTrack(track)

    def handlePrevBtn(self):
        """ Get the previous track, select its corresponding node, and focus the camera on it. If
            there is no previous node, just leave the current node selected. """

        track = self._trackwayVisualizer.getFirstSelectedTrack()
        if track is None:
            return

        prev = self._trackwayVisualizer.getPreviousTrack(track)
        if prev is None:
            PyGlassBasicDialogManager.openOk(
                self,
                'No previous track',
                '%s is the first in this series' % track)
            return

        self._trackwayVisualizer.selectTrack(prev)

    def handleNextBtn(self):
        """ Get the next track, select its corresponding node, and focus the camera on it. If
            there is no next node, just leave the current node selected. """

        track = self._trackwayVisualizer.getLastSelectedTrack()

        if track is None:
            return

        next = self._trackwayVisualizer.getNextTrack(track)
        if next is None:
            PyGlassBasicDialogManager.openOk(
                self,
                'No next track',
                '%s is the last in this series' % track)
            return

        self._trackwayVisualizer.selectTrack(next)

    def handleLastTrackBtn(self):
        track = self._trackwayVisualizer.getLastTrack()
        if track is None:
            return

        self._trackwayVisualizer.selectTrack(track)

    def handleNextUncBtn(self):
        track = self._trackwayVisualizer.getFirstSelectedTrack()
        next = self._trackwayVisualizer.getNextUnc(track, self.widthUnc, self.lengthUnc, self.rotUnc)
        if next is None:
            PyGlassBasicDialogManager.openOK(self,"No next track meets uncertainty conditions", '%s is the last in this series' % track)
            return
        self._trackwayVisualizer.selectTrack(next)

    def handlePrevUncBtn(self):
        track = self._trackwayVisualizer.getLastSelectedTrack()
        prev = self._trackwayVisualizer.getPrevUnc(track, self.widthUnc, self.lengthUnc, self.rotUnc)
        if prev is None:
            PyGlassBasicDialogManager.openOK(self,"No previous track meets uncertainty conditions", '%s is the first in this series' % track)
            return
        self._trackwayVisualizer.selectTrack(prev)

    def handleFirstUncBtn(self):
        track = self._trackwayVisualizer.getFirstUnc(self.widthUnc, self.lengthUnc, self.rotUnc)
        if track is None:
            return

        self._trackwayVisualizer.selectTrack(track)

    def handleLastUncBtn(self):
        track = self._trackwayVisualizer.getLastUnc(self.widthUnc, self.lengthUnc, self.rotUnc)
        if track is None:
            return

        self._trackwayVisualizer.selectTrack(track)

    def handleWidthUnc(self):
        self.widthUnc = self.widthUncInput.value()

    def handleLengthUnc(self):
        self.lengthUnc = self.lengthUncInput.value()

    def handleRotationUnc(self):
        self.rotUnc = self.rotationUncInput.value()

    def handleDisplayWidth(self):
        if self.displayWidthCkbx.isChecked():
            self.displayWidth = True
        else:
            self.displayWidth = False

    def handleDisplayHeight(self):
        if self.displayHeightCkbx.isChecked():
            self.displayHeight = True
        else:
            self.displayHeight = False

    def handleDisplayRotation(self):
        if self.displayRotationCkbx.isChecked():
            self.displayRotation = True
        else:
            self.displayRotation = False