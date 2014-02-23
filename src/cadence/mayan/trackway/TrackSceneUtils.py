# TrackSceneUtils.py
# (C)2014
# Scott Ernst

import math

from nimble import cmds

from pyaid.reflection.Reflection import Reflection

from cadence.CadenceEnvironment import CadenceEnvironment
from cadence.enum.TrackPropEnum import TrackPropEnum

#___________________________________________________________________________________________________ TrackSceneUtils
class TrackSceneUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    TRACK_RADIUS = 50
    Y_VEC  = (0, 1, 0)

#___________________________________________________________________________________________________ createTrackNode
    @classmethod
    def createTrackNode(cls, uid, trackSetNode =None, props =None):
        if not trackSetNode:
            trackSetNode = TrackSceneUtils.getTrackSetNode()
        if not trackSetNode:
            return None

        node = cls.getTrackNode(uid, trackSetNode=trackSetNode)
        if node:
            return node

        a    = 2.0*cls.TRACK_RADIUS
        node = cmds.polyCylinder(
            r=cls.TRACK_RADIUS,
            h=5,
            sx=40,
            sy=1,
            sz=1,
            ax=cls.Y_VEC,
            rcp=0,
            cuv=2,
            ch=1,
            n='track0')[0]

        p = cmds.polyPrism(
            l=4, w=a, ns=3, sh=1, sc=0, ax=cls.Y_VEC, cuv=3, ch=1, n='pointer')[0]

        cmds.rotate(0.0, -90.0, 0.0)
        cmds.scale(1.0/math.sqrt(3.0), 1.0, 1.0)
        cmds.move(0, 5, a/6.0)

        cmds.setAttr(p + '.overrideEnabled', 1)
        cmds.setAttr(p + '.overrideDisplayType', 2)

        cmds.parent(p, node)

        cmds.select(node)
        cmds.addAttr(
            longName='cadence_uniqueId',
            shortName=TrackPropEnum.UID.maya,
            dataType='string',
            niceName='Unique ID')

        # Add the new node to the Cadence track scene set
        cmds.sets(node, add=trackSetNode)

        if props:
            cls.setTrackProps(node, props)

        return node

#___________________________________________________________________________________________________ getTrackNode
    @classmethod
    def getTrackNode(cls, uid, trackSetNode =None):
        trackSetNode = TrackSceneUtils.getTrackSetNode() if not trackSetNode else trackSetNode
        if not trackSetNode:
            return None

        nodes = cmds.sets(trackSetNode, query=True)
        if not nodes:
            return None

        for node in nodes:
            if not cmds.hasAttr(node + '.' + TrackPropEnum.UID.maya):
                continue
            if uid == cmds.getAttr(node + '.' + TrackPropEnum.UID.maya):
                return node

        return None

#___________________________________________________________________________________________________ checkNodeUidMatch
    @classmethod
    def checkNodeUidMatch(cls, uid, node):
        try:
            return uid == cmds.getAttr(node + '.' + TrackPropEnum.UID.maya)
        except Exception, err:
            return False

#___________________________________________________________________________________________________ getTrackProps
    @classmethod
    def getTrackProps(cls, node):
        out = dict()
        for enum in Reflection.getReflectionList(TrackPropEnum):
            if enum.maya is None:
                continue
            out[enum.name] = cmds.getAttr(node + '.' + enum.maya)
        return out

#___________________________________________________________________________________________________ setTrackProps
    @classmethod
    def setTrackProps(cls, node, props):
        for enum in Reflection.getReflectionList(TrackPropEnum):
            if enum.maya and enum.maya in props:
                if enum.type == 'string':
                    cmds.setAttr(node + '.' + enum.maya, props[enum.maya], type=enum.type)
                else:
                    cmds.setAttr(node + '.' + enum.maya, props[enum.maya])

#___________________________________________________________________________________________________ getTrackManagerNode
    @classmethod
    def getTrackManagerNode(cls, trackSetNode =None, createIfMissing =False):
        """ Returns the name of the track manager node for the current Cadence scene.

            trackSetNode: The track set node on which to find the track manager node. If no node
                    is specified the method will look it up internally.

            createIfMissing: If true and no track manager node is found one will be created and
                    connected to the track set node, which will also be created if one does
                    not exist. """

        if not trackSetNode:
            trackSetNode = cls.getTrackSetNode(createIfMissing=createIfMissing)

        connects = cmds.listConnections(trackSetNode + '.usedBy', source=True, destination=False)
        if connects:
            for node in connects:
                if cmds.nodeType(node) == 'trackManager':
                    return node

        if createIfMissing:
            node = cmds.createNode('trackManager')
            cmds.connectAttr(node + '.trackSet', trackSetNode + '.usedBy', force=True)
            return node

        return None

#___________________________________________________________________________________________________ getTrackSetNode
    @classmethod
    def getTrackSetNode(cls, createIfMissing =False):
        for node in cmds.ls(exactType='objectSet'):
            if node == CadenceEnvironment.TRACKWAY_SET_NODE_NAME:
                return node

        if createIfMissing:
            return cmds.sets(name=CadenceEnvironment.TRACKWAY_SET_NODE_NAME, empty=True)

        return None
