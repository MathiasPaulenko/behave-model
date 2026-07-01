"""Shared fixtures and test data."""

from __future__ import annotations

from pathlib import Path

import pytest

from behave_model.parser.adapter import BehaveParserAdapter
from behave_model.parser.parser import parse_feature

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"

LOGIN_FEATURE = """\
@smoke @auth
Feature: Login
  As a user
  I want to log in
  So that I can access the system

  Background:
    Given a database connection
    And the web server is running

  @happy
  Scenario: Successful login
    Given the user is on the login page
    When the user enters "admin" and "password"
    Then the user should be logged in
    And the dashboard should be visible

  @error
  Scenario: Failed login with wrong password
    Given the user is on the login page
    When the user enters "admin" and "wrong"
    Then the user should see an error message
    And the user should not be logged in

  @api
  Scenario Outline: Login with role <role>
    Given the user is a <role>
    When the user logs in with <password>
    Then access should be <result>

    Examples:
      | role  | password | result  |
      | admin | secret   | granted |
      | user  | pass     | granted |
      | guest | unknown  | denied  |
"""

SHOPPING_FEATURE = """\
@shopping
Feature: Shopping Cart
  As a shopper
  I want to manage my cart

  @add
  Scenario: Add item to cart
    Given the cart is empty
    When the user adds "Widget" to the cart
    Then the cart should contain 1 item

  @bulk
  Scenario Outline: Bulk discount for <quantity> items
    Given the cart has <quantity> items
    When the user checks out
    Then the discount should be <discount>%

    Examples:
      | quantity | discount |
      | 5        | 10       |
      | 10       | 20       |
"""

DATA_TABLE_FEATURE = '''\
Feature: Data Tables
  As a developer
  I want to use data tables

  Scenario: User registration with data table
    Given the following users:
      | name  | email          | age |
      | Alice | alice@test.com | 30  |
      | Bob   | bob@test.com   | 25  |
    When the system processes the registrations
    Then all users should be registered

  Scenario: Step with docstring
    Given a JSON payload:
      """
      {"user": "admin", "action": "login"}
      """
    When the API receives the payload
    Then the response should be valid
'''


def _make_feature(text: str, filename: str = "test.feature"):
    """Parse text and adapt it to the domain model."""
    behave_feature = parse_feature(text, filename=filename)
    adapter = BehaveParserAdapter()
    return adapter.adapt_feature(behave_feature, filename=filename)


@pytest.fixture
def login_feature():
    """Return a parsed Login feature."""
    return _make_feature(LOGIN_FEATURE, "login.feature")


@pytest.fixture
def shopping_feature():
    """Return a parsed Shopping Cart feature."""
    return _make_feature(SHOPPING_FEATURE, "shopping_cart.feature")


@pytest.fixture
def data_table_feature():
    """Return a parsed Data Tables feature."""
    return _make_feature(DATA_TABLE_FEATURE, "data_tables.feature")


@pytest.fixture
def sample_project(login_feature, shopping_feature):
    """Return a project with two features."""
    from behave_model.model.project import Project

    return Project(features=[login_feature, shopping_feature])


@pytest.fixture
def examples_dir():
    """Return the path to the examples directory."""
    return EXAMPLES_DIR
