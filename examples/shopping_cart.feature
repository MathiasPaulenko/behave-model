@shopping
Feature: Shopping Cart
  As a shopper
  I want to manage my cart
  So that I can purchase items

  @add
  Scenario: Add item to cart
    Given the cart is empty
    When the user adds "Widget" to the cart
    Then the cart should contain 1 item
    And the total should be $10.00

  @remove
  Scenario: Remove item from cart
    Given the cart contains "Widget"
    When the user removes "Widget" from the cart
    Then the cart should be empty

  @bulk
  Scenario Outline: Bulk discount for <quantity> items
    Given the cart has <quantity> items
    When the user checks out
    Then the discount should be <discount>%

    Examples:
      | quantity | discount |
      | 5        | 10       |
      | 10       | 20       |
      | 50       | 30       |
