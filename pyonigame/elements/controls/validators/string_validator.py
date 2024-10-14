class StringValidator:
    def validate(self, value: str) -> bool:
        if value != "":
            return True
        return False
