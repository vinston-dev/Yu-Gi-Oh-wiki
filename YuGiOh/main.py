from unicodedata import name
from typing import Any, List, TypeVar, Callable, Type, cast
from monster_handler import *
import os
import sys
import urllib.request
from ascii import *
import subprocess as sp

print("YuGiOh card wiki\n")
print("This program will display information about a inputed YuGiOh card\n")
print("Usage: to use the program you enter a yugioh card, for example 'kuriboh'")
print("Answer the programs following questions by either typing 'y' for yes, or 'n' for no\n")

def main():
    card_data = get_card_data(input("Enter the name of a YuGiOh card!: ").replace(' ', '%20'), Monster)
    if card_data == None:
        print("Please check your spelling!!\n")
        main()
    print_card_data(card_data)
    
    if input("Would you like to see a image of the card? (y/n): ") == "y":
        # dowloads image from url and names it after selected yugioh card
        urllib.request.urlretrieve(card_data.url, card_data.name + ".jpg")  
        # converts image to ascii art
        get_ascii(card_data.name + ".jpg")
        print("\nPress ctrl and - to zoom out in the notepad")
        # opens out.txt file in notepad
        sp.Popen("notepad out.txt")
        # deletes dowloaded image
        os.remove(card_data.name + ".jpg")
    
    if input("Would you information about another card? (y/n): ") == "y":
        main()
    sys.exit("")

main()