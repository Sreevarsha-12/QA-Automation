from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger

logger = get_logger()


def test_forgot_password(driver):
    logger.info("Testing forgot password functionality")

    driver.get("http://127.0.0.1:5000/forgot-password")

    driver.find_element(By.ID, "email").send_keys("test@example.com")
    driver.find_element(By.ID, "resetBtn").click()

    message = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "message"))
    ).text

    assert "Password reset link sent to" in message
