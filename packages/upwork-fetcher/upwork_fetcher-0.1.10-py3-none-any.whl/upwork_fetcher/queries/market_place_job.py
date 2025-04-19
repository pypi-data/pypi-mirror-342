MarketplaceJobPostingsSearchQuery = """query marketplaceJobPostingsSearch($marketPlaceJobFilter: MarketplaceJobPostingsSearchFilter, $searchType: MarketplaceJobPostingSearchType, $sortAttributes: [MarketplaceJobPostingSearchSortAttribute]) {
  marketplaceJobPostingsSearch(
    marketPlaceJobFilter: $marketPlaceJobFilter
    searchType: $searchType
    sortAttributes: $sortAttributes
  ) {
    totalCount
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        title
        description
        category
        totalApplicants
        preferredFreelancerLocation
        preferredFreelancerLocationMandatory
        premium
        experienceLevel
        amount {
          rawValue
          currency
          displayValue
        }
        skills {
          name
          prettyName
          highlighted
        }
        hourlyBudgetType
        hourlyBudgetMin {
          rawValue
          currency
          displayValue
        }
        hourlyBudgetMax {
          rawValue
          currency
          displayValue
        }
        duration
        clientNotSureFields
        clientPrivateFields
        freelancerClientRelation{
          companyName
        }
        localJobUserDistance
        weeklyBudget {
          rawValue
          currency
          displayValue
        }
        engagementDuration {
          id
          label
          weeks
        }
        client{
          edcUserId
          totalHires
          totalPostedJobs
          totalSpent{
            rawValue
            currency
            displayValue
          }
          location{
            city
            country
            timezone
            state
            offsetToUTC
          }
          totalReviews
          totalFeedback
          companyRid
          companyName
          edcUserId
          lastContractPlatform
          lastContractRid
          lastContractTitle
          hasFinancialPrivacy
        }
        occupations{
          category{
            id
            prefLabel
          }
        }
        freelancerClientRelation{
          companyName
        }
        
        createdDateTime
        publishedDateTime
      }
    }
  }
}
        """
