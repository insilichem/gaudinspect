#!/usr/bin/python
# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide.QtCore import Qt

import numpy as np

from chemlab.graphics import QChemlabWidget, colors
from chemlab.graphics.renderers import BallAndStickRenderer, AtomRenderer
from chemlab.graphics.postprocessing import SSAOEffect, OutlineEffect, FXAAEffect
from chemlab.io import datafile


def get(context, parent=None):
    return GAUDInspectViewViewer(context, parent)


class GAUDInspectViewViewer(QChemlabWidget):
    RENDERERS = {
        'ballandstick': BallAndStickRenderer,
        'sphere': AtomRenderer
    }

    COLORS = {
        'default': colors.default_atom_map,
        'light': colors.light_atom_map
    }

    def __init__(self, context, parent=None):
        super(GAUDInspectViewViewer, self).__init__(context, parent)
        self.parent = parent
        self.molecules = {}
        context.makeCurrent()
        self.initializeGL()
        self.initUI()

    def initUI(self):
        self.setMinimumWidth(500)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Preferred)
        self.background_color = (0, 0, 0, 0)

    # Controller methods
    def add_molecule(self, path, renderer='ballandstick',
                     color='default', cache=True):
        try:
            mol = self.molecules[path]
        except KeyError:
            mol = self.molecules[path] = datafile(path).read('molecule')
            mol.renderer = self.RENDERERS[renderer](
                self, mol.r_array, mol.type_array, color_scheme=self.COLORS[color])
        self.renderers.append(mol.renderer)
        self.update()

    def focus(self, molecules=None):
        if not molecules:
            molecules = self.molecules.keys()
        coords = []
        for m in molecules:
            coords.append(self.molecules[m].r_array)
        self.camera.autozoom(np.concatenate(coords))

    def clear(self):
        del self.renderers[:]

    def _clear_cache(self):
        self.molecules.clear()

    # ####
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
        if self.renderers:
            self.add_post_processing(
                SSAOEffect, kernel_size=128, kernel_radius=1.0)
            self.add_post_processing(
                OutlineEffect, color=(0, 0, 0))  # black outlines
            self.add_post_processing(FXAAEffect)  # fast antialiasing
            self.update()
            self.parent.status('Enabled effects')

    def disable_effects(self):
        if self.renderers:
            del self.post_processing[:]
            self.update()
            self.parent.status('Disabled effects')
