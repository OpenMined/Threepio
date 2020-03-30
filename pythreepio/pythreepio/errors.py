class TranslationMissing(Exception):
    def __init__(self, message):
        super().__init__(
            f'Translation for the command {message} is not currently supported'
        )


class NotTranslated(Exception):
    def __init__(self):
        super().__init__(
            'Translation must be completed before executing'
        )
