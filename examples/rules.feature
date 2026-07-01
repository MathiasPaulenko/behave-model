@auth
Feature: User Account Management
  As a registered user
  I want to manage my account
  So that my profile stays up to date

  Background:
    Given the user is logged in

  Rule: Profile updates
    Background:
      Given the user has a profile

    Scenario: Update display name
      When the user changes their display name to "Alice"
      Then the profile should show "Alice"

    Scenario: Update email
      When the user changes their email to "alice@example.com"
      Then the profile should show email "alice@example.com"

  Rule: Password management
    @security
    Scenario: Change password
      When the user changes their password
      Then the password should be updated

    Scenario Outline: Password validation
      When the user tries to set password "<password>"
      Then the validation should <result>

      Examples:
        | password  | result           |
        | short     | fail             |
        | longenough| succeed          |
        | 123       | fail             |
