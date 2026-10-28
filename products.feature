Feature: Product catalogue
  As a shopper
  I want to manage and search products
  So that I can find products in the catalogue

  Background:
    Given the following products
      | name    | description        | price | available | category  |
      | Hat     | A red fedora       | 59.95 | true      | CLOTHS    |
      | Shoes   | Running shoes      | 89.50 | false     | CLOTHS    |
      | Big Mac | A tasty burger     | 5.99  | true      | FOOD      |
      | Sheets  | Cotton bed sheets  | 25.00 | true      | HOUSEHOLD |

  Scenario: Read a product
    When I read the product named "Hat"
    Then I should see "A red fedora" in the results

  Scenario: Update a product
    When I update the product named "Hat" to "Fedora"
    Then I should see "Fedora" in the results

  Scenario: Delete a product
    When I delete the product named "Hat"
    Then I should not see "Hat" in the results

  Scenario: List all products
    When I list all products
    Then I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results

  Scenario: Search by category
    When I search by category "FOOD"
    Then I should see "Big Mac" in the results
    And I should not see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Sheets" in the results

  Scenario: Search by availability
    When I search for available products
    Then I should see "Hat" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results
    And I should not see "Shoes" in the results

  Scenario: Search by name
    When I search by name "Hat"
    Then I should see "Hat" in the results
