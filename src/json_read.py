import json


filename = "../datasets/recipe-ingredients-dataset/train.json"

with open(filename, 'r') as f:
    recipes = json.load(f)

print(recipes)

print(recipes[00000]["ingredients "])



