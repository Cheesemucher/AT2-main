def getAttributes(textFile):
    rawCodeList = []
    with open(textFile, 'r') as rawCode:
        for line in rawCode:
            rawCodeList.append(line.strip())

    count = 0

    print(rawCodeList)

    if "#attributes" in rawCodeList and "#end attributes" in rawCodeList:
        for line in rawCodeList:
            if line == "#attributes": #where the attributes are marked to begin in the code
                attributesBegin = count 
            elif line == "#end attributes": #where they are marked to end in the code
                attributesEnd = count

            count += 1

    else:
        print("\n >>> required tags '#attributes' and '#end attributes' not found \n")

    attributesCodeList = rawCodeList[(attributesBegin + 1):attributesEnd]
    
    attributeList = []
    attributesToBeConstructedList = []
    for attribute in attributesCodeList:
        #attribute is now now in the format _variable = None # comment
        attribute, equalSign, nonething, *comments  = attribute.split()
        #attribute now in the format of attribute = variable (equalSign = '=', nonething = None and *comments = # whatever comment)

        attributeList.append(attribute)

        if nonething == 'None':
            attributesToBeConstructedList.append(attribute)
    print()
    print(attributeList)
    print()
    print(attributesToBeConstructedList)

    return rawCodeList, attributesEnd, attributeList, attributesToBeConstructedList

def createConstructors(attributeList) -> list:
    firstLine = "def __init__(self, "
    for attribute in attributeList:
        attributeName = attribute.replace('_', '') #gets purely the attribute name
        firstLine = firstLine + attributeName + ', '
    firstLine = firstLine + "):"

    constructorFunction = [firstLine]

    for attribute in attributeList:
        attributeName = attribute.replace('_', '') #gets purely the attribute name
        line = "    self." + attribute + " = " + attributeName
        constructorFunction.append(line)

    return constructorFunction

def createAccessors(attribute) -> str:
    attributeName = attribute.replace('_', '') #gets purely the attribute name
    firstLine = "    def get" + attributeName[0].upper() + attributeName[1:] + "(self):"
    secondLine = "        return self." + attribute
    accessor = [firstLine, secondLine]
    
    return accessor


def createMutators(attribute):
    attributeName = attribute.replace('_', '') #gets purely the attribute name
    attributeWithCapitalFirstLetter = attributeName[0].upper() + attributeName[1:] #gets the attribute but with a capital first letter
    firstLine = "    def set" + attributeWithCapitalFirstLetter + "(self, new" + attributeWithCapitalFirstLetter + "):"
    secondLine = "        self." + attribute + " = new" + attributeWithCapitalFirstLetter
    mutator = [firstLine, secondLine]
    
    return mutator

rawCodeList, attributesEnd, attributeList, attributesToBeConstructed = getAttributes("codeToConvert.txt")

accessorFunctions = map(createAccessors, attributeList)
mutatorFunctions = map(createMutators, attributeList)
constructorFunctions = createConstructors(attributesToBeConstructed)

newCodeList = rawCodeList[:(attributesEnd+1)] + [''] + ['    #constructors'] + constructorFunctions + [''] + ['    #accessors']

for accessor in accessorFunctions:
    line1, line2 = accessor
    newCodeList.append(line1)
    newCodeList.append(line2)
    newCodeList.append('')

newCodeList += ['']
newCodeList += ['#mutators']

for mutator in mutatorFunctions:
    line1, line2 = mutator
    newCodeList.append(line1)
    newCodeList.append(line2)
    newCodeList.append('')

newCodeList = newCodeList + rawCodeList[(attributesEnd+1):]


with open('codeToConvert.txt', 'w') as oldCode:
    for lineToWrite in newCodeList:
        oldCode.write(lineToWrite + '\n')





