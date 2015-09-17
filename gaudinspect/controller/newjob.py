#!/usr/bin/python
# -*- coding: utf-8 -*-


class GAUDInspectNewJobController(object):

    FIELDS = {
        'general_generations_field': ('ga', 'gens'),
        'general_population_field': ('ga', 'pop'),
        'general_project_field': ('general', 'name'),
        'general_outputpath_field': ('general', 'outputpath')
    }

    def __init__(self, view, model=None):
        self.model = model
        self.view = view
        self.form = self.view.tabber.tabs[0]
        if model:
            self.set_model(model)

    def set_model(self, model):
        self.model = model
        self._fill_view()

    def _fill_view(self):
        if not self.model:
            return

        for k, (v, w) in self.FIELDS.items():
            getattr(self.form, k).setText(str(self.model.gaudidata[v][w]))

        for gene in self.model.gaudidata['genes']:
            self.form.genes_list.addItem(
                '{} ({})'.format(gene['name'], gene['type']))

        for obj in self.model.gaudidata['objectives']:
            self.form.objectives_list.addItem(
                '{} ({})'.format(obj['name'], obj['type']))

    def export(self):
        self.model.export()
