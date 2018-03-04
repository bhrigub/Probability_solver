"""
Created on Mon Oct 11 18:44:17 2017

@author: bhrigu_bhargava
References: Artificial Intelligence- A Modern Approach (Third Edition) by Stuart Russell and Peter Norvig
            https://www.slideshare.net/PyData/understanding-your-data-with-bayesian-networks-in-python-by-bartek-wilczynski
            http://tdc-www.harvard.edu/Python.pdf
            https://classroom.udacity.com/courses/cs271/lessons/48743138/concepts/484039240923
            https://www.ics.uci.edu/~rickl/courses/cs-171/cs171-lecture-slides/cs-171-17-BayesianNetworks.pdf
            https://chrisalbon.com/python/cartesian_product.html
            
Logic: The user input is decoded in form of an equation using generateEquation function. The generateEquation function 
results into an output containing:
    1) stableLogic i.e. the logic indipendent of other nodes, 
    2) repeatingLogic i.e. the undefined variables that would be needed to solve probability and perform summation 
    3) newGiven i.e. the list used to differentiate the actually required given nodes for calculation from the other nodes given by user
Next, the we check for combination of indipendent events and ones requiring summation and execute calculation accordingly and
trigger functions like enumerationQuery for solving cases that require cartesian product and other function solveQuery
which require simple product rule.   

"""
#==============================================================================
#     A  -          -   B
#          -     - 
#             C
#       -         -
#     D               E
#==============================================================================
   
def calculate_probability (A,B,C,D,E):
    """
    Function to compute and returns the probability of any conjunction of events given any other conjunction of events.
    """
    inputArray = [A, B, C, D, E]
    if len(inputArray) > 5:
        return print("Invalid Value Entry")
    givenTotal=[]
    #Debug:
    #print (inputArray)
    #Query generation for preserving original inputs and for future editing
    givenLogic, queryLogic, unspecified = formEquation(inputArray)
    givenLogic2, queryLogic2, unspecified2 = formEquation(inputArray)
    givenTotal= givenLogic + queryLogic
    if not queryLogic:
            return print ("Missing Query for Probability Calculation")
    #Debug:
    #print (queryLogic, givenLogic, unspecified)
    #print (givenTotal)
    stableLogic, repeatingLogic, newGiven = generateEquation (queryLogic, givenTotal, unspecified)
    #print (stableLogic, repeatingLogic)

    if queryLogic2:
        if repeatingLogic and stableLogic:
            probCal = solveQuery (stableLogic)
            #print(probCal)
            probabilityNum = enumerationQuery (repeatingLogic, probCal)
        elif repeatingLogic and not stableLogic:
            probabilityNum = enumerationQuery (repeatingLogic, 1)
        elif stableLogic and not repeatingLogic:
            probabilityNum = solveQuery (stableLogic)
            #print('1:', stableLogic)
        else:
            return print("Invalid probability1")
        probability = probabilityNum
    #print('ng:',newGiven)
    #print(givenLogic2)
    finalGiven = []
    finalGivenSet = {}
    
    finalGivenSet = set(newGiven).intersection(givenLogic2)
    finalGiven = list(finalGivenSet)
    
    #print('fg:', finalGiven)
    stableLogic1, repeatingLogic1, newGiven1 = generateEquation (finalGiven,[],[])    
    if finalGiven:
        if repeatingLogic1 and stableLogic1:
            probCal1 = solveQuery (stableLogic1)
            probabilityDen = enumerationQuery (repeatingLogic1,probCal1)
        elif repeatingLogic1 and not stableLogic1:
            probabilityDen = enumerationQuery (repeatingLogic1, 1)
        elif stableLogic1 and not repeatingLogic1:
            probabilityDen = solveQuery (stableLogic1)
        else:
            probabilityDen = 1
        probability = probabilityNum / probabilityDen     
        
    #print (stableLogic1, repeatingLogic1)
      
    #probability = round(probability, 2)
    #print (probability)
    
    return probability
        
   
def formEquation (inputArray):
    """
    Function to decode the input from the user into given, query and unspecified.
    """
    i = 0
    #Lists to store the inputs in form of variable probability
    givenLogic = []
    queryLogic = []
    unspecified = []
    #Available arguments
    argumentsOption = ['A','B','C','D','E']
    for i in range (0, len(inputArray)):        
        if (inputArray[i] == 0) or (inputArray[i] == 1):
            if (inputArray[i] == 1):
                givenLogic.append('P' + argumentsOption[i]) 
            else:
                givenLogic.append('Pn' + argumentsOption[i]) #n added to depict falte or not case
        elif (inputArray[i] == 2) or (inputArray[i] == 3):
            if (inputArray[i] == 3):
                queryLogic.append('P' + argumentsOption[i])
            else:
                queryLogic.append('Pn' + argumentsOption[i])
        elif (inputArray[i] == 4):
            unspecified.append(argumentsOption[i])
        else:
            return print ("Invalid Entry of Logic Values")        
        
    #Debug:
    #print (givenLogic, queryLogic, unspecified)
    return givenLogic, queryLogic, unspecified


def generateEquation (queryNodes, givenLogic, unspecified):
    """
    Function to generate equation in form of stable nodes and enumerated nodes with submission.
    """
    #print (queryNodes, givenLogic, unspecified)
    #requirements for Node C, D, E for calculations
    requirementC = ['PnA', 'PnB', 'PA', 'PB']
    requirementD = ['PnC', 'PC']
    requirementE = ['PnC', 'PC']
    #New probability equation storage
    probNew= [] 
    #Nodes that have been visited already
    processedNodes = []
    #Nodes with submission since they are unspecified but required for enumeration expansion
    repeatingNodes = []
    
    newGiven = []
    i= 0
    while (i < 20):
        """
        Loop to process the given, query and unspecified nodes and result in equation and check individual requirement
        for every node and beysian networks flow.
        """
#   requirementE = ['PnC', 'PC']
#checks for requirement for a node is present in givenlogic and if it has been visited already or not
        if 'PnE' in queryNodes and 'PnE' not in processedNodes:
            if requirementE[0] in givenLogic:
                #probNew is to store newly generated probability for indipendent elements
                probNew.append('PnEgnC')
                #store processed nodes values
                processedNodes.append('PnE')
                #new given to compare the values of actually required elements vs the inputs given by user and helps in 
                #finding alpha or the denominator                
                newGiven.append(requirementE[0])
                
            elif requirementE[1] in givenLogic:
                probNew.append('PnEgC')
                processedNodes.append('PnE')
                newGiven.append(requirementE[1])
                
            else:
                repeatingNodes.append('PnE')
                repeatingNodes.append('PCC')
                queryNodes.append('PC')
                processedNodes.append('PnE')
        elif 'PE' in queryNodes and 'PE' not in processedNodes:
            if requirementE[0] in givenLogic:
                probNew.append('PEgnC') 
                processedNodes.append('PE')
                newGiven.append(requirementE[0])
            elif requirementE[1] in givenLogic:
                probNew.append('PEgC')
                processedNodes.append('PE')
                newGiven.append(requirementE[1])
            else:
                repeatingNodes.append('PE')
                repeatingNodes.append('PCC')
                queryNodes.append('PC')
                processedNodes.append('PE')
#   requirementD = ['PnC', 'PC']
        elif 'PD' in queryNodes and 'PD' not in processedNodes:
            if requirementD[0] in givenLogic:
                probNew.append('PDgnC')
                processedNodes.append('PD')
                newGiven.append(requirementD[0])
            elif requirementD[1] in givenLogic:
                probNew.append('PDgC')
                processedNodes.append('PD')
                newGiven.append(requirementD[1])
            else:
                repeatingNodes.append('PD')
                repeatingNodes.append('PCC')
                queryNodes.append('PC')
                processedNodes.append('PD')
        elif 'PnD' in queryNodes and 'PnD' not in processedNodes:
            if requirementD[0] in givenLogic:
                probNew.append('PnDgnC')
                processedNodes.append('PnD')
                newGiven.append(requirementD[0])
            elif requirementD[1] in givenLogic:
                probNew.append('PnDgC')
                processedNodes.append('PnD')
                newGiven.append(requirementD[1])
            else:
                repeatingNodes.append('PnD')
                repeatingNodes.append('PCC')
                queryNodes.append('PC')
                processedNodes.append('PnD')
#   requirementC = ['PnA', 'PnB', 'PA', 'PB']
        elif 'PC' in queryNodes and 'PC' not in processedNodes:
            if 'A' and 'B' in unspecified:
                repeatingNodes.append('PA')
                repeatingNodes.append('PB')
                processedNodes.append('PC')
                if 'PC' not in repeatingNodes:
                    repeatingNodes.append('PC')
                
            elif requirementC[0] in givenLogic:
                if requirementC[1] in givenLogic:
                    probNew.append('PCgnAnB')
                    processedNodes.append('PC')
                    newGiven.append(requirementC[0])
                    newGiven.append(requirementC[1])
                elif requirementC[3] in givenLogic:
                    probNew.append('PCgnAB')
                    processedNodes.append('PC')
                    newGiven.append(requirementC[0])
                    newGiven.append(requirementC[3])                    
                else:
                    repeatingNodes.append('PB')
                    queryNodes.append('PnA')
                    processedNodes.append('PC')
                    newGiven.append(requirementC[0])
            elif requirementC[2] in givenLogic:
                if requirementC[1] in givenLogic:
                    probNew.append('PCgAnB')
                    processedNodes.append('PC')
                    newGiven.append(requirementC[2])
                    newGiven.append(requirementC[1])
                elif requirementC[3] in givenLogic:
                    probNew.append('PCgAB')
                    processedNodes.append('PC')
                    newGiven.append(requirementC[2])
                    newGiven.append(requirementC[3])
                else:
                    repeatingNodes.append('PB')
                    queryNodes.append('PA')
                    processedNodes.append('PC')
                    newGiven.append(requirementC[2])
#   requirementC = ['PnA', 'PnB', 'PA', 'PB']
            elif 'PA' not in givenLogic and 'PnA' not in givenLogic:
                if 'PnB' in givenLogic:
                    repeatingNodes.append('PA')
                    queryNodes.append('PnB')
                    processedNodes.append('PC')
                    newGiven.append('PnB')
                    if 'PC' not in repeatingNodes:
                        repeatingNodes.append('PC')
                if 'PB' in givenLogic:
                    repeatingNodes.append('PA')
                    queryNodes.append('PB')
                    processedNodes.append('PC')
                    newGiven.append('PB')
                    if 'PC' not in repeatingNodes:
                        repeatingNodes.append('PC')
           
        elif 'PnC' in queryNodes and 'PnC' not in processedNodes:
            if 'A' and 'B' in unspecified:
                repeatingNodes.append('PA')
                repeatingNodes.append('PB')
                processedNodes.append('PnC')
                if 'PnC' not in repeatingNodes:
                    repeatingNodes.append('PnC')
                
            elif requirementC[0] in givenLogic:
                if requirementC[1] in givenLogic:
                    probNew.append('PnCgnAnB')
                    processedNodes.append('PnC')
                    newGiven.append(requirementC[0])
                    newGiven.append(requirementC[1])
                elif requirementC[3] in givenLogic:
                    probNew.append('PnCgnAB')
                    processedNodes.append('PnC')
                    newGiven.append(requirementC[0])
                    newGiven.append(requirementC[3])                    
                else:
                    repeatingNodes.append('PB')
                    queryNodes.append('PnA')
                    processedNodes.append('PnC')
                    newGiven.append(requirementC[0])
            elif requirementC[2] in givenLogic:
                if requirementC[1] in givenLogic:
                    probNew.append('PnCgAnB')
                    processedNodes.append('PnC')
                    newGiven.append(requirementC[2])
                    newGiven.append(requirementC[1])
                elif requirementC[3] in givenLogic:
                    probNew.append('PnCgAB')
                    processedNodes.append('PnC')
                    newGiven.append(requirementC[2])
                    newGiven.append(requirementC[3])
                else:
                    repeatingNodes.append('PB')
                    queryNodes.append('PA')
                    processedNodes.append('PnC')
                    newGiven.append(requirementC[2])
#   requirementC = ['PnA', 'PnB', 'PA', 'PB']
            elif 'PA' not in givenLogic and 'PnA' not in givenLogic:
                if 'PnB' in givenLogic:
                    repeatingNodes.append('PA')
                    queryNodes.append('PnB')
                    processedNodes.append('PnC')
                    newGiven.append('PnB')
                    if 'PnC' not in repeatingNodes:
                        repeatingNodes.append('PnC')
                if 'PB' in givenLogic:
                    repeatingNodes.append('PA')
                    queryNodes.append('PB')
                    processedNodes.append('PnC')
                    newGiven.append('PB')
                    if 'PnC' not in repeatingNodes:
                        repeatingNodes.append('PnC')
#  requirementC = ['PnA', 'PnB', 'PA', 'PB'] 
        elif 'PB' in queryNodes and 'PB' not in processedNodes:
            #print('hi')
            if 'PC' in givenLogic and 'PC' not in queryNodes:
                queryNodes.append('PC')
                #processedNodes.append('PB')
                if 'PC' not in newGiven:
                    newGiven.append('PC')
            elif 'PnC' in givenLogic and 'PnC' not in queryNodes:
                queryNodes.append('PnC')
                #processedNodes.append('PB')
                if 'PnC' not in newGiven:
                    newGiven.append('PnC')
            else:
                probNew.append('PB')
                processedNodes.append('PB')
        elif 'PnB' in queryNodes and 'PnB' not in processedNodes:
            if 'PC' in givenLogic and 'PC' not in queryNodes:
                queryNodes.append('PC')
                #processedNodes.append('PnB')
                if 'PC' not in newGiven:
                    newGiven.append('PC')
            elif 'PnC' in givenLogic and 'PnC' not in queryNodes:
                queryNodes.append('PnC')
                #processedNodes.append('PnB')
                if 'PnC' not in newGiven:
                    newGiven.append('PnC')
            else:
                probNew.append('PnB')
                processedNodes.append('PnB')
        elif 'PA' in queryNodes and 'PA' not in processedNodes:
            if 'PC' in givenLogic and 'PC' not in queryNodes:
                queryNodes.append('PC')
                #processedNodes.append('PA')
                if 'PC' not in newGiven:
                    newGiven.append('PC')
            elif 'PnC' in givenLogic and 'PnC' not in queryNodes:
                queryNodes.append('PnC')
                #processedNodes.append('PA')
                if 'PnC' not in newGiven:
                    newGiven.append('PnC')
            else:
                probNew.append('PA')
                processedNodes.append('PA')
        elif 'PnA' in queryNodes and 'PnA' not in processedNodes:
            if 'PC' in givenLogic and 'PC' not in queryNodes:
                queryNodes.append('PC')
                #processedNodes.append('PnA')
                if 'PC' not in newGiven:
                    newGiven.append('PC')
            elif 'PnC' in givenLogic and 'PnC' not in queryNodes:
                queryNodes.append('PnC')
                #processedNodes.append('PnA')
                if 'PnC' not in newGiven:
                    newGiven.append('PnC')
            else:
                probNew.append('PnA')
                processedNodes.append('PnA')
        else:
            break
        i = i+1
                
        #Debug:
        #print (queryNodes, probNew, repeatingNodes, processedNodes, newGiven) 
        
        #Debug:
        #print (queryNodes, givenLogic, probNew, repeatingNodes, processedNodes) 
    return probNew, repeatingNodes, newGiven

def solveQuery (stableLogic):
    """
    Function to solve the query values to calculate the final probability with input picked from the equation
    """
    #dictionary to store probability values
    valueDict = {'PA': 0.30,'PnA': 0.70, 'PB': 0.40, 'PnB': 0.60, 'PCgnAnB': 0.25, 'PnCgnAnB': 0.75, 'PCgnAB': 0.50, 'PnCgnAB': 0.50, 'PCgAnB': 0.60, 'PnCgAnB': 0.40, 'PCgAB': 0.80, 'PnCgAB': 0.20, 'PDgnC': 0.75, 'PnDgnC': 0.25, 'PDgC': 0.20, 'PnDgC': 0.80, 'PEgC': 0.80, 'PnEgC': 0.20, 'PEgnC': 0.30, 'PnEgnC': 0.70}
    #list of possible values in solution equation
    requiredValues =['PnEgnC', 'PnEgC', 'PEgnC', 'PEgC', 'PDgnC', 'PDgC', 'PnDgnC', 'PnDgC', 'PCgnAnB', 'PCgnAB', 'PCgAnB', 'PCgAB', 'PnCgnAnB', 'PnCgnAB', 'PnCgAnB', 'PnCgAB', 'PB', 'PA', 'PnA', 'PnB']
    probabilityTable = []
    j,g = 0,0
    probCal = 1
    #loop to build probability list 
    for j in range (0, len(requiredValues)):
        if (requiredValues[j] in stableLogic):
            probabilityTable.append(valueDict[requiredValues[j]])
            #print(probabilityTable)
            probCal = probCal * probabilityTable[g]
            g = g + 1
            #print(g)
    
    #Debug:
    #print (probabilityTable)
    #print (probCal)
    return probCal

def enumerationQuery (repeatingLogic, probCal):
    """
    Function to solve the query for unspecified elements that are required to solve equation. These values are
    summation of every state and require catesian product
    """
    queryProbability = 0
    #Requirements for forming solutions
    solnPCC = ['PCgnAnB','PCgnAB', 'PCgAnB', 'PCgAB', 'PnCgnAnB', 'PnCgnAB', 'PnCgAnB', 'PnCgAB']
    solnPnD = ['PnDgnC', 'PnDgC']
    solnPD = ['PDgnC', 'PDgC']
    solnPnE = ['PnEgnC', 'PnEgC']
    solnPE = ['PEgC','PEgnC']
    solnPC = ['PCgnAnB','PCgnAB', 'PCgAnB', 'PCgAB']
    solnPnC = ['PnCgnAnB', 'PnCgnAB', 'PnCgAnB', 'PnCgAB']
    solnA = ['PA', 'PnA']
    solnB = ['PB', 'PnB']
    
    #List to store and generate different combinations for the unspecified values
    probLists = []
    if 'PA'in repeatingLogic:
        probLists.append(solnA)
    if 'PB' in repeatingLogic:
        probLists.append(solnB)
    if 'PCC' in repeatingLogic:
        probLists.append(solnPCC)
    if 'PC' in repeatingLogic:
        probLists.append(solnPC)
    if 'PnC' in repeatingLogic:
        probLists.append(solnPnC)
    if 'PD' in repeatingLogic:
        probLists.append(solnPD)
    if 'PnD' in repeatingLogic:
        probLists.append(solnPnD)
    if 'PE' in repeatingLogic:
        probLists.append(solnPE)
    if 'PnE' in repeatingLogic:
        probLists.append(solnPnE)
    #print (probLists)
    p,q,r,s = 0,0,0,0
    #Find length of array and understand number of combinations required for different variables
    l1 = len(probLists)
    # Apply cartesian product to achieve different combination of variables
    if l1 == 0:
        return ("No Solution")
    elif l1 == 1:
       for p in range (0,1):
           queryProbability = queryProbability + (probCal * solveQuery(probLists[p]))
           #print (queryProbability)
    elif l1 == 2:
        finalProbList = [[a,b] for a in probLists[0] for b in probLists[1]]
        for q in range (0,len(finalProbList)):
            queryProbability = queryProbability + (probCal * solveQuery(finalProbList[q]))
    elif l1 == 3:
        finalProbList = [[a,b,c] for a in probLists[0] for b in probLists[1] for c in probLists[2]]
        for r in range (0,len(finalProbList)):
            queryProbability = queryProbability + (probCal * solveQuery(finalProbList[r]))
    elif l1 == 4:
        finalProbList = [[a,b,c,d] for a in probLists[0] for b in probLists[1] for c in probLists[2] for d in probLists[3]]
        for s in range (0,len(finalProbList)):
            queryProbability = queryProbability + (probCal * solveQuery(finalProbList[s]))
        
    #print (queryProbability)
    return queryProbability

#for a in range (0,4):
#    for b in range (0,4):
#        for c in range (0,4) :
#             for d in range (0,4) :
#                for e in range (0,4): 
#                    calculate_probability(a,b,c,d,e)        

           
        
        