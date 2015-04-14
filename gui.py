
import chimera
from chimera.baseDialog import ModelessDialog
from chimera import tkgui, triggerSet
import Tkinter
import Pmw
import Tix

import base
import gaudi


ui = None


def showUI(callback=None):
    global ui
    if not ui:
        ui = GAUDInspectDialog()
    ui.enter()
    if callback:
        ui.addCallback(callback)


class GAUDInspectDialog(ModelessDialog):
    buttons = ("OK", "Close")
    default = None
    help = "https://bitbucket.org/jrgp/gaudinspect"
    SELECTION_CHANGED = "GAUDInspectSelectionChanged"
    DBL_CLICK = "GAUDInspectDoubleClick"
    EXIT = "GAUDInspectExited"

    def __init__(self, *args, **kw):

        # GUI init
        self.title = 'GAUDInspect'
        ModelessDialog.__init__(self)
        chimera.extension.manager.registerInstance(self)
        print self.title, "GUI entered"
