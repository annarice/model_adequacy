import sys
sys.path.append("../")
from defs import *
from utils import *

def calculate_statistics(counts,filename, tree_file, simulated_counts_file = False, tree_file2 = None):
    '''

    :param counts: list of counts
    :param filename: output file to where the stats will be printed
    :param tree_file: for parsimony (fitch) and time-parsimony calculations
    :param simulated_counts_file: if supplied - stats are calculated on simulations
    :param tree_file2: if supplied - stats are calculated on simulations, a different tree file that needs to be corrected (CE bug - semicolon)
    :return: list of statistics representing the counts
    '''

    # variance
    v = round(np.var(counts),2)

    # range = max - min
    r = max(counts) - min(counts)

    # enthropy, calculates the probabilities
    d = {}
    for i in counts:
        d[i] = counts.count(i)
    prob_lst = [x / len(counts) for x in list(d.values())]
    e = sc.entropy(prob_lst)

    # unique counts
    counts_set = set(counts)
    u = len(counts_set)

    # parsimony
    p = fitch(tree_file,simulated_counts_file)

    if tree_file2 is not None:
        fix_tree_file2(tree_file2) # add semicolon
        tmp_tree_file = tree_file2
    else:
        tmp_tree_file = tree_file

    try:
        a = acctran(tmp_tree_file)
    except:
        a = 0

    lst_of_stats = [v, e, p, a, r, u]
    round_stats = [round(x,2) for x in lst_of_stats]

    with open(filename, "w+") as stats:
        stats.write(','.join([str(x) for x in round_stats]))

    return (round_stats)

def fitch (tree_file, c = False):
    t = Tree(tree_file, format = 1)
    score = 0

    '''
    if c: # if there's a counts file, the analysis is of a simulated dataset
        d = {}
        with open(c, "r") as counts:
            for line in counts:
                line = line.strip()
                if line.startswith(">"):
                    key = line[1:]
                else:
                    val = line
                    d[key] = val
    '''
    if c:
        d = create_counts_hash(c)


    for node in t.traverse("postorder"):
        if not node.is_leaf():  # internal node
            lst = []  # list version
            intersect, union = None, None
            for child in node.get_children():
                if child.is_leaf():  # if the child is a tip - parse number from tip label
                    if c:  # if there is a dictionary --> take the number from it --> the tree is a simulated tree
                        name = re.search("(.*)\-\d+", child.name)
                        if name:
                            num = {int(d.get(name.group(1)))}
                    else:  # the tree is the original tree
                        tmp = re.search("(\d+)", child.name)
                        if tmp:  # there is a number at the tip, and not X
                            num = {int(tmp.group(1))}
                else:  # if the child is an internal node - take number
                    num = child.name
                lst.append(num)
            intersect = lst[0] & lst[1]
            union = lst[0] | lst[1]
            if len(intersect) == 0:
                result = union
                score += 1
            else:
                result = intersect
            node.name = result

    return(score)

def acctran(t):
    command = "unset R_HOME; Rscript "
    script = "/groups/itay_mayrose/annarice/model_adequacy/code/analysis/phangorn.R "
    arg = t
    cmd = command + script + arg
    res = subprocess.Popen(cmd, shell=True, cwd=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    out, err = res.communicate()
    res = float(out[3:].strip())
    return(res)