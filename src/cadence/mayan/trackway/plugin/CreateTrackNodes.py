# CreateTrackNodes.py
# (C)2013-2014
# Kent A. Stevens and Scott Ernst

from nimble import NimbleScriptBase
from pyaid.dict.DictUtils import DictUtils
from cadence.enum.TrackPropEnum import TrackPropEnum

from cadence.mayan.trackway.TrackSceneUtils import TrackSceneUtils

#___________________________________________________________________________________________________ CreateTrackNodes
class CreateTrackNodes(NimbleScriptBase):
    """ TODO: Kent... """

#===================================================================================================
#                                                                                       C L A S S

    NO_TRACKLIST = u'noTrackList'

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self, *args, **kwargs):
        trackList     = self.fetch('trackList', None)
        if not trackList:
            self.putErrorResult(
                u'No trackList specified. Unable to create tracks.',
                code=self.NO_TRACKLIST)
            return

        trackSetNode  = TrackSceneUtils.getTrackSetNode(createIfMissing=True)
        trackNodeList = dict()
        for track in trackList:
            uid = track.get(TrackPropEnum.UID.maya)
            if not uid:
                continue
            print 'TRACK:', DictUtils.prettyPrint(track)
            trackNodeList[uid] = TrackSceneUtils.createTrackNode(uid, trackSetNode, track)
        self.put('nodes', trackNodeList)

