class NonLoadableSourceConfigurationPath(Exception):
    def __init__(self, filepath):
        super(NonLoadableSourceConfigurationPath, self).__init__(
            "Cannot load the configuration file for the source: {!r}".format(filepath))


class NonLoadableConfigurationPath(Exception):
    def __init__(self, filepath):
        super(NonLoadableConfigurationPath, self).__init__("Cannot load the configuration file: {!r}".format(filepath))
