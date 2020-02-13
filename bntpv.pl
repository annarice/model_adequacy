#!/usr/bin/perl
use strict;
use chromevol;

my $expFile = "/groups/itay_mayrose/annarice/model_adequacy/genera/Jasminum/BASE_NUM/expectations.txt"
my $mlAncTree = "/groups/itay_mayrose/annarice/model_adequacy/genera/Jasminum/BASE_NUM/mlAncestors.tree"
my $baseNum = 13

my $tmp = create_bntpv($expFile, $mlAncTree, $baseNum);
print($tmp);
