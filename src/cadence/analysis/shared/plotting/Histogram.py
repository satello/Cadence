# Histogram.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division
from pyaid.ArgsUtils import ArgsUtils

from cadence.analysis.shared.plotting.SinglePlotBase import SinglePlotBase

#*************************************************************************************************** Histogram
class Histogram(SinglePlotBase):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of Histogram."""
        ArgsUtils.addIfMissing('yLabel', 'Frequency', kwargs)
        super(Histogram, self).__init__(**kwargs)
        self.color      = kwargs.get('color', 'b')
        self.binCount   = kwargs.get('binCount', 100)
        self.data       = kwargs.get('data', [])
        self.isLog      = kwargs.get('isLog', False)

#===================================================================================================
#                                                                               P R O T E C T E D


#___________________________________________________________________________________________________ _plot
    def _plot(self):
        """_plot doc..."""
        pl = self.pl
        pl.hist(self.data, self.binCount, range=self.xLimits, facecolor=self.color, log=self.isLog)
        pl.title(self.title)
        pl.xlabel(self.xLabel)
        pl.ylabel(self.yLabel)
        if self.xLimits:
            pl.xlim(*self.xLimits)
        if self.yLimits:
            pl.ylim(*self.yLimits)
        pl.grid(True)
