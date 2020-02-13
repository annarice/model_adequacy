from ete3 import Tree
import re

def create_bntpv(expFile, mlAncTree, baseNum):

    with open(expFile,'r') as expFile_f:
        perNode_EXPECTATIONS_lines=[]
        look_for_end=0
        for line in expFile_f:
            if "#ALL EVENTS EXPECTATIONS PER NODE" in line and look_for_end == 0:
                look_for_end = 1    #stop when you find the next #+++++++++++++++++++++++++++++ line
            if look_for_end == 1 and "#++++++++++++++++++++++++" in line:
                break
            if look_for_end == 1:
                if "#ALL EVENTS EXPECTATIONS PER NODE" not in line and "BASE-NUMBER" not in line:
                    perNode_EXPECTATIONS_lines.append(line.strip())
    expFile_f.close()

    btnodes=dict()
    for item in perNode_EXPECTATIONS_lines:
        item_split = item.split()
        node = item_split[0]
        weight = float(item_split[5])
        if weight > 0.1:
            if weight > 1: weight = 1
            btnodes[node] = weight
    if not btnodes:
        return "%d=1.00"%baseNum
    # if for some reason there are no base transition events
    #if not btnodes.values():
    #    baseNum=1
    #    return baseNum

    ### for each node, find the base transition
    transitions = dict()  # will contain all transitions found in data (value is # of times transition was found)
    tree_test=Tree(mlAncTree, format=1)
    for node in tree_test.traverse("postorder"):
        nodeid = re.search("\[?([^\-]+)-([^\]]+)\]?", node.name)
        nodeName = nodeid.group(1)
        if nodeid.group(2) is not 'x' and nodeid.group(2) is not 'X':
            nodeCount = int(nodeid.group(2))
        else:
            nodeCount = nodeid.group(2)
        # if node has base num transition
        if nodeName in btnodes.keys():
            ancestor = node.up
            ancestorid = re.search("\[?([^\-]+)-([^\]]+)\]?", ancestor.name)
            ancestorName = ancestorid.group(1)
            if ancestorid.group(2) is not 'x' and ancestorid.group(2) is not 'X':
                ancestorCount = int(ancestorid.group(2))
            else:
                ancestorCount = ancestorid.group(2)

            # if both node and parent have counts
            if nodeCount is not 'x' and nodeCount is not 'X' and ancestorCount is not 'x' and ancestorCount is not 'X':
                #Need to add the posibility of probabilities vector !!!
                transition = nodeCount - ancestorCount  # may include gains\losses
                realTrans = round(transition /baseNum) * baseNum
                # add transition to hash
                if realTrans > 0:
                    if realTrans in transitions.keys():
                        transitions[realTrans] += btnodes[nodeName]
                    else:
                        transitions[realTrans] = btnodes[nodeName]
            else:
                btnodes[nodeName] = "NA"

    # in case no transitions were found, give transition by base number prob of 1
    if not transitions:
        transitions[baseNum] = 1.00

    ### calculate probabilities
    allTransitions = list(transitions.values())
    totalTrans = sum(allTransitions)
    # remove rare transitions (less then 0.05)
    for key in transitions.keys():
        if (transitions[key]/totalTrans < 0.05):
            del transitions[key]

    # create final probs hash
    probsHash=dict()
    for key in transitions.keys():

        res=float(transitions[key]/totalTrans)
        finalProb = "%.2f" %res # limited to 2 decimal digits
        probsHash[key] = float(finalProb)

    # make sure probs sum to 1
    allProbs = list(probsHash.values())

    probSum = sum(allProbs)
    diff = 1-probSum
    if diff != 0:
        # complete or substract to 1 on a random prob
        transitions = list(probsHash.keys())
        randTrans = transitions[0]
        probsHash[randTrans] += diff

    # create probs vector
    vector = ""
    for key in probsHash.keys():
        vector+= str(key) + '=' + str(probsHash[key]) + '_'
    vector = vector[:-1]

    return vector

if __name__ == '__main__':
	x = create_bntpv("/groups/itay_mayrose/annarice/model_adequacy/genera/Potentilla/BASE_NUM_DUPL/expectations.txt", "/groups/itay_mayrose/annarice/model_adequacy/genera/Potentilla/BASE_NUM_DUPL/mlAncestors.tree", 7)
	print(x)
