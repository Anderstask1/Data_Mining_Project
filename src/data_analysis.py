import json
import csv
from difflib import SequenceMatcher


# Find and count matches in datasets
def match_analysis(threshold):
    #find non overlapping items
    items_not_in_recipes = []

    for item in transactions_items:
        if item not in recipes_items:
            items_not_in_recipes.append(item)

    print("length: ", len(items_not_in_recipes))
    # print(items_not_in_recipes)

    for trans_item in transactions_items:
        match_flag = False
        for recipe_item in recipes_items:
            if similar(trans_item,recipe_item, threshold) :
                if match_flag == False:
                    match_count += 1 #count a match once only
                match_flag = True
                print("match found: ",trans_item," and ",recipe_item)
        if match_flag == False:
             items_without_matches.append(trans_item)

    print("transactions_items")
    print("lenght: ", len(transactions_items))
    print("recipes_items")
    print("length: ", len(recipes_items))
    print("matches found: ", match_count)
    print("items with no matches (",len(items_without_matches),"): ", items_without_matches)


