#!/usr/bin/python
# 
# CIS 472/572 -- Programming Homework #1
#
# Starter code provided by Daniel Lowd, 1/20/2017
# You are not obligated to use any of this code, but are free to use
# anything you find helpful when completing your assignment.
#
import sys
import re
# Node class for the decision tree
import node

import math


# SUGGESTED HELPER FUNCTIONS:
# - compute entropy of a 2-valued (Bernoulli) probability distribution 
# - compute information gain for a particular attribute
# - collect counts for each variable value with each class label
# - find the best variable to split on, according to mutual information
# - partition data based on a given variable

#Helper function: calcEntropy(val1, val2)
# - calculates entropy of two values and returns answer
# - formula: -(+val1/valTotal)log2(-val1/valTotal)
#	     - (+val2/valTotal)log2(-val2/valTotal)
def calc_Entropy(val1, val2):
  return -(float(val1) / (val1 + val2))*math.log(float(val1) / (val1 + val2), 2) - (float(val2) / (val1 + val2))*math.log(float(val2) / (val1 + val2), 2)

#Helper function: info_Gain(attr[])
def info_Gain(pEntropy, a1c1, a1c0, a0c1, a0c0):
  return pEntropy - (float(a1c1) + a1c0)/total * calc_Entropy(a1c1, a1c0) - (float(a0c1) + a0c0)/ total * calc_Entropy(a0c1, a0c0)

# Load data from a file
def read_data(filename):
  f = open(filename, 'r')
  p = re.compile(',')
  data = []
  header = f.readline().strip()
  varnames = p.split(header)
  namehash = {}
  for l in f:
    data.append([int(x) for x in p.split(l.strip())])
  return (data, varnames)

# Saves the model to a file.  Most of the work here is done in the 
# node class.  This should work as-is with no changes needed.
def print_model(root, modelfile):
  f = open(modelfile, 'w+')
  root.write(f, 0)

# Build tree in a top-down manner, selecting splits until we hit a
# pure leaf or all splits look bad.
def build_tree(data, varnames):
    # >>>> YOUR CODE GOES HERE <<<<
    # For now, always return a leaf predicting "1":
    
  attr = []
  val = []
  for index, entry in enumerate(varnames):
      attr.append(entry)
      val.append([0])
      val[index].append(0)
      val[index].append(0)
      val[index].append(0)

  for line in data:
    for index, x in enumerate(line):
      if ( x == 1):
        if ( line[len(line) - 1] == 1 ):
          val[index][0] += 1
        else:
          val[index][1] += 1
      else:
        if ( line[len(line) - 1] == 1):
          val[index][2] += 1
        else:
          val[index][3] += 1

#select new node
  current = 0.0
  for index, x in enumerate(attr):
    if ( x != '-' ):
      check = info_Gain(pEnt, val[index][0], val[index][1], val[index][2], val[index][3])
    if (check > current):
      current = check
      use = index

#create node
  parent = Node(attr[use])
  attr[use] = '-'
  recur_Tree(parent, attr[], val[])



  return node.Leaf(varnames, 1)

#Recursively form tree
def recur_Tree(pNode, attr[], val[]):

  if (len(attr) != 0 ):
    sNode = Split(pNode.names) 
    #select new node
    current = 0.0
    for index, x in enumerate(attr):
      if ( x != '-' ):
        check = info_Gain(pNode, val[index][0], val[index][1], val[index][2], val[index][3])
      if (check > current):
        current = check
        use = index

  if ( sNode.left == NULL):
    node = Split(attr[use])
    attr[use] = '-'
    recur_Tree(node, attr[], val[])

  if ( pNode.right == NULL):
    node = Split(attr[use])
    attr[use] = '-'
    recur_Tree(node, attr[], val[])

# Load train and test data.  Learn model.  Report accuracy.
def main(argv):
  if (len(argv) != 3):
    print 'Usage: id3.py <train> <test> <model>'
    sys.exit(2)
  # "varnames" is a list of names, one for each variable
  # "train" and "test" are lists of examples.  
  # Each example is a list of attribute values, where the last element in
  # the list is the class value.
  (train, varnames) = read_data(argv[0])
  (test, testvarnames) = read_data(argv[1])
  modelfile = argv[2]

  # build_tree is the main function you'll have to implement, along with
  # any helper functions needed.  It should return the root node of the
  # decision tree.
  root = build_tree(train, varnames)

  print_model(root, modelfile)
  correct = 0
  # The position of the class label is the last element in the list.
  yi = len(test[0]) - 1
  for x in test:
    # Classification is done recursively by the node class.
    # This should work as-is.
    pred = root.classify(x)
    if pred == x[yi]:
      correct += 1
  acc = float(correct)/len(test)
  print "Accuracy: ",acc

if __name__ == "__main__":
  main(sys.argv[1:])
