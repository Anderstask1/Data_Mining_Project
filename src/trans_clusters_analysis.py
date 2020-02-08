import pickle

with open('clustering_transaction_results.pickle', 'rb') as handle:
    clustering_transaction_results = pickle.load(handle)

with open('unmatched_transactions.pickle', 'rb') as handle:
    unmatched_transactions = pickle.load(handle)




