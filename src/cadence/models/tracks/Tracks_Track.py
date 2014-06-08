# Tracks_Track.py
# (C)2013-2014
# Scott Ernst and Kent A. Stevens

import nimble
from nimble import cmds

from cadence.mayan.trackway import GetTrackNodeData
from cadence.mayan.trackway import UpdateTrackNode
from cadence.mayan.trackway import CreateTrackNode
from cadence.models.tracks.TracksDefault import TracksDefault

#___________________________________________________________________________________________________ Tracks_Track
class Tracks_Track(TracksDefault):
    """ Database model representation of a track with all the attributes and information for a
        specific track as well connectivity information for the track within its series. """

#===================================================================================================
#                                                                                       C L A S S

    __tablename__  = u'tracks'

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: nodeName
    @property
    def nodeName(self):
        """ A cached value for the name of the Maya nodeName representing this track if one exists,
            which is updated each time a create/update operation on the nodeName occurs. Can be
            incorrect if the nodeName was renamed between such operations. """
        return self.fetchTransient('nodeName')
    @nodeName.setter
    def nodeName(self, value):
        self.putTransient('nodeName', value)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ createNode
    def createNode(self):
        """ Create a visual representation of a track, to signify the position, dimensions (length
            and width), and rotation of either a manus or pes print.  The representation has
            basic dimensions of one meter so that the scale in x and z equates to the width and
            length of the manus or pes in fractional meters (e.g., 0.5 = 50 cm).  The node is
            prohibited from changing in y (elevation) or to rotate about either x or z. """
        conn = nimble.getConnection()
        out  = conn.runPythonModule(
            CreateTrackNode,
            uid=self.uid,
            props=self.toMayaNodeDict(),
            runInMaya=True)
        if not out.success:
            print 'Error in CreateNode:', out.error
            return None

        self.nodeName = out.payload.get('nodeName')

        return self.nodeName

#___________________________________________________________________________________________________ updateNode
    def updateNode(self):
        """ Sends values to Maya nodeName representation of the track to synchronize the values in
            the model and the nodeName. """
        conn = nimble.getConnection()
        result = conn.runPythonModule(UpdateTrackNode, uid=self.uid, props=self.toMayaNodeDict())
        if not result.success:
            return False

        self.nodeName = result.payload.get('nodeName')
        return True

#___________________________________________________________________________________________________ updateFromNode
    def updateFromNode(self):
        """ Retrieves Maya values from the nodeName representation of the track and updates this
            model instance with those values. """
        conn = nimble.getConnection()
        result = conn.runPythonModule(GetTrackNodeData, uid=self.uid, nodeName=self.nodeName)
        if result.payload.get('error'):
            print 'Error in updateFromNode:', result.payload.get('message')
            return False

        self.nodeName = result.payload.get('nodeName')

        if self.nodeName:
            self.fromDict(result.payload.get('props'))
            return True

        return False


