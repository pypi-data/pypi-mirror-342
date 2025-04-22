

# Mutation for creating a user
CREATE_USER_MUTATION = """
mutation CreateUser($email: String!, $password: String!, $organization: String) {
    createUser(email: $email, password: $password, organization: $organization) {
        success
        message
        user {
            id
            email
            organization
            createdAt
        }
    }
}
"""

# Mutation for creating a company
CREATE_COMPANY_MUTATION = """
mutation CreateCompany($name: String!) {
    createCompany(name: $name) {
        success
        message
        company {
            id
            name
            createdAt
        }
    }
}
"""