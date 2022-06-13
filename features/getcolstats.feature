      Feature:GetColstats validations

        Scenario Outline: Verify Get_col_stats passes positive test cases
          Given the user has datasetid and versionid through AddByPathAPI
          When the user calls GetColStatsAPI using request payload "<JSONFile>"
          Then user should get status code 200
          And response body should not be null
          And message in result should be "success"
          And column names in API response data should be equal to column names given in input file


          Examples:
	        |JSONFile|
	        |get_col_stats.json|
            |get_col_stats_homes.json|

