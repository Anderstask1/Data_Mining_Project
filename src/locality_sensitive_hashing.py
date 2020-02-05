from datasketch import MinHash, MinHashLSH

def minhash_lsh(matrix_a, matrix_b, threshold, permutations):
	similarity_matrix = []

	# Create LSH index
	lsh = MinHashLSH(threshold=threshold, num_perm=permutations)

	# Hash transaction
	for index, array in enumerate(matrix_a):
		# Init hash functions for transaction and recipe
		min_hash = MinHash(num_perm=128)
		for value in array:
			min_hash.update(value.encode('utf8'))
		lsh.insert(index, min_hash)

	for array in matrix_b:
		# Init hash functions for transaction and recipe
		min_hash = MinHash(num_perm=128)
		# Hash recipe
		for value in array:
			min_hash.update(value.encode('utf8'))
		# Find similarity between transacion and all recipes
		approximated_jaccard = lsh.query(min_hash)
		similarity_matrix.append(approximated_jaccard)
	return similarity_matrix