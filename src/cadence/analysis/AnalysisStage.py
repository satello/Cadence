# AnalysisStage.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

from pyaid.config.ConfigsDict import ConfigsDict

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

#*************************************************************************************************** AnalysisStage
class AnalysisStage(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, key, owner, **kwargs):
        """Creates a new instance of AnalysisStage."""
        self.owner = owner

        self._key   = key
        self._cache = ConfigsDict()

        self._analyzeCallback   = kwargs.get('analyze')
        self._preStageCallback  = kwargs.get('pre')
        self._postStageCallback = kwargs.get('post')
        self._sitemapCallback   = kwargs.get('sitemap')
        self._seriesCallback    = kwargs.get('series')
        self._trackwayCallback  = kwargs.get('trackway')
        self._trackCallback     = kwargs.get('track')

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: key
    @property
    def key(self):
        return self._key

#___________________________________________________________________________________________________ GS: index
    @property
    def index(self):
        try:
            return self.owner.stages.index(self)
        except Exception:
            return -1

#___________________________________________________________________________________________________ GS: cache
    @property
    def cache(self):
        return self._cache

#___________________________________________________________________________________________________ GS: logger
    @property
    def logger(self):
        return self.owner.logger

#___________________________________________________________________________________________________ GS: plot
    @property
    def plot(self):
        return plt

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ getPath
    def getPath(self, *args, **kwargs):
        """getPath doc..."""
        return self.owner.getPath(*args, **kwargs)

#___________________________________________________________________________________________________ GS: getTempPath
    def getTempPath(self, *args, **kwargs):
        return self.owner.getTempPath(*args, **kwargs)

#___________________________________________________________________________________________________ analyze
    def analyze(self):
        """analyze doc..."""
        self._preAnalyze()
        self._analyze()
        self._postAnalyze()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _preAnalyze
    def _preAnalyze(self):
        """_preAnalyze doc..."""
        if self._preStageCallback:
            self._preStageCallback(self)

#___________________________________________________________________________________________________ _postAnalyze
    def _postAnalyze(self):
        """_postAnalyze doc..."""
        if self._postStageCallback:
            self._postStageCallback(self)

#___________________________________________________________________________________________________ _analyze
    def _analyze(self):
        """_analyze doc..."""

        if self._analyzeCallback and not self._analyzeCallback(self):
            return

        for sitemap in self.owner.getSitemaps():
            self._analyzeSitemap(sitemap)

#___________________________________________________________________________________________________ _analyzeSitemap
    def _analyzeSitemap(self, sitemap):
        """_analyze doc..."""

        if self._sitemapCallback and not self._sitemapCallback(self, sitemap):
            return

        for tw in self.owner.getTrackways(sitemap, loadHidden=self.owner.loadHidden):
            self._analyzeTrackway(tw)

#___________________________________________________________________________________________________ _analyzeTrackway
    def _analyzeTrackway(self, trackway):
        """_analyzeTrackway doc..."""

        if self._trackwayCallback and not self._trackwayCallback(self, trackway):
            return

        for s in trackway.seriesList:
            self._analyzeTrackSeries(s)

#___________________________________________________________________________________________________ _analyzeTrackSeries
    def _analyzeTrackSeries(self, series):
        """_analyzeTrackSeries doc..."""
        if not series:
            return

        if self._seriesCallback and not self._seriesCallback(self, series):
            return

        for t in series.tracks:
            self._analyzeTrack(t)

#___________________________________________________________________________________________________ _analyzeTrack
    def _analyzeTrack(self, track):
        """_analyzeTrack doc..."""
        if self._trackCallback:
            self._trackCallback(self, track)

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__

