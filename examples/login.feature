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
      | admin | secret   | granted  |
      | user  | pass     | granted  |
      | guest | unknown  | denied  |
