import time
from bugster.auth.base_login import BaseLoginStrategy
from bugster.exceptions import BugsterLoginException


class UserInputLoginStrategy(BaseLoginStrategy):
    def __init__(self, instructions):
        """
        instructions: a list of dictionaries, each describing a step, e.g.:
        [
          {"action": "goto", "url": "/auth/sign-in"},
          {"action": "fill", "method": "placeholder", "value": "email", "text": "{email}"},
          ...
        ]

        The "{email}" or "{password}" can be template placeholders replaced at runtime.
        """
        self.instructions = instructions

    def run_login(self, page, credentials: dict, test_metadata):
        for instr in self.instructions:
            self.execute_step(page, instr, credentials, test_metadata)
            time.sleep(2)
        time.sleep(5)

    def execute_step(self, page, instr, credentials, test_metadata):
        action = instr["action"]
        if action == "goto":
            auth_url = test_metadata.get_auth_url()
            if not auth_url:
                base_url = test_metadata.get_base_url()
                page.goto(base_url + instr["url"])
            else:
                page.goto(auth_url)
        elif action == "fill":
            text = instr["text"]
            text = text.replace("{email}", credentials["email"]).replace(
                "{password}", credentials["password"]
            )
            locator = self.get_locator(page, instr)
            locator.click()
            locator.fill(text)
        elif action == "click":
            locator = self.get_locator(page, instr)
            locator.click()
        elif action == "save_assertion":
            text_to_assert = instr["input"]["text"]
            text_exists = False

            for attempt in range(2):
                time.sleep(5)
                body = page.query_selector("body")
                page_text = body.inner_text()
                text_exists = text_to_assert in page_text

                if text_exists:
                    break

            if not text_exists:
                raise BugsterLoginException("Expected text not found in login")

    def get_locator(self, page, instr):
        # Dynamically choose the locator method based on instructions
        method = instr.get("method")
        value = instr.get("value")
        if method == "placeholder":
            return page.get_by_placeholder(value)
        elif method == "label":
            return page.get_by_label(value)
        elif method == "role":
            return page.get_by_role(value, **instr.get("kwargs", {}))
        elif method == "text":
            return page.get_by_text(value, **instr.get("kwargs", {}))
        else:
            return page.locator(value)  # fallback to raw selector
