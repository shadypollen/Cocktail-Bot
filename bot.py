"""
TODO:
	*Choose which drink you want out of the top n
	*Exception when 0 mathces
"""

import sqlite3

def main():
	ingredientList = [];
	matchDict = {};
	print("""\nHello, I'm Cocky, and this is Cocky's Cocktail Shack. \nI'll help you make a cocktail.""");
	print("Please enter your ingredients and write \"done\" when finished \n")
	while True:
		ingredientString = input("> ")		
		if ingredientString.lower() == "done":
			break
		else:
			ingredientList.append(ingredientString.lower())
	makeTable()
	dbEntries = fetchTable()
	for entry in dbEntries:
		matchName, matchValue = getMatches(ingredientList, entry[0], entry[1])
		matchDict[matchName] = matchValue
	bestDrink = max(matchDict, key=matchDict.get)
	bestDrinkIngredients = getBestDrink(bestDrink)
	bestDrinkInstructions = getBestInstructions(bestDrink)
	haveList, haveNotList = getMatchingIngredients(ingredientList, bestDrinkIngredients)
	haveString = ", ".join(haveList)
	haveNotString = ", ".join(haveNotList)
	print("\n")
	print("Your most suitable cocktail is: ", bestDrink)
	print("The ingredients you have are: ", haveString, "\r")
	print("The ingredients you need to get are: ", haveNotString, "\r") 
	print("\n")
	print("Instructions: ", bestDrinkInstructions)
	conn.close()


def makeTable():
	c.execute("""CREATE TABLE IF NOT EXISTS cocktails
				(names text, ingredients text, instructions text)""")
	conn.commit()


def fetchTable():
	entriesList = []
	c.execute("SELECT * FROM cocktails")
	for entry in c.fetchall():
		entryName, entryIngredients, entryInstructions = entry
		entryIngredients = entryIngredients.split(", ")
		entriesList.append([entryName, entryIngredients, entryInstructions])
	return entriesList

def getMatches(userIngredients, cocktailName, cocktailIngredients):
	matchDict = {};
	for item in userIngredients:
		if item in cocktailIngredients:
			if not cocktailName in matchDict:
				matchDict[cocktailName] = 1
			else:
				matchDict[cocktailName] += 1
		elif not cocktailName in matchDict:
			matchDict[cocktailName] = 0
	return(cocktailName, matchDict[cocktailName])

def getBestDrink(bestDrink):
	c.execute("SELECT ingredients FROM cocktails WHERE names = (?)", [bestDrink])
	ingredientList = c.fetchone()[0].split(", ") 
	return(ingredientList)

def getMatchingIngredients(userIngredients, bestIngredients):
	haveList = []
	haveNotList = []
	for item in bestIngredients:
		if item in userIngredients:
			haveList.append(item)
		else:
			haveNotList.append(item)
	return(haveList, haveNotList)

def getBestInstructions(bestDrink):
	c.execute("SELECT instructions FROM cocktails WHERE names = (?)", [bestDrink])
	instruction = c.fetchone()[0]
	return(instruction)
	
	
conn = sqlite3.connect("cocktails2.db")
c = conn.cursor()
main()
		
