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
        """ Returns the track model corresponding to the first track in a series, based on a given
            selection of one or more track nodes. """

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
        return cmds.ls('Track*', sl=True)

    #___________________________________________________________________________________________________ getPreviousTrack
    def getPreviousTrack(self, track):
        """ This method just encapsulates the session getter. """
        return cmds.getAttr(track+'.cadence_prevNode')

    def getNextTrack(self, track):
        #print cmds.listAttr(track)
        return cmds.getAttr(track+".cadence_nextNode")

    def selectTrack(self, track):
        """ Select the node corresponding to this track model instance, then focus the camera
            upon this node. """

        if track:
            cmds.select(track)
            self.setCameraFocus()
        else:
            cmds.select(clear=True)

    def setCameraFocus(self):
        """ Center the current camera (CadenceCam or persp) on the currently selected node. If
            using the CadenceCam, the view is fitted to FIT_FACTOR; with the persp camera, it is
            not so contrained. """

        cmds.viewFit(fitFactor=self.FIT_FACTOR, animate=True)

    def getFirstSelectedTrack(self):
        """ Returns the track model corresponding to the first of a series of selected nodes. """

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
        """ Returns the track model corresponding to the last of a series of selected nodes. """
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
        next = cmds.getAttr(track+'.cadence_nextNode')

        while next != None:
            if cmds.getAttr(next+'.cadence_widthUncertainty') >= widthUnc and \
                cmds.getAttr(next+'.cadence_lengthUncertainty') >= lengthUnc and \
                cmds.getAttr(next+'.cadence_rotationUncertainty') >= rotUnc:
                return next
            next = cmds.getAttr(next+'.cadence_nextNode')

        return None

    def getPrevUnc(self, track, widthUnc, lengthUnc, rotUnc):
        prev = cmds.getAttr(track+'.cadence_prevNode')

        while prev != None:
            if cmds.getAttr(prev+'.cadence_widthUncertainty') >= widthUnc and \
                cmds.getAttr(prev+'.cadence_lengthUncertainty') >= lengthUnc and \
                cmds.getAttr(prev+'.cadence_rotationUncertainty') >= rotUnc:
                return prev
            prev = cmds.getAttr(prev+'.cadence_prevNode')

        return None

    def getFirstUnc(self, widthUnc, lengthUnc, rotUnc):

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
        tracks = list()
        trav = self.getFirstTrack()

        while trav != None:
            tracks.append(trav)
            trav = self.getNextTrack(trav)

        return tracks

    def selectPerspCam(self):
        cmds.lookThru('persp')
        self.setCameraFocus()

    def selectTrackCam(self, cam):
        cmds.lookThru(cam[0])
        #self.setCameraFocus()

class CameraAnimation():

    def __init__(self):
        self._camElevation = 0
        self._camSpeed = 120
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
        self._maxUncertainty = 0.2
        self.lengthUnc = False
        self.widthUnc = False

    def setStartingTrack(self, track):
        self._startingTrack = track

    def setTrackway(self, trackway):
        self._trackway = trackway

    def setCamElevation(self, height):
        self._camElevation = height
        if self._trackWayCurve is not None:
            cmds.setAttr(self._trackWayCurve+".translateY", self._camElevation)

    def getCamElevation(self):
        return self._camElevation

    def setAnimSpeed(self, speed):
        # Nimble bridge doesn't allow you to use time parameter in cmds.keyframe(), so we resort to creating a new path.
        self._camSpeed = speed
        cmds.delete(self._motionPath)
        self.setToCurve()

    def getAnimSpeed(self):
        return self._camSpeed

    def setAnimAngle(self, angle):
        self._camAngle = angle
        if self._mainCam is not None:
            cmds.setAttr(self._motionPath+".sideTwist", self._camAngle)
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=0)

            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed*1.0/4)

            cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=self._camSpeed*3.0/8)

            cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=self._camSpeed*1.0/2)

            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle*2.0/3, t=self._camSpeed*5.0/8)

            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed*3.0/4)

            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed)

    def getAnimAngle(self):
        return self._camAngle

    def setFocalLength(self, length):
        self._focalLength = length
        cmds.setAttr(self._mainCam[0]+".focalLength", self._focalLength)

    def getFocalLength(self):
        return self._focalLength

    def createMainCamera(self):
        self._mainCam = cmds.camera()

    def positionCamOnTrack(self):
        xPos = cmds.getAttr(self._startingTrack+".translateX")
        cmds.setAttr(self._mainCam[0]+".translateX", xPos)

        zPos = cmds.getAttr(self._startingTrack+".translateZ")
        cmds.setAttr(self._mainCam[0]+".translateZ", zPos)

        cmds.setAttr(self._mainCam[0]+".translateY", self._camElevation)

    def makeCurve(self):
        pos = []
        #pos.append((cmds.getAttr(self._trackway[0]+".translateX")-100,100,cmds.getAttr(self._trackway[0]+".translateZ")-100))
        for track in self._trackway:
            pos.append(((cmds.getAttr(track+".translateX")), 0, cmds.getAttr(track+".translateZ")))
        it = reversed(pos)
        last_vec = [(cmds.getAttr(self._trackway[-2]+".translateX"),0, cmds.getAttr(self._trackway[-2]+".translateZ"))]
        last_vec += [(cmds.getAttr(self._trackway[-1]+".translateX"),0, cmds.getAttr(self._trackway[-1]+".translateZ"))]
        #dist = math.sqrt((last_vec[0][0]-last_vec[1][0])**2 + (last_vec[0][1] - last_vec[1][1])**2)
        dir_vec = tuple([(last_vec[1][i]-last_vec[0][i])/2 for i in range(3)])
        norm_vec = tuple([-1*dir_vec[2], 0, dir_vec[0]])
        center_pt = (cmds.getAttr(self._trackway[-1]+".translateX")+dir_vec[0],0, cmds.getAttr(self._trackway[-1]+".translateZ")+dir_vec[2])
        pos.append(tuple([center_pt[i]+norm_vec[i] for i in range(3)]))
        pos.append(tuple([center_pt[i]+dir_vec[i] for i in range(3)]))
        pos.append(tuple([center_pt[i] - norm_vec[i] for i in range(3)]))
        rev = list()
        try:
            while True:
                rev.append(it.next())
        except StopIteration:
            pass
        pos += rev

        self._trackWayCurve = cmds.curve(name='camCurve', p=pos)
        self._baseTrackwayCurve = cmds.duplicate(self._trackWayCurve, name='baseCurve')
        cmds.setAttr(self._trackWayCurve+".translateY", self._camElevation)

    def setToCurve(self):
        # Nimble bridge doesn't allow you to use std parameter in cmds.pathAnimation
        self._motionPath = cmds.pathAnimation(self._mainCam[0], etu=self._camSpeed, follow=True, c=self._trackWayCurve)
        cmds.setAttr(self._motionPath+".sideTwist", self._camAngle)
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=0)

        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed*1.0/4)

        cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=self._camSpeed*3.0/8)

        cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=self._camSpeed*1.0/2)

        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle*2.0/3, t=self._camSpeed*5.0/8)

        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed*3.0/4)

        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed)

    def createVisualizerCylinders(self):
        self._shaders = []
        self._spheres = []
        for track in self._trackway:
            newSphere = cmds.polyCylinder(r=20)
            cmds.setAttr(newSphere[0]+".scaleY", 0.5)
            cmds.setAttr(newSphere[0]+".translateX", cmds.getAttr(track+".translateX"))
            cmds.setAttr(newSphere[0]+".translateZ", cmds.getAttr(track+".translateZ"))
            cmds.setAttr(newSphere[0]+".translateY", -10)
            shader = self.createHotColdConstantColor(self.getUnc(track))
            if self.lengthUnc or self.widthUnc:
                cmds.select(newSphere)
                cmds.hyperShade(assign=shader)
            self._shaders.append(shader)
            self._spheres.append(newSphere)

    def createHotColdConstantColor(self, uncertainty):
        new_shade = cmds.shadingNode('blinn', asShader=True)
        blue = 1 - ((float(uncertainty)*10)/2)
        red = 0 + ((float(uncertainty)*10)/2)
        cmds.setAttr(new_shade+".color", red,0,blue, type="double3")
        return new_shade



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
        cmds.setAttr(new_shade+".color[1].color_Position", 0)
        cmds.setAttr(new_shade+".color[0].color_Position", 1)
        cmds.setAttr(new_shade+".color[0].color_Interp", 1)
        cmds.setAttr(new_shade+".color[1].color_Interp", 1)
        return new_shade

    def updateUncDisplay(self):
        if len(self._shaders) != 0:
            for i in range(0, len(self._trackway)):
                track = self._trackway[i]
                shade = self._shaders[i]
                cyl = self._spheres[i]
                blue = 1 - (float(self.getUnc(track))*10)
                red = 0 + (float(self.getUnc(track))*10)
                cmds.setAttr(shade+".color", red,0,blue, type="double3")
                cmds.select(cyl)
                cmds.hyperShade(assign=shade)



    def getUnc(self, track):
        num = 0
        res = 0
        if self.lengthUnc:
            res += cmds.getAttr(track+".cadence_lengthUncertainty")
            num += 1
        if self.widthUnc:
            res += cmds.getAttr(track+".cadence_widthUncertainty")
            num += 1
        if num is not 0:
            return float(res)/num
        return 0







