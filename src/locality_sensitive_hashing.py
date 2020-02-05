from datasketch import MinHash, MinHashLSH

def

# Create LSH index
	lsh = MinHashLSH(threshold=JACCARDIAN_THRESHOLD, num_perm=128)

	# Hash transaction
	for index_r, recipe in enumerate(recipes_mapped):
		# Init hash functions for transaction and recipe
		min_hash = MinHash(num_perm=128)
		for ingredient in recipe:
			min_hash.update(ingredient.encode('utf8'))
		lsh.insert(index_r, min_hash)

	similarity_matrix = []
	for transaction in transactions:
		# Init hash functions for transaction and recipe
		min_hash = MinHash(num_perm=128)
		# Hash recipe
		for grocery in transaction:
			min_hash.update(grocery.encode('utf8'))
		# Find similarity between transacion and all recipes
		approximated_jaccard = lsh.query(min_hash)
		similarity_matrix.append(approximated_jaccard)