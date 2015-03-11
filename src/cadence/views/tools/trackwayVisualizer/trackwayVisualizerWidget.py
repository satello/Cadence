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
from cadence.views.tools.trackwayVisualizer.TrackwayVisualizer import CameraAnimation
from cadence.views.tools.trackNodeUtils.TrackNodeUtils import TrackNodeUtils
from nimble import cmds

class TrackwayVisualizerWidget(PyGlassWidget):

    RESOURCE_FOLDER_PREFIX = ['tools']

    def __init__(self, parent, **kwargs):
        super(TrackwayVisualizerWidget, self).__init__(parent, **kwargs)

        self._uiLock  = False
        self._session = None


        # create an instance of a TrackwayManager to deal with the database and the Maya scene
        self._trackwayVisualizer = TrackwayVisualizer()

        # create an instance of CameraAnimation to visualize a path
        self._animation = CameraAnimation()

        # provide conventional arrow icons for the navigation buttons
        self.firstBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'first.png')))
        self.prevBtn.setIcon( QtGui.QIcon(self.getResourcePath('mediaIcons', 'prev.png')))
        self.nextBtn.setIcon( QtGui.QIcon(self.getResourcePath('mediaIcons', 'next.png')))
        self.lastBtn.setIcon( QtGui.QIcon(self.getResourcePath('mediaIcons', 'last.png')))

        self.firstBtn.clicked.connect(self.handleFirstTrackBtn)
        self.prevBtn.clicked.connect(self.handlePrevBtn)
        self.nextBtn.clicked.connect(self.handleNextBtn)
        self.lastBtn.clicked.connect(self.handleLastTrackBtn)

        self.widthUncertaintySbx.valueChanged.connect(self.handleWidthUnc)
        self.lengthUncertaintySbx.valueChanged.connect(self.handleLengthUnc)
        self.rotationUncertaintySbx.valueChanged.connect(self.handleRotationUnc)

        self.elevationSbox.valueChanged.connect(self.handleElevation)
        self.angleSbox.valueChanged.connect(self.handleAngle)
        self.speedSbox.valueChanged.connect(self.handleSpeed)
        self.fLengthSbox.valueChanged.connect(self.handleFocal)

        self.selectTrackwayCamBtn.clicked.connect(self.handleCreateCam)
        self.selectTrackFromListBtn.clicked.connect(self.handleCreateCamFromList)

        self.firstUncBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'first.png')))
        self.prevUncBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'prev.png')))
        self.nextUncBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'next.png')))
        self.lastUncBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'last.png')))

        self.firstUncBtn.clicked.connect(self.handleFirstUncBtn)
        self.prevUncBtn.clicked.connect(self.handlePrevUncBtn)
        self.nextUncBtn.clicked.connect(self.handleNextUncBtn)
        self.lastUncBtn.clicked.connect(self.handleLastUncBtn)

        self.displayWidthCkbx.clicked.connect(self.handleDisplayWidth)
        self.displayLengthCkbx.clicked.connect(self.handleDisplayLength)
        self.displayRotationCkbx.clicked.connect(self.handleDisplayRotation)

        self.pauseBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'pause.png')))
        self.playBtn.setIcon(QtGui.QIcon(self.getResourcePath('mediaIcons', 'play.png')))

        self.pauseBtn.clicked.connect(self.handlePauseBtn)
        self.playBtn.clicked.connect(self.handlePlayBtn)

        self.perspCamBtn.clicked.connect(self.handlePerspCamBtn)
        self.trackCamBtn.clicked.connect(self.handleTrackCamBtn)

        self.widthUnc, self.lengthUnc, self.rotUnc = 0.0, 0.0, 0.0
        self.displayWidth, self.displayLength, self.displayRotation = False, False, False

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
        track = self._trackwayVisualizer.getLastSelectedTrack()
        next = self._trackwayVisualizer.getNextUnc(track, self.widthUnc, self.lengthUnc, self.rotUnc)
        if next is None:
            PyGlassBasicDialogManager.openOk(
                self,
                'No next track meets uncertainty conditions',
                '%s is the last in this series' % track)
            return

        self._trackwayVisualizer.selectTrack(next)

    def handlePrevUncBtn(self):
        track = self._trackwayVisualizer.getFirstSelectedTrack()
        prev = self._trackwayVisualizer.getPrevUnc(track, self.widthUnc, self.lengthUnc, self.rotUnc)
        if prev is None:
            PyGlassBasicDialogManager.openOk(
                self,
                'No previous track meets uncertainty conditions',
                '%s is the first in this series' % track)
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

    def handleCreateCam(self):
        track = self._trackwayVisualizer.getSelectedTracks()
        if len(track) < 1:
            print "No Selection"
        else:
            trackway = self._trackwayVisualizer.getSelectedTrackway()
            self._animation.setTrackway(trackway)
            self._animation.setStartingTrack(track[0])
            self._animation.createMainCamera()
            self._animation.positionCamOnTrack()
            self._animation.makeCurve()
            self._animation.setToCurve()
            self._animation.createVisualizerCylinders()

    def handleElevation(self):
        elevation = self.elevationSbox.value()
        self._animation.setCamElevation(elevation)

    def handleAngle(self):
        angle = self.angleSbox.value()
        self._animation.setAnimAngle(angle)

    def handleSpeed(self):
        speed = self.speedSbox.value()
        self._animation.setAnimSpeed(speed*24)

    def handleFocal(self):
        fLength = self.fLengthSbox.value()
        self._animation.setFocalLength(fLength)

    def handleWidthUnc(self):
        self.widthUnc = self.widthUncertaintySbx.value()

    def handleLengthUnc(self):
        self.lengthUnc = self.lengthUncertaintySbx.value()

    def handleRotationUnc(self):
        self.rotUnc = self.rotationUncertaintySbx.value()

    def handleDisplayWidth(self):
        if self.displayWidthCkbx.isChecked():
            self.displayWidth = True
        else:
            self.displayWidth = False
        self._animation.widthUnc = self.displayWidth


    def handleDisplayLength(self):
        if self.displayLengthCkbx.isChecked():
            self.displayLength = True
        else:
            self.displayLength = False
        self._animation.lengthUnc = self.displayLength
        self._animation.updateUncDisplay()

    def handleDisplayRotation(self):
        if self.displayRotationCkbx.isChecked():
            self.displayRotation = True
        else:
            self.displayRotation = False


    def handlePauseBtn(self):
        cmds.play(state=False)

    def handlePlayBtn(self):
        cmds.play(forward=True)

    def handleCreateCamFromList(self):
        tracks = self._trackwayVisualizer.getSelectedTracks()
        self._animation.setTrackway(tracks)
        self._animation.setStartingTrack(self._trackwayVisualizer.getFirstSelectedTrack())
        self._animation.createMainCamera()
        self._animation.positionCamOnTrack()
        self._animation.makeCurve()
        self._animation.setToCurve()

    def handlePerspCamBtn(self):
        self._trackwayVisualizer.selectPerspCam()

    def handleTrackCamBtn(self):
        self._trackwayVisualizer.selectTrackCam(self._animation._mainCam)

