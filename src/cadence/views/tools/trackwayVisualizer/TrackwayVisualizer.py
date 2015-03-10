__author__ = 'Wilson'

import nimble

from nimble import cmds
import math

from pyglass.dialogs.PyGlassBasicDialogManager import PyGlassBasicDialogManager

from cadence.CadenceEnvironment import CadenceEnvironment
from cadence.enums.TrackPropEnum import TrackPropEnum
from cadence.enums.SourceFlagsEnum import SourceFlagsEnum

from cadence.models.tracks.Tracks_Track import Tracks_Track
from cadence.models.tracks.Tracks_SiteMap import Tracks_SiteMap

from cadence.util.maya.MayaUtils import MayaUtils

from cadence.mayan.trackway import GetSelectedUidList
from cadence.mayan.trackway import GetUidList
from cadence.mayan.trackway import GetTrackNodeData
from cadence.mayan.trackway import SetNodeDatum
from cadence.mayan.trackway import SetNodeLinks

class TrackwayVisualizer(object):

    LAYER_SUFFIX = '_Trackway_Layer'
    PATH_LAYER   = 'Track_Path_Layer'
    FIT_FACTOR   = 0.2
    CADENCE_CAM  = 'CadenceCam'


    def __init__(self):
        self._session = None


    #___________________________________________________________________________________________________ getFirstTrack
    def getFirstTrack(self):
        """
        Returns the track corresponding to the first track in a series, based on a given
        selection of one or more track nodes.
        :return: First track.
        """

        selectedTracks = self.getSelectedTracks()
        if not selectedTracks:
            return None

        t = selectedTracks[0]
        p = self.getPreviousTrack(t)
        while p != None:
            t = p
            p = self.getPreviousTrack(p)

        return t

    def getLastTrack(self):
        """
        Returns the track corresponding to the last track in a series, based on a given
        selection of one or more track nodes.
        :return: Last track.
        """

        selectedTracks = self.getSelectedTracks()
        if not selectedTracks:
            return None

        t = selectedTracks[0]
        n = self.getNextTrack(t)
        while n != None:
            t = n
            n = self.getNextTrack(n)

        return t

    # __________________________________________________________________________________________________ getSelectedTracks
    def getSelectedTracks(self):
        """
        Returns a list of selected tracks in the Maya environment.
        :return: List of tracks.
        """
        return cmds.ls('Track*', sl=True)

    #___________________________________________________________________________________________________ getPreviousTrack
    def getPreviousTrack(self, track):
        """
        Returns the previous track attribute of the track param.
        :param: track: Track to query on.
        :return: Previous track.
        """
        return cmds.getAttr(track+'.cadence_prevNode')

    def getNextTrack(self, track):
        """
        Returns the next track attribute of the track param.
        :param track: Track to query on.
        :return: Next track.
        """
        return cmds.getAttr(track+".cadence_nextNode")

    def selectTrack(self, track):
        """
        Select the node corresponding to this track model instance, then focus the camera
        upon this node.
        :param: track: Track to select.
        :return: None.
        """

        if track:
            cmds.select(track)
            self.setCameraFocus()
        else:
            cmds.select(clear=True)

    def setCameraFocus(self):
        """
        Center the current camera (TrackwayCam or persp) on the currently selected node.
        :return: None.
        """

        cmds.viewFit(fitFactor=self.FIT_FACTOR, animate=True)

    def getFirstSelectedTrack(self):
        """
        Returns the track corresponding to the first of a series of selected nodes.
        :return: First selected track.
        """

        selectedTracks = self.getSelectedTracks()
        if not selectedTracks:
            return None

        t = selectedTracks[0]
        p = self.getPreviousTrack(t)

        while p in selectedTracks:
            t = p
            p = self.getPreviousTrack(p)

        return t

    def getLastSelectedTrack(self):
        """
        Returns the track corresponding to the last of a series of selected nodes.
        :return: Last selected track.
        """

        selectedTracks = self.getSelectedTracks()
        if not selectedTracks:
            return None

        t = selectedTracks[-1]
        n = self.getNextTrack(t)
        while n in selectedTracks:
            t = n
            n = self.getNextTrack(n)

        return t

    def getNextUnc(self, track, widthUnc, lengthUnc, rotUnc):
        """
        :param track: Current track.
        :param widthUnc: Width uncertainty threshold to exceed.
        :param lengthUnc: Length uncertainty threshold to exceed.
        :param rotUnc: Rotational uncertainty threshold to exceed.
        :return: The next track to meet param-based uncertainty thresholds.
        """

        next = cmds.getAttr(track+'.cadence_nextNode')

        while next != None:
            if cmds.getAttr(next+'.cadence_widthUncertainty') >= widthUnc and \
                cmds.getAttr(next+'.cadence_lengthUncertainty') >= lengthUnc and \
                cmds.getAttr(next+'.cadence_rotationUncertainty') >= rotUnc:
                return next
            next = cmds.getAttr(next+'.cadence_nextNode')

        return None

    def getPrevUnc(self, track, widthUnc, lengthUnc, rotUnc):
        """
        :param track: Current track.
        :param widthUnc: Width uncertainty threshold to exceed.
        :param lengthUnc: Length uncertainty threshold to exceed.
        :param rotUnc: Rotational uncertainty threshold to exceed.
        :return: The previous track to meet param-based uncertainty threshold.
        """
        prev = cmds.getAttr(track+'.cadence_prevNode')

        while prev != None:
            if cmds.getAttr(prev+'.cadence_widthUncertainty') >= widthUnc and \
                cmds.getAttr(prev+'.cadence_lengthUncertainty') >= lengthUnc and \
                cmds.getAttr(prev+'.cadence_rotationUncertainty') >= rotUnc:
                return prev
            prev = cmds.getAttr(prev+'.cadence_prevNode')

        return None

    def getFirstUnc(self, widthUnc, lengthUnc, rotUnc):
        """
        :param widthUnc: Width uncertainty threshold to exceed.
        :param lengthUnc: Length uncertainty threshold to exceed.
        :param rotUnc: Rotational uncertainty threshold to exceed.
        :return: The first track to meet param-based uncertainty threshold.
        """

        selectedTracks = self.getSelectedTracks()
        if not selectedTracks:
            return None

        t = selectedTracks[0]
        p = self.getPrevUnc(t, widthUnc, lengthUnc, rotUnc)
        while p != None:
            t = p
            p = self.getPrevUnc(p, widthUnc, lengthUnc, rotUnc)

        return t

    def getLastUnc(self, widthUnc, lengthUnc, rotUnc):
        """
        :param widthUnc: Width uncertainty threshold to exceed.
        :param lengthUnc: Length uncertainty threshold to exceed.
        :param rotUnc: Rotational uncertainty threshold to exceed.
        :return: The last track to meet param-based uncertainty threshold.
        """

        selectedTracks = self.getSelectedTracks()
        if not selectedTracks:
            return None

        t = selectedTracks[-1]
        n = self.getNextUnc(t, widthUnc, lengthUnc, rotUnc)
        while n != None:
            t = n
            n = self.getNextUnc(t, widthUnc, lengthUnc, rotUnc)

        return t

    def getSelectedTrackway(self):
        """
        :return: A list of tracks denoting the selected trackway.
        """

        tracks = list()
        trav = self.getFirstTrack()

        while trav != None:
            tracks.append(trav)
            trav = self.getNextTrack(trav)

        return tracks

    def selectPerspCam(self):
        """
        Selects the persp cam in the Maya environment.
        :return: None.
        """
        cmds.lookThru('persp')
        self.setCameraFocus()

    def selectTrackCam(self, cam):
        """
        :param cam: The camera to be selected.
        :return: None.
        """
        cmds.lookThru(cam[0])
        #self.setCameraFocus()

class CameraAnimation():

    def __init__(self):
        self._camElevation = 0
        self._camSpeed = 480
        self._camAngle = 0
        self._focalLength = .1
        self._startingTrack = None
        self._trackway = None
        self._mainCam = None
        self._trackWayCurve = None
        self._baseTrackwayCurve = None
        self._motionPath = None
        self._spheres = []
        self._shaders = []

    def setStartingTrack(self, track):
        """
        :param track: Track to be set.
        :return: None.
        """
        self._startingTrack = track

    def setTrackway(self, trackway):
        """
        :param trackway: Trackway to be set.
        :return: None.
        """
        self._trackway = trackway

    def setCamElevation(self, height):
        """
        :param height: Set _trackwayCurve to this height.
        :return: None.
        """
        self._camElevation = height
        if self._trackWayCurve is not None:
            cmds.setAttr(self._trackWayCurve+".translateY", self._camElevation)

    def getCamElevation(self):
        """
        :return: Cam elevation.
        """
        return self._camElevation

    def setAnimSpeed(self, speed):
        """
        :param speed: Set _camSpeed to speed.
        :return: None.
        """
        # Nimble bridge doesn't allow you to use time parameter in cmds.keyframe(), so we resort to creating a new path.
        self._camSpeed = speed
        cmds.delete(self._motionPath)
        self.setToCurve()

    def getAnimSpeed(self):
        """
        :return: Camera speed.
        """
        return self._camSpeed

    def setAnimAngle(self, angle):
        """
        :param angle: Set _camAngle to angle.
        :return: None.
        """
        self._camAngle = angle
        if self._mainCam is not None:
            cmds.setAttr(self._motionPath+".sideTwist", self._camAngle)
            # At start, camera has _camAngle.
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=0)
            # At start of turnaround in path, keep angle at _camAngle
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed*1.0/4)
            # After 3/8 of path, move camera to orthogonal view to avoid looking off into the abyss.
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=self._camSpeed*3.0/8)
            # At halfway point, keep angle orthogonal.
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=self._camSpeed*1.0/2)
            # At 5/8 of the total curve, move the angle to 2/3 of _camAngle for 'smooth' transition.
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle*2.0/3, t=self._camSpeed*5.0/8)
            # At 3/4 of the total curve, movve the angle to the full _camAngle
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed*3.0/4)
            # Keep angle at _camAngle to the end of the curve.
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed)

    def getAnimAngle(self):
        """
        :return: Camera angle.
        """
        return self._camAngle

    def setFocalLength(self, length):
        """
        :param length: Set _focalLength to length.
        :return: None.
        """
        self._focalLength = length
        cmds.setAttr(self._mainCam[0]+".focalLength", self._focalLength)

    def getFocalLength(self):
        """
        :return: Focal length.
        """
        return self._focalLength

    def createMainCamera(self):
        """
        Create new camera.
        :return: None.
        """
        self._mainCam = cmds.camera()

    def positionCamOnTrack(self):
        """
        Sets starting position of cam to the starting track.
        :return: None.
        """
        xPos = cmds.getAttr(self._startingTrack+".translateX")
        cmds.setAttr(self._mainCam[0]+".translateX", xPos)

        zPos = cmds.getAttr(self._startingTrack+".translateZ")
        cmds.setAttr(self._mainCam[0]+".translateZ", zPos)

        cmds.setAttr(self._mainCam[0]+".translateY", self._camElevation)

    def makeCurve(self):
        """
        Creates curve in Maya environment based on track coordinates, and sets the camera's motion to
        this curve.
        :return: None.
        """
        pos = list()
        # Need to change to take first two coordinates of track, and extend this vector out in the opposite direction.
        pos.append((cmds.getAttr(self._trackway[0]+".translateX")-100, 100, cmds.getAttr(self._trackway[0]+".translateZ")-100))

        for track in self._trackway:
            pos.append(((cmds.getAttr(track+".translateX")), 0, cmds.getAttr(track+".translateZ")))

        # Get reverse iterator for current list of tracks
        it = reversed(pos)

        # Get list of last two points in pos list.
        last_vec = [pos[-2], pos[-1]]

        dir_vec = tuple([(last_vec[1][i]-last_vec[0][i])/2 for i in range(3)])
        norm_vec = tuple([-1.5*dir_vec[2], 0, 1.5*dir_vec[0]])
        center_pt = (cmds.getAttr(self._trackway[-1]+".translateX")+dir_vec[0],0, cmds.getAttr(self._trackway[-1]+".translateZ")+dir_vec[2])

        # Put three corners of turnaround into pos list.
        pos.append(tuple([center_pt[i]+norm_vec[i] for i in range(3)]))
        pos.append(tuple([center_pt[i]+dir_vec[i] for i in range(3)]))
        pos.append(tuple([center_pt[i] - norm_vec[i] for i in range(3)]))

        # Put reversed initial pos list into pos.
        rev = list()
        try:
            while True:
                rev.append(it.next())
        except StopIteration:
            pass
        pos += rev

        # Set _trackWayCurve to created curve based on the pos list, and move the track to _camElevation.
        self._trackWayCurve = cmds.curve(name='camCurve',p=pos)
        self._baseTrackwayCurve = cmds.duplicate(self._trackWayCurve, name='baseCurve')
        cmds.setAttr(self._trackWayCurve+".translateY", self._camElevation)

    def setToCurve(self):
        """
        Keyframes curve to make the trackway visualization look 'pretty.'
        :return: None
        """
        self._motionPath = cmds.pathAnimation(self._mainCam[0], etu=self._camSpeed, follow=True, c=self._trackWayCurve)
        # Nimble bridge doesn't allow you to use std parameter in cmds.pathAnimation
        cmds.setAttr(self._motionPath+".sideTwist", self._camAngle)
        # At start, camera has _camAngle.
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=0)
        # At start of turnaround in path, keep angle at _camAngle
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed*1.0/4)
        # After 3/8 of path, move camera to orthogonal view to avoid looking off into the abyss.
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=self._camSpeed*3.0/8)
        # At halfway point, keep angle orthogonal.
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=self._camSpeed*1.0/2)
        # At 5/8 of the total curve, move the angle to 2/3 of _camAngle for 'smooth' transition.
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle*2.0/3, t=self._camSpeed*5.0/8)
        # At 3/4 of the total curve, movve the angle to the full _camAngle
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed*3.0/4)
        # Keep angle at _camAngle to the end of the curve.
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed)

    def createVisualizerSpheres(self):
        self._shaders = []
        self._spheres = []
        for track in self._trackway:
            newSphere = cmds.polySphere(r=20)
            cmds.setAttr(newSphere[0]+".scaleY", 0.5)
            cmds.setAttr(newSphere[0]+".translateX", cmds.getAttr(track+".translateX"))
            cmds.setAttr(newSphere[0]+".translateZ", cmds.getAttr(track+".translateZ"))
            cmds.setAttr(newSphere[0]+".translateY", -10)
            shader = self.createHotColdShader(cmds.getAttr(track+".cadence_datum"))
            cmds.select(newSphere)
            cmds.hyperShade(assign=shader)
            self._shaders.append(shader)
            self._spheres.append(newSphere)



    def createHotColdShader(self, uncertainty):
        """
        :param uncertainty: uncertainty value to give ramp different hot:cold ratio
        :return: shader for track

        color[1] = blue
        color[0] = red
        """
        new_shade = cmds.shadingNode('rampShader', asShader=True)
        cmds.setAttr(new_shade+".color[0].color_Color", 1,0,0, type="double3")
        cmds.setAttr(new_shade+".color[1].color_Color", 0,0,1, type="double3")
        bluePos = 0.65 + (uncertainty/3)
        cmds.setAttr(new_shade+".color[1].color_Position", bluePos)
        cmds.setAttr(new_shade+".color[0].color_Position", 1)
        cmds.setAttr(new_shade+".color[0].color_Interp", 1)
        cmds.setAttr(new_shade+".color[1].color_Interp", 1)
        return new_shade

