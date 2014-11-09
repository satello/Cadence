# CadenceCompiler.py
# (C)2013
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyglass.compile.PyGlassApplicationCompiler import PyGlassApplicationCompiler
from pyglass.compile.SiteLibraryEnum import SiteLibraryEnum

from cadence.CadenceApplication import CadenceApplication

#___________________________________________________________________________________________________ CadenceCompiler
class CadenceCompiler(PyGlassApplicationCompiler):
    """A class for..."""

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: siteLibraries
    @property
    def siteLibraries(self):
        return [SiteLibraryEnum.PYSIDE, SiteLibraryEnum.SQL_ALCHEMY]

#___________________________________________________________________________________________________ GS: binPath
    @property
    def binPath(self):
        return ['..', '..', 'bin']

#___________________________________________________________________________________________________ GS: appFilename
    @property
    def appFilename(self):
        return 'Cadence'

#___________________________________________________________________________________________________ GS: appDisplayName
    @property
    def appDisplayName(self):
        return 'Cadence'

#___________________________________________________________________________________________________ GS: applicationClass
    @property
    def applicationClass(self):
        return CadenceApplication

#___________________________________________________________________________________________________ GS: iconPath
    @property
    def iconPath(self):
        return ['apps', 'Cadence']

####################################################################################################
####################################################################################################

if __name__ == '__main__':
    CadenceCompiler().run()

