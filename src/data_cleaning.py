def clean_dictionary(dictionary, array):
    cleaned_dict = {}
    for key, value in dictionary.items():
        intersection = set(value) & set(array)
        cleaned_dict[key] = list(intersection)
    return cleaned_dict