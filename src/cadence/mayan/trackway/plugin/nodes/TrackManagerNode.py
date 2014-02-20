# TrackManagerNode.py
# (C)2014
# Scott Ernst

from maya import OpenMaya
from maya import OpenMayaMPx

from elixir.nodes.ElixirNode import ElixirNode
from elixir.nodes.attrs.MessageNodeAttribute import MessageNodeAttribute
from elixir.nodes.attrs.NumericNodeAttribute import NumericNodeAttribute

#___________________________________________________________________________________________________ TrackManagerNode
class TrackManagerNode(ElixirNode):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    NODE_NAME       = 'trackManager'
    NODE_ID         = 0x3F3F3F
    NODE_TYPE       = OpenMayaMPx.MPxNode.kDependNode
    NODE_LOCATION   = 'utility/general'

    input  = NumericNodeAttribute(
        'i', 'input', 0, OpenMaya.MFnNumericData.kInt, affects='output')
    output = NumericNodeAttribute(
        'o', 'output', 0, OpenMaya.MFnNumericData.kInt, compute='outputCompute')
    tracks = MessageNodeAttribute('ts', 'trackSet')

#___________________________________________________________________________________________________ __init__
    def __init__(self):
        """Creates a new instance of TrackManagerNode."""
        ElixirNode.__init__(self)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ outputCompute
    def outputCompute(self, data):
        value = data.inHandles.input.asInt()
        data.outHandles.output.setInt(2*value)
        data.outHandles.cleanAll()


