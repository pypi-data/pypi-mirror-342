class BugsterLoginException(Exception):
    """Exception raised for login errors."""

    code = "bugster_login_failed"

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(f"{self.code}: {self.detail}")
