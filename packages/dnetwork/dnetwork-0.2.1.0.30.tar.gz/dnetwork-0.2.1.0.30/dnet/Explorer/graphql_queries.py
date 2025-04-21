GET_BLOCKCHAIN_EXPLORER = """
query GetBlockByHeight($height: Int!) {
    block(height: $height) {
        blockHeader {
            version
            blockHash
            prevBlockHash
            merkleRoot
            timestamp
            bits
            nonce
        }
        blockSize
        height
        txCount
        txs {
            txId
            version
            lockTime
            txIns {
                prevIndex
                prevTx
                sequence
                scriptSig {
                    cmds
                }
            }
            txOuts {
                amount
                scriptPubkey {
                    cmds
                }
            }
        }
    }
}
"""



GET_BLOCKCHAIN_EXPLORER_BY_SEARCH = """
   query GetBlockchainExplorerBySearch($input: SearchInput!) {
  search(input: $input) {
    __typename           
    success
    error
    data {
      __typename      
      
      ... on BlockInfo {
        blockHeader {
          version
          blockHash
          prevBlockHash
          merkleRoot
          timestamp
          bits
          nonce
        }
        blockSize
        height
        txCount
       
        txs {
          ...transactionDetails
        }
        
      }

      ... on Transaction {
        ...transactionDetails
      }

      ... on WalletTypes {
        ...walletDetails
        rawBalance
        updatedAt
        coin {
          ...coinDetails  
        }
      }

      ... on CoinTypes {
        ...coinDetails  
      }
    }
  }
}
    fragment walletDetails on WalletTypes {
        id
        publicAddress
        balance
        label
        transactionCount
        previousTransactions {
      ...previousTransactions
    }
        aggregatedRewards
        balanceBreakdown
    }
    
    
    fragment previousTransactions on PreviousTransactionType {
      transactionId
      method
      block
      fromAddress
      toAddress
      amount
      txnFee
      status
      timestamp
    }


    fragment coinDetails on CoinTypes {
        id
        name
        symbol
        maxSupply
        totalSupply
        decimals
        contractAddress
        governanceModel
        transactionFee
        visibility
        coinMetadata
        createdTime
        price
        change24h
        priceChangeUsd
        volume1hr
        volume24h
        marketCap
        prices7d
        circulatingSupply
        typicalHoldTime
        volumeMarketCapRatio
        trendingActivity
        popularity
        allTimeHigh
        rank
        orderBook
        candlesticks
        historicalData
        mempoolTxids
        mempoolTxCount
        walletDistribution {
            publicAddress
            rawBalance
            balance
            percentage
            label
        }
        walletCount
        transactions {
      ...previousTransactions
    }
          
    }
    
    fragment transactionDetails on Transaction {
        txId
        version
        lockTime
        coinId
        fee
        block {
          height
          blockHash
          timestamp
        }
        userTransaction {
          transactionId
          amount
          status
          transactionType
          timestamp
          linkedFeeTxId
          linkedAltTxId
          senderWallet {
            ...walletDetails
          }
          recipientWallet {
            ...walletDetails
          }
        }
        txIns {
          prevIndex
          prevTx
          sequence
          scriptSig {
            cmds
          }
        }
        txOuts {
          amount
          scriptPubkey {
            cmds
            minerAddress
          }
        }
        coin {
          ...coinDetails
        }
      }
      
      


"""



GET_NEW_BLOCK_SUBSCRIPTION = """
subscription GetNewBlock {
  new_block {
    height
    block_header {
      version
      block_hash
      prev_block_hash
      merkle_root
      timestamp
      bits
      nonce
    }
    block_size
    tx_count
    timestamp
    txs {
      tx_id
      lock_time
      fee
      coin_id
      tx_ins {
        prev_index
        prev_tx
        script_sig {
          cmds
        }
        sequence
      }
      tx_outs {
        amount
        script_pubkey {
          cmds
          miner_address
        }
      }
      block {
        block_hash
        timestamp
      }
      user_transaction {
        transaction_id
        amount
        status
        transaction_type
        timestamp
        sender_wallet {
          id
          public_address
          balance
          label
          transaction_count
          created_at
           previous_transactions {
            ...PreviousTransactionFields
          }
          aggregated_rewards
          balance_breakdown
          raw_balance
          updated_at
        }
        recipient_wallet {
          id
          public_address
          balance
          label
          transaction_count
          created_at
           previous_transactions {
            ...PreviousTransactionFields
          }
          aggregated_rewards
          balance_breakdown
          raw_balance
          updated_at
        }
        linked_fee_tx_id
        linked_alt_tx_id
      }
      coin {
        id
        name
        symbol
        creator_id
        total_supply
        contract_address
        max_supply
        decimals
        is_active
        is_utxo_based
        consensus_type
        governance_model
        transaction_fee
        treasury_wallet
        treasury_allocation_percentage
        burnable
        mintable
        visibility
        coin_metadata
        created_time
        status
        premine_allocation
        price
        price_change_usd
        change_24h
        volume_1hr
        volume_24h
        market_cap
        prices_7d
        circulating_supply
        typical_hold_time
        volume_market_cap_ratio
        trending_activity
        popularity
        all_time_high
        rank
        order_book
        candlesticks
        historical_data
        mempool_txids
        mempool_tx_count
        wallet_distribution{
          public_address
            raw_balance
            balance
            percentage
            label
        }
        wallet_count
        transactions {
          ...PreviousTransactionFields
        }
      }
    }
  }
}

  fragment PreviousTransactionFields on previousTransactions {
  transactionId
  method
  block
  fromAddress
  toAddress
  amount
  txnFee
  status
  timestamp
}


"""
