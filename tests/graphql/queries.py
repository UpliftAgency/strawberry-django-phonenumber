USER_PROFILE_FIELDS = """
fragment UserProfileFields on User {
  id
  firstName
  lastName
  phoneNumber {
    asInternational
    asNational
    asE164
    asRfc3966
    countryCode
    nationalNumber
    extension
    rawInput
  }

}
"""


GET_USER_WITH_PHONE_NUMBER = (
    """
  query MeWithFields {
    me {
      ...UserProfileFields
    }
  }
"""
    + USER_PROFILE_FIELDS
)
