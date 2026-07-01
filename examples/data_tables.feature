Feature: Data Tables
  As a developer
  I want to use data tables
  So that I can pass structured data to steps

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
