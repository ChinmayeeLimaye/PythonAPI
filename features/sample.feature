      Feature:Bank Transactions

        Scenario: Withdrawl of money
          Given the account balance is 100
          When the account holder withdraws 30
          Then the account balance should be 70
