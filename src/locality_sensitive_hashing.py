from datasketch import MinHash, MinHashLSH

def minhash_lsh(matrix_a, matrix_b, threshold, permutations):
	print("Running Min Hash and Locality Sensitive Hashing")
	similarity_matrix = {}

	# Create LSH
	lsh = MinHashLSH(threshold=threshold, num_perm=permutations)

	# Hash transaction
	for key, array in matrix_a.items():
		# Init hash functions for transaction and recipe
		min_hash = MinHash(num_perm=128)
		for value in array:
			min_hash.update(value.encode('utf8'))
		lsh.insert(key, min_hash)

	for key,array in matrix_b.items():
		# Init hash functions for transaction and recipe
		min_hash = MinHash(num_perm=128)
		# Hash recipe
		for value in array:
			min_hash.update(value.encode('utf8'))
		# Find key to row in matrix a with similarity > threshold of current row in matrix b
		results = lsh.query(min_hash)
		similarity_matrix[key]= results
	return similarity_matrix