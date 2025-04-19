def lab1():
    print(''' Lab - 1: Pattern Matching with RegEx
import re
import pandas as pd
import seaborn as sns
data = pd.read_csv("Titanic-Dataset.csv")
def match_pattern(data, column, pattern):
    matched = []
    for value in data[column]:
        if re.match(pattern.lower(), str(value).lower()):
            matched.append(value)
    return matched
def get_input():
    print("Available columns to search: 'Name', 'Age', 'Sex', 'Survived', 'Pclass'")
    column = input("Enter the column name to search: ")
    if column not in ['Name', 'Age', 'Sex', 'Survived', 'Pclass']:
        print("Invalid column name. Please enter a valid column name")
        return
    pattern = input(f"Enter the pattern to match in the {column} column: ")
    matched = match_pattern(data, column, pattern)
    if matched:
        print(f"\nFound {len(matched)} matches for the pattern {pattern} in column {column}:")
        for result in matched:
            print(result)
    else:
        print(f"\nNo matches found for the pattrn {pattern} in column {column}")
get_input()
''')