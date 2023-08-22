from behave import given, when, then
from django.conf import settings
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from functional_tests.base import wait
from functional_tests.management.commands.create_session import create_pre_authentication_session


@wait
def wait_for_list_item(context, item_text):
    context.test.assertIn(item_text, context.browser.find_element(by=By.ID, value="id_list_table").text)


def add_item(context, item_text):
    print(f"add item: {item_text}")
    inputbox = context.browser.find_element(by=By.ID, value="id_text")
    inputbox.send_keys(item_text)
    inputbox.send_keys(Keys.ENTER)
    wait_for_list_item(context, item_text)


@given('I am a logged-in user')
def given_i_am_logged_in(context):
    """При условии, что я являюсь зарегистрированным пользователем"""
    session_key = create_pre_authentication_session(email="edith@example.com")
    # Установить cookie, которые нужны для первого посещения домена.
    # Страницы 404 загружаются быстрее всего
    context.browser.get(context.get_url("/404_no_such_url/"))
    context.browser.add_cookie(dict(
        name=settings.SESSION_COOKIE_NAME,
        value=session_key,
        path="/"
    ))


@when('I create a list with first item "{first_item_text}"')
def create_a_list(context, first_item_text):
    context.browser.get(context.get_url("/"))
    add_item(context, first_item_text)


@when('I add an item "{item_text}"')
def add_an_item(context, item_text):
    add_item(context, item_text)


@then('I will see a link to "{link_text}"')
@wait
def see_a_link(context, link_text):
    link = context.browser.find_element(by=By.LINK_TEXT, value=link_text)
    context.test.assertIsNotNone(link)


@when('I click the link to "{link_text}"')
def click_link(context, link_text):
    context.browser.find_element(by=By.LINK_TEXT, value=link_text).click()


@then('I will be on the "{first_item_text}" list page')
@wait
def on_list_page(context, first_item_text):
    first_row = context.browser.find_element(by=By.CSS_SELECTOR, value="#id_list_table tr:first-child")
    expected_row_text = f"1: {first_item_text}"
    context.test.assertEqual(first_row.text, expected_row_text)
