from ete3 import Tree
import regex as re
import argparse

parser = argparse.ArgumentParser(description="Calculates the number of intersections of trait in internal nodes")
parser.add_argument('--tree', '-t', help='Newick tree with traits in the tip label, e.g., mlAncestors.tree',required=True)

args = parser.parse_args()
tree_file = args.tree

t = Tree(tree_file, format = 1)

score = 0
score = fitch(score,t)

def fitch(score,t):
	for node in t.traverse("postorder"):
		node.add_feature("state",0)
		if not node.is_leaf(): # internal node
			lst = []
			intersect, union = None, None
			for child in node.get_children():
				if child.is_leaf(): # if the child is a tip - parse number from tip label
					tmp = re.search("(\d+)",child.name)
					num = {int(tmp.group(1))}
					#child.name = num
					child.state = num
				else: # if the child is an internal node - take number
					num = child.state
				lst.append(num)
			intersect = lst[0] & lst[1]
			union = lst[0] | lst[1]
			if len(intersect) == 0:
				result = union
				score += 1
			else:
				result = intersect
			node.state = result
	print(str(score))
	return(t)

def distance_of_change(tmp_tree,tmp_node):
	if tmp_node.is_root():
		return(0)
	else:
		return(tmp_tree.get_distance(tmp_node.name) + (tmp_node.dist*0.5))

def fitch_original(score,t):
	for node in t.traverse("postorder"):
		if not node.is_leaf(): # internal node
			lst = [] # list version
			intersect, union = None, None
			for child in node.get_children():
				#print(child.name)
				if child.is_leaf(): # if the child is a tip - parse number from tip label
					tmp = re.search("(\d+)",child.name)
					num = {int(tmp.group(1))}
				else: # if the child is an internal node - take number
					num = child.name
				lst.append(num)
			intersect = lst[0] & lst[1]
			union = lst[0] | lst[1]
			#print ("intersect " + str(intersect))
			#print("union " + str(union))
			if len(intersect) == 0:
				result = union
				score += 1
			else:
				result = intersect
			node.name = result
		print(node.name)
	print(str(score))