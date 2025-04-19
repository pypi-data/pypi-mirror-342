class APIResponseError(Exception):
    pass


class APIHealthCheckFailedError(Exception):
    pass


class APIDataNotAvailableError(Exception):
    pass


class TrackInitializationError(Exception):
    pass


class DBTrackInitializationError(TrackInitializationError):
    pass


class TrackTransformationError(Exception):
    pass


class InvalidBoundsError(Exception):
    pass


class GPXPointExtensionError(Exception):
    pass


class VisualizationSetupError(Exception):
    pass


class TrackAnalysisError(Exception):
    pass


class VisualizationSetupWarning(Warning):
    pass
