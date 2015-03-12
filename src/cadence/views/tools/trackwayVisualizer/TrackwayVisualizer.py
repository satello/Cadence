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
        self._spheres = list()
        self._shaders = list()
        self._maxUncertainty = 0.2
        self.lengthUnc = False
        self.widthUnc = False

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

        if len(self._spheres) > 0:
            for sphere in self._spheres:
                cmds.delete(sphere)
            self._spheres = list()
        if len(self._shaders) > 0:
            for shader in self._shaders:
                cmds.delete(shader)
            self._shaders = list()
        if self._trackway is not None:
            self.createVisualizerCylinders()

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
            max_u = cmds.getAttr(self._motionPath+'.uValue', time=self._camSpeed)
            cmds.setAttr(self._motionPath+'.sideTwist', self._camAngle)
            # Function derived through experimentation for good track turnaround aesthetics
            t = 90*math.sqrt(6)*(2.0/3)**(max_u/8)
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=0)
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=1.0/2*self._camSpeed-t)
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=1.0/2*self._camSpeed-t/2)
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=1.0/2*self._camSpeed)
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=2.0/3*self._camAngle, t=1.0/2*self._camSpeed+t/2)
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=1.0/2*self._camSpeed+t)
            cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed)

        if len(self._spheres) > 0:
            for sphere in self._spheres:
                cmds.delete(sphere)
            self._spheres = list()
        if len(self._shaders) > 0:
            for shader in self._shaders:
                cmds.delete(shader)
            self._shaders = list()
        if self._trackway is not None:
            self.createVisualizerCylinders()

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
        max_u = cmds.getAttr(self._motionPath+'.uValue', time=self._camSpeed)
        cmds.setAttr(self._motionPath+'.sideTwist', self._camAngle)
        # Function derived through experimentation for good track turnaround aesthetics
        t = 90*math.sqrt(6)*(2.0/3)**(max_u/8)
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=0)
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=1.0/2*self._camSpeed-t)
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=1.0/2*self._camSpeed-t/2)
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=0, t=1.0/2*self._camSpeed)
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=2.0/3*self._camAngle, t=1.0/2*self._camSpeed+t/2)
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=1.0/2*self._camSpeed+t)
        cmds.setKeyframe(self._motionPath, at='sideTwist', v=self._camAngle, t=self._camSpeed)

    def createVisualizerCylinders(self):
        tmp = self._trackway
        first_pt = (cmds.getAttr(tmp[0]+".translateX"), 0, cmds.getAttr(tmp[0]+".translateZ"))
        sec_pt = (cmds.getAttr(tmp[1]+".translateX"), 0, cmds.getAttr(tmp[1]+".translateZ"))
        prev_vec = tuple([sec_pt[j]-first_pt[j] for j in range(3)])
        prev_vec = tuple([first_pt[i] - prev_vec[i] for i in range(3)])
        seclast_pt = (cmds.getAttr(tmp[-2]+".translateX"), 0, cmds.getAttr(tmp[-2]+".translateZ"))
        last_pt = (cmds.getAttr(tmp[-1]+".translateX"), 0, cmds.getAttr(tmp[-1]+".translateZ"))
        next_vec = tuple([last_pt[j]-seclast_pt[j] for j in range(3)])
        next_vec = tuple([last_pt[j]+next_vec[j] for j in range(3)])
        first = cmds.polySphere(r=1)
        cmds.move(prev_vec[0], prev_vec[1], prev_vec[2], first)
        last = cmds.polySphere(r=1)
        cmds.move(next_vec[0], next_vec[1], next_vec[2], last)

        tmp.insert(0, first)
        tmp.append(last)

        for i in xrange(1, len(tmp)-1):
            newSphere = cmds.polyCylinder(r=20, h=20)
            cmds.setAttr(newSphere[0]+".translateX", cmds.getAttr(tmp[i]+".translateX"))
            cmds.setAttr(newSphere[0]+".translateZ", cmds.getAttr(tmp[i]+".translateZ"))
            cmds.setAttr(newSphere[0]+".translateY", -20)
            shader = self.createHotColdConstantColor(self.getUnc(tmp[i]))
            if self.lengthUnc or self.widthUnc:
                cmds.select(newSphere)
                cmds.hyperShade(assign=shader)
            self._shaders.append(shader)
            self._spheres.append(newSphere)

            self.handleDrivenKeys(tmp[i-1], tmp[i], tmp[i+1], newSphere)

        cmds.delete(first)
        cmds.delete(last)
        tmp.pop(0)
        tmp.pop()

    def handleDrivenKeys(self, prev, curr, next, sphere):
        tmp_vec = tuple([cmds.getAttr(curr+".translateX"), 0, cmds.getAttr(curr+".translateZ")])
        # MAGIC NUMBER HERE, FEEL FREE TO REDEFINE!!!!!!!!!
        length = 150 if self._camAngle == 0 or self._camElevation == 0 else self._camElevation/math.tan(self._camAngle)

        # make first directional vector off of change in coordinates between previous and this track
        if "Sphere" in prev[0]:
            prev_tmp_vec = tuple([cmds.getAttr(prev[0]+".translateX"), 0, cmds.getAttr(prev[0]+".translateZ")])
        else:
            prev_tmp_vec = tuple([cmds.getAttr(prev+".translateX"), 0, cmds.getAttr(prev+".translateZ")])
        prev_vec = tuple([tmp_vec[j]-prev_tmp_vec[j] for j in range(3)])
        prev_length = math.sqrt(math.fsum([prev_vec[j]**2 for j in range(3)]))
        prev_vec = tuple([prev_vec[j]*1.5*length/prev_length for j in range(3)])
        prev_pt = tuple([tmp_vec[j]-prev_vec[j] for j in range(3)])
        sec_prev_pt = tuple([tmp_vec[j]-2.0/3*prev_vec[j] for j in range(3)])
        diff_height = float(self.getUnc(curr))*100+10
        att = ".translateY"
        val = -20
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateX", dv=prev_pt[0], v=val)
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateZ", dv=prev_pt[2], v=val)
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateX", dv=sec_prev_pt[0], v=diff_height)
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateZ", dv=sec_prev_pt[2], v=diff_height)
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateX", dv=tmp_vec[0], v=val)
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateZ", dv=tmp_vec[2], v=val)

        # make second directional vector off of change in coordinates between this track and next
        if "Sphere" in next[0]:
            next_tmp_vec = tuple([cmds.getAttr(next[0]+".translateX"), 0, cmds.getAttr(next[0]+".translateZ")])
        else:
            next_tmp_vec = tuple([cmds.getAttr(next+".translateX"), 0, cmds.getAttr(next+".translateZ")])
        next_vec = tuple([next_tmp_vec[j]-tmp_vec[j] for j in range(3)])
        next_length = math.sqrt(math.fsum([next_vec[j]**2 for j in range(3)]))
        next_vec = tuple([next_vec[j]*1.5*length/next_length for j in range(3)])
        next_pt = tuple([tmp_vec[j]+next_vec[j] for j in range(3)])
        sec_next_pt = tuple([tmp_vec[j]+2.0/3*next_vec[j] for j in range(3)])
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateX", dv=next_pt[0], v=val)
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateZ", dv=next_pt[2], v=val)
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateX", dv=sec_next_pt[0], v=diff_height)
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateZ", dv=sec_next_pt[2], v=diff_height)
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateX", dv=tmp_vec[0], v=val)
        cmds.setDrivenKeyframe(sphere[0]+att, cd=self._mainCam[0]+".translateZ", dv=tmp_vec[2], v=val)

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

    def clear(self):
        if len(self._spheres) > 0:
            for elem in self._spheres:
                cmds.delete(elem)
            self._spheres = list()
        if len(self._shaders) > 0:
            for elem in self._shaders:
                cmds.delete(elem)
            self._shaders = list()
        self._trackway = None
        self._startingTrack = None
        self._mainCam = None
        cmds.delete(self._trackWayCurve)
        self._trackWayCurve = None
        cmds.delete(self._baseTrackwayCurve)
        self._baseTrackwayCurve = None
        cmds.delete(self._motionPath)
        self._motionPath = None