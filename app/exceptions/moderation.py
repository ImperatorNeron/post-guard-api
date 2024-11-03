class ModerationResponseError(Exception):
    """Error parsing the moderation JSON response."""

    def __init__(
        self,
        message="Unable to process the moderation response. Invalid JSON format.",
    ):
        super().__init__(message)
