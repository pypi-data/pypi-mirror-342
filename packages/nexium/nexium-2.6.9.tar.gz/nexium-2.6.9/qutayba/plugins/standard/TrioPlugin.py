


""" Deprecated trio plugin.
"""

from qutayba.plugins.PluginBase import nexiumPluginBase


class nexiumPluginTrio(nexiumPluginBase):
    plugin_name = "trio"
    plugin_desc = "Deprecated, was once required by the 'trio' package"
    plugin_category = "package-support,obsolete"

    @classmethod
    def isDeprecated(cls):
        return True



