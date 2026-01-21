import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger

logger = get_logger()


@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("admin", "admin123", "Login Successful"),
        ("admin", "wrong", "Invalid username or password"),
        ("wrong", "admin123", "Invalid username or password"),
    ],
)
def test_login(driver, username, password, expected):
    logger.info("Testing login functionality")

    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "loginBtn").click()

    wait = WebDriverWait(driver, 5)

    if expected == "Login Successful":
        assert expected in driver.page_source
    else:
        error = wait.until(
            EC.visibility_of_element_located((By.ID, "error"))
        ).text
        assert error == expected
