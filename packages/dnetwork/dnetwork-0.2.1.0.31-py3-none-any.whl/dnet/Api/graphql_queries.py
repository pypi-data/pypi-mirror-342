# graphql_queries.py



# Query for fetching API keys
GET_API_KEYS_QUERY = """
query GetApiKeys($entityType: String!, $entityIdentifier: String!) {
    getApiKeys(entityType: $entityType, entityIdentifier: $entityIdentifier) {
        success
        message
        apiKeys {
            key
            createdAt
            entityType
            entityName
        }
    }
}
"""


# Mutation for creating an API key
CREATE_API_KEY_MUTATION = """
mutation CreateApiKey($entityType: String!, $entityIdentifier: String!, $scopes: [String!]) {
    createApiKey(entityType: $entityType, entityIdentifier: $entityIdentifier, scopes: $scopes) {
        success
        message
        apiKey {
            key
            createdAt
            entityType
            entityName
        }
    }
}
"""

# Mutation for upserting an API key
UPSERT_API_KEY_MUTATION = """
mutation UpsertApiKey($entityType: String!, $entityIdentifier: String!, $scopes: [String!]) {
    upsertApiKey(entityType: $entityType, entityIdentifier: $entityIdentifier, scopes: $scopes) {
        success
        message
        apiKey {
            key
            createdAt
            entityType
            entityName
        }
    }
}
"""

# Query for checking API key usage
CHECK_API_KEY_USAGE_QUERY = """
query CheckApiKeyUsage($apiKey: String!) {
  getApiKeyUsage(apiKey: $apiKey) {
    success
    message
    apiKeyUsage {
      key
      keyUsage
      keyRateLimit
      keyRemaining
      isWithinKeyLimit
      entityType
      entityIdentifier
      entityUsage
      entityRateLimit
      entityRemaining
      isWithinEntityLimit
    }
  }
}
"""




# Mutation for revoking an API key
REVOKE_API_KEY_MUTATION = """
mutation RevokeApiKey($apiKeyId: String!) {
    revokeApiKey(apiKeyId: $apiKeyId) {
        success
        message
    }
}
"""


# Query for fetching recent API‑call logs
GET_API_CALL_LOGS_QUERY = """
query GetApiCallLogs(
    $apiKey: String!
    $sinceHours: Int
    $limit: Int
    $offset: Int
) {
    getApiCallLogs(
        apiKey: $apiKey
        sinceHours: $sinceHours
        limit: $limit
        offset: $offset
    ) {
        success
        message
        sinceHours
        limit
        offset
        totalCount
        logs {
            createdAt
            path
            statusCode
            durationMs
            clientIp
            httpMethod
            apiKey
            operation
            requestBytes
            responseBytes
            requestId
            userAgent
            referer
            scheme
            isTls
            resolverMs
            depth
            complexity
            authSubjectId
            authMethod
            scopeSet
            bodySha256
        }
    }
}
"""

