# TrackPropEnum.py
# (C)2013-2014
# Scott Ernst and Kent A. Stevens

from collections import namedtuple

from pyaid.reflection.Reflection import Reflection

#___________________________________________________________________________________________________ TRACK_PROP_NT
# A custom data type for track property enumerations that contain the following information:
#   * name      | Key for the track property in both the database and in Maya
#   * type      | The type of attribute for the track property within Maya
#   * intrinsic | True if the track property mirrors an existing property of a Maya transform nodeName
#   * unique    | Boolean specifying whether or not the property should be included in uniquely
#                 identified tracks within the database
TRACK_PROP_NT = namedtuple('TRACK_PROP_NT', ['name', 'type', 'maya', 'unique' ])

#___________________________________________________________________________________________________ TrackPropEnum
class TrackPropEnum(object):
    """ A class for all track properties encoded either as additional attributes of the Maya
        transform nodeName which represents a track (of type string or float) or computed from other
        'intrinsic' transform attributes such as scale, rotation, or translation. """

#===================================================================================================
#                                                                                       C L A S S

    # Fractional value specifying the front to center length over the total track length
    FORWARD_LENGTH_RATIO = TRACK_PROP_NT('forwardLengthRatio', 'float', None, False)

    # Community, site, year, level, sector, trackway
    COMM = TRACK_PROP_NT('community', 'string', None, True)

    # the depth of a given track (in cm) as originally measured
    DEPTH_MEASURED    = TRACK_PROP_NT('depthMeasured',    'float', None, False)
    DEPTH_UNCERTAINTY = TRACK_PROP_NT('depthUncertainty', 'float', None, False)

    # A 32bit integer containing enumerated flags for how the track should be displayed
    DISPLAY_FLAGS = TRACK_PROP_NT('flags', 'long', None, False)

    # A 32bit integer containing enumerated flags related to the state and type of the track
    FLAGS = TRACK_PROP_NT('flags', 'long', None, False)

    # The row index of the track entry in the source spreadsheet where the track data was imported
    INDEX = TRACK_PROP_NT('index', 'float', None, False)

    # a boolean indicating left versus right track, defaults to false if unknown
    LEFT = TRACK_PROP_NT('left', 'bool', None, True)

    # the length of a given track estimated from map, as previously measured, and uncertainty)
    # the center of the track is defined by the point of maximum width and length.  Note that the
    # length is measured from anterior to posterior intersection with the inner margin of the track,
    # and in hoof-shaped manus tracks the length is mostly anterior to the center, while in pes
    # tracks, the track has a longer heal region posterior to the point of maximum width.  The
    # center is thus offset a fraction (0.0 to 1.0) of the length measurement measured anteriorly,
    # and >0.5 for manus tracks, <0.5 for pes.  In terms of the Maya track node, the length measure
    # is offset in object-coordintes z by this fraction of the length (which is scaleZ).
    LENGTH             = TRACK_PROP_NT('length',            'float', 'length',            False)
    LENGTH_MEASURED    = TRACK_PROP_NT('lengthMeasured',    'float',  None,               False)
    LENGTH_UNCERTAINTY = TRACK_PROP_NT('lengthUncertainty', 'float', 'lengthUncertainty', False)

    # a given tracksite has multiple levels
    LEVEL = TRACK_PROP_NT('level', 'string', None, True)

    # UID of the next track in the track series, or an empty string if no next track exists
    NEXT = TRACK_PROP_NT('next', 'string', None, False)

    # a text note associated with a given track
    NOTE = TRACK_PROP_NT('note', 'string', None, False)

    # each track has a number (part of the 'name', such as the 3 in LM3 or the 15 in RP1)5
    NUMBER = TRACK_PROP_NT('number', 'string', None, True)

    # a boolean, true if the track is a pes (hind) print, not a manus, default is false if unknown
    PES = TRACK_PROP_NT('pes', 'bool', None, True)

    # rotation is measured relative to North (the world coordinates z-axis in the scene), and
    # increases counterclockwise.  It is an intrinsic attribute of the nodeName transform (rotation
    # about the 'vertical' y axis).
    ROTATION             = TRACK_PROP_NT('rotation',            'float', 'ry', False)
    ROTATION_MEASURED    = TRACK_PROP_NT('rotationMeasured',    'float', None, False)
    ROTATION_UNCERTAINTY = TRACK_PROP_NT('rotationUncertainty', 'float', None, False)

    # the specified sector for this track, at this site
    SECTOR = TRACK_PROP_NT('sector', 'string', None, True)

    # a given tracksite (BEB, TCH, etc.)
    SITE = TRACK_PROP_NT('site', 'string', None, True)

    # A serialized JSON string of that stores the last saved state of the track for reference
    SNAPSHOT = TRACK_PROP_NT('snapshot', 'string', None, False)

    # A 32bit integer containing enumerated flags related to how the track data was imported
    SOURCE_FLAGS = TRACK_PROP_NT('flags', 'long', None, False)

    # a trackway is numbered at a given site/level, and consists of four (for quadrupedal) or
    # two (bipedal) track series.
    TRACKWAY_NUMBER = TRACK_PROP_NT('trackwayNumber', 'string', None, True)

    # trackways are 'S' for sauropod, 'T' for theropod, 'tr' for tridactyl, and 'U' for unclassified
    TRACKWAY_TYPE = TRACK_PROP_NT('trackwayType', 'string', None, True)

    # Unique identifier for the track, created when the track is first created and never changed
    # for the lifetime of the track. The UID has no dependence upon any other track property
    UID = TRACK_PROP_NT('uid', 'string', 'track_uid', False)

    # the width of a given track, the value previously measured, and the uncertainty
    WIDTH             = TRACK_PROP_NT('width',            'float', 'sx', False)
    WIDTH_MEASURED    = TRACK_PROP_NT('widthMeasured',    'float', None, False)
    WIDTH_UNCERTAINTY = TRACK_PROP_NT('widthUncertainty', 'float', 'widthUncertainty', False)

    # the x coordinate of a given track (relative to tracksite's map origin) encoded in nodeName
    X = TRACK_PROP_NT('x', 'float', 'translateX', False)

    # the year of excavation of the tracksite of which this track belongs
    YEAR = TRACK_PROP_NT('year', 'string', None, False)

    # the z coordinate of a given track (relative to tracksite's map origin) encoded in nodeName
    Z = TRACK_PROP_NT('z', 'float', 'translateZ', False)

#___________________________________________________________________________________________________ TrackPropEnumOps
class TrackPropEnumOps(object):
    """ Support class for helper operations related to the TrackPropEnum class. """

#___________________________________________________________________________________________________ _getTrackPropEnum
    @classmethod
    def getTrackPropEnumByName(cls, name):
        """ Retrieves the TrackPropEnum enumerated value based on the name attribute. """

        for enum in Reflection.getReflectionList(TrackPropEnum):
            if enum.name == name:
                return enum
        return None
