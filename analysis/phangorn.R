require(phytools)
require(phangorn)

# arguments: (1) working_dir (2) number of iterations (1 for original counts, n for simulations)
# output: list of calculated statistic N times

args = commandArgs(trailingOnly=TRUE)
working_dir = args[1]
iter = args[2]

calculate_stat = function(tree){
	counts = c()
	
	for (i in 1:(tree$Nnode+1)){
	  counts = c(counts, as.numeric(gsub("[^0-9]", "",  tree$tip.label[i])))
	  tree$tip.label[i] = gsub('-[0-9]+', '', tree$tip.label[i])
	}
	mat_data = matrix(counts,dimnames = list(tree$tip.label,NULL), nrow=length(counts), byrow=TRUE)
	data = phyDat(mat_data, type = "USER", levels = unique(counts))
	tmp = acctran(tree,data)

	#mat = as.data.frame(cbind(tree$edge,tree$edge.length,tmp$edge.length,0))
	#names(mat) = c("begin","end","length","parsimony","time")
	tmp_mat = as.data.frame(cbind(tmp$edge,tmp$edge.length))
	names(tmp_mat) = c("begin","end","parsimony")
	tree_mat = as.data.frame(cbind(tree$edge,tree$edge.length))
	names(tree_mat) = c("begin","end","time")
	mat = merge(tree_mat, tmp_mat, by=c("begin","end"))
	mat$time = 0
	distances = dist.nodes(tree)
	root_ind = which(node.depth.edgelength(tree)==0)
	for (i in 1:nrow(mat)){
	  end = mat$end[i]
	  mat$time[i] = distances[root_ind,end]
	}

	x = mat$time
	y = mat$parsimony

	lm = lm(y~x)
	result = round(lm$coefficients[2],2)
	names(result) = NULL
	#results_lst = append(results_lst,result)
	return(result)
}

results_lst = c()
if (iter==1){
	tree_file = "tree_with_counts.tree"
	tree = read.newick(paste(working_dir,tree_file,sep="/"))
	results_lst = calculate_stat(tree)
} else {
	tree_file = "simTree.phr"
	for (n in (1:iter)-1){
		tree = read.newick(paste(working_dir,n,"simTree.phr",sep="/"))
		stat = try(calculate_stat(tree))
		if (inherits(stat,'try-error')){
			next
		}
		results_lst = append(results_lst,stat)
	}
}

cat(results_lst)

