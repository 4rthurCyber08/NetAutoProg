import json


String = 'string'
Integers = 23
Float = 0.02
Boolean = True
List = ['item1', 'item2', String, Integers, 45, Boolean]



with open('data.json', 'r') as file:
    filePy = json.load(file)

dataType = type(filePy)

stringChar = r'That\'s a great idea. \nLet\'s do it.'
formatString = f'My age is {Integers}'
format2 = f'Hello, my name is {filePy['Firstname']} {filePy['Lastname']}. I was born on {filePy['Birthdate']['Month']} {filePy['Birthdate']['Day']}, {filePy['Birthdate']['Year']}. I like {filePy['Likes'][0]}.'


print(format2)