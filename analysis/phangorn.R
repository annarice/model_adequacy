require(phytools)
require(phangorn)

args = commandArgs(trailingOnly=TRUE)
tree = read.newick(args[1])
counts = c()
for (i in 1:(tree$Nnode+1)){
  counts = c(counts, as.numeric(gsub("[^0-9]", "",  tree$tip.label[i])))
  tree$tip.label[i] = gsub('-[0-9]+', '', tree$tip.label[i])
}

mat_data = matrix(counts,dimnames = list(tree$tip.label,NULL), nrow=length(counts), byrow=TRUE)
data = phyDat(mat_data, type = "USER", levels = unique(counts))
tmp = acctran(tree,data)

mat = as.data.frame(cbind(tree$edge,tree$edge.length,tmp$edge.length,0))
names(mat) = c("begin","end","length","parsimony","time")
distances = dist.nodes(tree)
root_ind = which(node.depth.edgelength(tree)==0)
for (i in 1:nrow(mat)){
  end = mat$end[i]
  mat$time[i] = distances[root_ind,end]
}

x = mat$time
y = mat$parsimony

lm = lm(y~x)
result = round(lm$coefficients[2],4)
names(result) = NULL
print(result)



