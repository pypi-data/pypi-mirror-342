import re
import time
import robocorp.log
from bs4 import BeautifulSoup


class PC:
    @staticmethod
    def login(username, password, passcodes, url, page, has_cookies=True):
        try:
            with robocorp.log.suppress_variables():
                page.goto(url)

                if has_cookies:
                    page.wait_for_selector("#CybotCookiebotDialogBodyButtonDecline")
                    page.locator("#CybotCookiebotDialogBodyButtonDecline").click()

                page.fill("#LocalizableTextField_CH_LOGINNAME", username)
                page.fill("#LocalizableUIPasswordField_CH_PASSWORD", password)
                page.click("id=LoginPageButton_BUTTON_NEXT")

                login_text = page.locator("#UIPasswordForm")
                text = login_text.text_content()
                passcode_number = re.findall(r"\d+", text)
                passcode = PC.get_passcode(passcode_number[0], passcodes)
                for i, char in enumerate(passcode):
                    locator = f"css=#UIPasswordForm .v-textfield:nth-child({i+1})"
                    page.fill(locator, char)

                page.click("id=LoginPageButton_c_log_in")
        except Exception as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_passcode(passcode_number, passcodes):

        soup = BeautifulSoup(passcodes, "html.parser")

        items = [td.text for td in soup.find_all("td")]
        passcodes_dict = {}
        # pylint:disable=consider-using-enumerate
        for i in range(len(items)):
            if items[i].isdigit():
                if i + 1 < len(items):
                    passcodes_dict[items[i]] = items[i + 1]

        return passcodes_dict.get(passcode_number)

    @staticmethod
    def switch_customer_view(page, customer):
        try:
            time.sleep(3)
            selector = "#ChangeCompanySelect .v-filterselect-input"
            page.wait_for_selector(selector, state="visible")
            page.fill(selector, "")
            page.type(selector, customer)
            time.sleep(3)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")
            time.sleep(5)

            customer_name = page.input_value(selector)
            result = str(customer).upper() in str(customer_name).upper()
            return SwitchViewResult(result)

        except Exception as e:
            raise RuntimeError("Error") from e


class SwitchViewResult:
    def __init__(self, result):
        self.result = result
        self.called_bool = False

    def bool(self):
        return self.result

    def __del__(self):
        if not self.called_bool:
            pass
