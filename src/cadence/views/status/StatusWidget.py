# StatusWidget.py
# (C)2014
# Scott Ernst

from PySide import QtGui

from pyglass.widgets.PyGlassWidget import PyGlassWidget

#___________________________________________________________________________________________________ StatusWidget
class StatusWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of StatusWidget."""
        super(StatusWidget, self).__init__(parent, **kwargs)

        self._animatedIcon = QtGui.QMovie(self.getResourcePath('loader.gif'))
        self.iconLabel.setMovie(self._animatedIcon)

        self.statusText.setReadOnly(True)

        self.target    = None
        self.isShowing = False

        self.closeBtn.clicked.connect(self._handleClose)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: header
    @property
    def header(self):
        return self.headerLabel.text()
    @header.setter
    def header(self, value):
        self.headerLabel.setText(value)

#___________________________________________________________________________________________________ GS: info
    @property
    def info(self):
        return self.infoLabel.text()
    @info.setter
    def info(self, value):
        if value is None:
            self.infoLabel.setVisible(False)
            return

        self.infoLabel.setVisible(True)
        self.infoLabel.setText(value)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ clear
    def clear(self):
        self.statusText.clear()

#___________________________________________________________________________________________________ append
    def append(self, text):
        self.statusText.append(text)

#___________________________________________________________________________________________________ showStatusDone
    def showStatusDone(self):
        self.iconLabel.setVisible(False)
        self.closeBtn.setEnabled(True)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _activateWidgetDisplayImpl
    def _activateWidgetDisplayImpl(self, **kwargs):
        self.closeBtn.setEnabled(False)
        self.iconLabel.setVisible(True)
        self.isShowing = True
        self._animatedIcon.start()

#___________________________________________________________________________________________________ _deactivateWidgetDisplayImpl
    def _deactivateWidgetDisplayImpl(self, **kwargs):
        self.isShowing = False
        self._animatedIcon.stop()

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleClose
    def _handleClose(self):
        self.mainWindow.hideStatus(self.target)
