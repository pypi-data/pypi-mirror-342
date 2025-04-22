CREATE_TRANSACTION_MUTATION = """
mutation CreateTransaction($input: CreateTransactionInput!) {
    createTransaction(input: $input) {
        altCoinTransaction {
            transactionId
            senderAddress
            recipientAddress
            amount
            feePayerAddress
            fee
            coinSymbol
            status
            type
            timestamp
        }
        feeTransaction {
            transactionId
            senderAddress
            recipientAddress
            amount
            feePayerAddress
            fee
            coinSymbol
            status
            type
            timestamp
        }
        status
        ok
        message
    }
}



"""


GET_TRANSACTIONS_QUERY = """
query GetTransactions($walletAddress: String!) {
    getTransactions(walletAddress: $walletAddress) {
        transactionId
        senderAddress
        recipientAddress
        amount
        feePayerAddress
        fee
        coinSymbol
        status
        type
        timestamp
    }
}
"""


GET_TRANSACTION_DETAILS_QUERY = """
query GetTransactionDetails($transactionId: String!) {
    getTransactionDetails(transactionId: $transactionId) {
        transactionId
        blockId
        isCoinbase
        fee
        coinId
        senderAddress
        recipientAddress
        amount
        status
    }
}
"""


CONVERT_COIN_MUTATION = """
mutation ConvertCoin(
    $senderAddress: String!,
    $recipientAddress: String!,
    $feePayerAddress: String!,
    $amount: Float!
) {
    convertCoin(
        senderAddress: $senderAddress,
        recipientAddress: $recipientAddress,
        feePayerAddress: $feePayerAddress,
        amount: $amount
    ) {
        sourceCoinTransaction {
            transactionId
            senderAddress
            recipientAddress
            amount
            feePayerAddress
            fee
            coinSymbol
            status
        }
        destinationCoinTransaction {
            transactionId
            senderAddress
            recipientAddress
            amount
            feePayerAddress
            fee
            coinSymbol
            status
        }
        status
    }
}
"""
