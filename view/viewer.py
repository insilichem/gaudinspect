#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide.QtCore import Qt
from chemlab.graphics import QChemlabWidget, colors
from chemlab.graphics.renderers import BallAndStickRenderer

from chemlab.graphics.postprocessing import SSAOEffect
from chemlab.graphics.postprocessing import OutlineEffect
from chemlab.graphics.postprocessing import FXAAEffect


def get(context, parent=None):
    return GAUDInspectViewViewer(context, parent)


class GAUDInspectViewViewer(QChemlabWidget):

    def __init__(self, context, parent=None):
        super(GAUDInspectViewViewer, self).__init__(context, parent)
        self.parent = parent
        context.makeCurrent()
        self.initializeGL()
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(400)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Preferred)
        self.background_color = (0, 0, 0, 0)

    def add_molecule(self, positions, types, bonds, color=colors.default_atom_map):
        r = BallAndStickRenderer(
            self, positions, types, bonds, color_scheme=color)
        self.renderers.append(r)

    def clear_view(self):
        self.renderers = []

    # Redefine some QChemlabWidget methods
    def mouseMoveEvent(self, evt):
        if self._last_mouse_right:
            # Panning
            if bool(evt.buttons() & Qt.RightButton):
                x, y = self._last_mouse_pos.x(), self._last_mouse_pos.y()
                x2, y2 = evt.pos().x(), evt.pos().y()
                self._last_mouse_pos = evt.pos()

                # Converting to world coordinates
                w = self.width()
                h = self.height()

                x, y = 2 * float(x) / w - 1.0, 1.0 - 2 * float(y) / h
                x2, y2 = 2 * float(x2) / w - 1.0, 1.0 - 2 * float(y2) / h
                dx, dy = x2 - x, y2 - y

                cam = self.camera

                cam.position += (-cam.a * dx + -cam.b * dy)
                cam.pivot += (-cam.a * dx + -cam.b * dy)
                self.update()

        if self._last_mouse_left:
            # Orbiting Rotation
            if bool(evt.buttons() & Qt.LeftButton):
                x, y = self._last_mouse_pos.x(), self._last_mouse_pos.y()
                x2, y2 = evt.pos().x(), evt.pos().y()
                self._last_mouse_pos = evt.pos()

                # Converting to world coordinates
                w = self.width()
                h = self.height()

                x, y = float(x) / w - 1.0, 1.0 - float(y) / h
                x2, y2 = float(x2) / w - 1.0, 1.0 - float(y2) / h
                dx, dy = x2 - x, y2 - y

                cam = self.camera
                cam.mouse_rotate(dx, dy)

                self.update()

    def mouseDoubleClickEvent(self, evt):
        if self._last_mouse_left:
            if bool(evt.buttons() & Qt.LeftButton):
                if self.post_processing:
                    self.disable_effects()
                else:
                    self.enable_effects()

    def add_post_processing(self, klass, *args, **kwargs):
        pp = klass(self, *args, **kwargs)
        self.post_processing.append(pp)
        return pp

    def enable_effects(self):
        # better illumination
        self.add_post_processing(
            SSAOEffect, kernel_size=128, kernel_radius=1.0)
        self.add_post_processing(OutlineEffect)  # black outlines
        self.add_post_processing(FXAAEffect)  # fast antialiasing
        self.update()

    def disable_effects(self):
        del self.post_processing[:]
        self.update()
