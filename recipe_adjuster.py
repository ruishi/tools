"""Given a recipe, adjusts ingredients given a fraction or multiplier"""

import argparse
from fractions import Fraction

def process_file_recipe(recipe):
    """Processes recipe stored in plaintext file"""
    ingredients = [line.strip('\n') for line in recipe]
    recipe.close()
    return ingredients

def process_direct_recipe(recipe):
    """Processes recipe taken from standard input"""
    ingredients = recipe.split(',')
    return ingredients

def adjust_recipe(ingredients, ratio, fileinput=False):
    ratio = create_fraction(ratio)

    if fileinput:
        ingredients = process_file_recipe(ingredients)
    else:
        ingredients = process_direct_recipe(ingredients)

    for ingredient in ingredients:
        amount= create_fraction(ingredient.split()[0])
        pl_ingredient = ' '.join(ingredient.split()[1:])
        new_amount = amount * ratio
        print("{} {}".format(new_amount, pl_ingredient))

def create_fraction(number):
    """Takes a string representation of a numberand converts it into a
    fraction"""
    if '/' in number:
        num, denom = [int(n) for n in number.split('/')]
        return Fraction(num, denom)
    elif '.' in number:
        return Fraction(float(number))
    else:
        return Fraction(int(number), 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fileinput', type=argparse.FileType('r'),
                        help='path to recipe file')
    parser.add_argument('-d', '--directinput', type=str,
                        help="directly input recipe")
    parser.add_argument('-r', '--ratio', type=str, required=True,
                        help="adjustment ratio or multiplier")

    args = parser.parse_args()
    if args.fileinput:
        adjust_recipe(args.fileinput, args.ratio, True)
    elif args.directinput:
        adjust_recipe(args.directinput, args.ratio)
    else:
        print("Must input a recipe either directly or via a file")
