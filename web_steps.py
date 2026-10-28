from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@when('I click the "{button_text}" button')
def step_click_button(context, button_text):
    button = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()='{button_text}']"))
    )
    button.click()

@then('I should see "{name}" in the results')
def step_should_see_name(context, name):
    if hasattr(context, "results"):
        rendered = str(context.results)
        assert name in rendered, f"Expected '{name}' in results: {rendered}"
        return
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "search_results"), name)
    )
    assert found, f"Expected '{name}' in search results"

@then('I should not see "{name}" in the results')
def step_should_not_see_name(context, name):
    if hasattr(context, "results"):
        rendered = str(context.results)
        assert name not in rendered, f"Did not expect '{name}' in results: {rendered}"
        return
    results = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    assert name not in results.text, f"Did not expect '{name}' in search results"

@then('I should see the message "{message}"')
def step_should_see_message(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), message)
    )
    assert found, f"Expected message '{message}'"
