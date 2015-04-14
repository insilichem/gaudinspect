import chimera.extension


class GAUDInspectEMO(chimera.extension.EMO):

    def name(self):
        return "GAUDInspect"

    def description(self):
        return "Evaluate your system in realtime with the power of GAUDI"

    def categories(self):
        return ['GAUDI']

    def activate(self):
        self.module('gui').showUI()
        return None

emo = GAUDInspectEMO(__file__)
chimera.extension.manager.registerExtension(emo)
