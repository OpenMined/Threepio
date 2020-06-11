class TranslationMissing(Exception):
    def __init__(self, name):
        super().__init__(
            f"Translation for the command {name} is not currently supported"
        )


class NotTranslated(Exception):
    def __init__(self):
        super().__init__("Translation must be completed before executing")
