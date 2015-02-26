__author__ = 'Wilson'

import nimble

from nimble import cmds

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
            if cmds.getAttr(next+'.cadence_widthUncertainty') > widthUnc and \
                cmds.getAttr(next+'.cadence_lengthUncertainty') > lengthUnc and \
                cmds.getAttr(next+'.cadence_rotationUncertainty') > rotUnc:
                return next
            next = cmds.getAttr(next+'.cadence_nextNode')

        return None

    def getPrevUnc(self, track, widthUnc, lengthUnc, rotUnc):
        prev = cmds.getAttr(track+'.cadence_prevNode')

        while prev != None:
            if cmds.getAttr(prev+'.cadence_widthUncertainty') > widthUnc and \
                cmds.getAttr(prev+'.cadence_lengthUncertainty') > lengthUnc and \
                cmds.getAttr(prev+'.cadence_rotationUncertainty') > rotUnc:
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