class TranslationMissing(Exception):
    """Exception for commands which currently do not support translation."""

    def __init__(self, name):
        super().__init__(
            f"Translation for the command {name} is not currently supported"
        )
