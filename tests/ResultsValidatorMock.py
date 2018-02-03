class ResultsValidatorMock:
    def __init__(self) -> None:
        self.was_called = False

    def validate_params(self, params):
        self.was_called = True
        return []

    def validator_was_called(self):
        was_called = self.was_called
        self.was_called = False
        return was_called
