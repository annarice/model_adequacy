import sys
sys.path.insert(0,"/groups/itay_mayrose/annarice/model_adequacy/code")
#from code.defs import *
from defs import *

def match_counts_to_tree(tree_file,counts,new_counts,new_tree):
    t = Tree(tree_file, format=1)
    tree_flag = 0
    to_be_pruned = []
    tips = []
    for leaf in t:
        tips.append(leaf.name)
    tmp = {}
    with open(counts,"r") as counts_file:
        for line in counts_file:
            line = line.strip()
            if line.startswith('>'):
                name = line[1:]
            else:
                if line != "x":
                    tmp[name] = int(line)
                else:
                    to_be_pruned.append(name)
                    tree_flag = 1
    with open(new_counts,"w+") as handle:
        for key in tmp:
            if key in tips: # count on the tree
                handle.write(">" + key + "\n")
                handle.write(str(tmp.get(key)) + "\n")
    if tree_flag == 1: # the tree was pruned - re-write it
        t.prune(list(set(tips) - set(to_be_pruned)))
        t.write(format=1, outfile=new_tree)
    else:
        t.write(format=1,outfile=new_tree)


def handle_tree(tree_file,tip_to_prune):
    t = Tree(tree_file, format=1)
    tips = [leaf.name for leaf in t]
    t.prune(list(set(tips) - set([tip_to_prune])))
    t.write(format=1, outfile=tree_file)


def get_counts(filename):
    '''
        reads the .counts_edit file and extracts the counts
    :param filename: supplied by the user
    :return: list of counts
    '''
    with open(filename, "r") as tmp_counts_file:
        counts = []
        for line in tmp_counts_file:
            line = line.strip()
            if line.startswith('>'):
                name = line[1:]
                continue
            else:
                #if line=="x":
                    #handle_tree(tree_file, name) # prune the tree
                    #continue
                counts.append(int(line))
    if len(set(counts))== 0: # no counts variability, do not apply MA
        return ("exit")
    return (counts)