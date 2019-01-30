#from NodeCreate import NodeCreate
import sys
#Python 3.6 

#Vishaal Bakshi
#UCID 00305550
#CPSC 335 Assignment 2

#Citations-https://www.geeksforgeeks.org/b-tree-set-1-introduction-2/
#Citations-https://cs.stackexchange.com/questions/6799/are-degree-and-order-the-same-thing-when-referring-to-a-b-tree
#Citations-http://www.cs.carleton.edu/faculty/jgoldfea/cs201/spring11/inclass/Tree/BTreefinalNew.pdf- slide24
#Citations-https://github.com/alansammarone/BTree/blob/master/btree.py
#Citations-https://www.guru99.com/reading-and-writing-files-in-python.html#4
#Citations-https://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work
#Citations-https://www.nayuki.io/res/As2-set/btreeset.py

#THIS PROGRAM TAKES 2 ARGUMENTS FROM COMMAND LINE. FIRST ARGUMENT IS THE TXT filename AND SECOND ARGUMENT IS THE B-TREE ORDER number

#the purpose of the program is to build a b-tree after order is provided by user in command line and then be able to search by key values
#it also displays the number of nodes in the tree and the depth of the tree 
						
						
class As2(object):
  
  class NodeCreate(object):
    def __init__(self, order):				#initializer for NodeCreate class
      self.leaf = True
      self.ordered = order
      self.pointers=[]
      self.keys = []
      self.kids = []
    @property
    def noRoom(self):						#condition for when node is full
      return self.size == 2 * self.ordered - 1
    @property
    def size(self):							#number of keys store in the list
      return len(self.keys)
    def add_child(self, nodeCreate):		#insert function when value passed from reading file
      i = len(self.kids) - 1
      while i >= 0 and self.kids[i].keys[0] > nodeCreate.keys[0]:
        i -= 1
      return self.kids[:i + 1]+ [nodeCreate] + self.kids[i + 1:]
    def keyed_up(self, valuePassed):		#when you need to move the key up by splitting the node
      self.keys.append(valuePassed)
      self.keys.sort()
    def halfway(self, parent, valuePass):      #split node when node value exceeded
      nodeCreate = self.__class__(self.ordered)
      middle = self.size//2						#half way mark in the node
      mid_val = self.keys[middle]
      parent.keyed_up(mid_val)					#move the middle value up using parent
      nodeCreate.kids = self.kids[middle + 1:]	#move middle index to right for splitting
      self.kids = self.kids[:middle + 1]		#move middle index to left for splitting
      nodeCreate.keys = self.keys[middle+1:]	#repeat for keys
      self.keys = self.keys[:middle]
      if len(nodeCreate.kids) > 0:				#the list of kids should not be empty. if it is then we are at leaf
        nodeCreate.leaf = False
      parent.kids = parent.add_child(nodeCreate)   
      if valuePass < mid_val:
        return self
      else:
        return nodeCreate
  
  def __init__(self, order):					#initializer for As2
    
    self.ordered = order
    self.root = self.NodeCreate(order)			#pass it to NodeCreate initializer
    return
  def count_node(self, NodeCreate):				#counting the total number of nodes
    #NodeCreate = self.root
    list=[]										#create empty list to put the count of nodes into
    if NodeCreate is None:      
      NodeCreate=self.root
      return 0
    else:
      count=1
      for child in NodeCreate.kids:				#for every child of the nodes count it as a node 
        count += self.count_node(child)
        list.append(count)						#add the values to the list
        #print(count)
        #count=count+self.count_node(child)
      return sum(list)							#sum the values inside the list to get the total nodes
      #return count
  def Find_key(self, valuePassed, NodeCreate):	#search by key value
    if NodeCreate is None:						#node shouldn't be empty
      NodeCreate = self.root					# if it is then point it to the root and print the statement
      print ("no NodeCreate exists")
      return 
    if valuePassed in NodeCreate.keys:			#if the value passed is in the keys list print the statement
      print ("Key is present in the data set")
	  #return True
    elif NodeCreate.leaf:
      # If we are in a leaf, there is no more to check.
      print ("Key is not present in the data set")
	  #return False
    else:										#keep traversing through recursively until list is exhausted
      i = 0
      while i < NodeCreate.size and valuePassed > NodeCreate.keys[i]:
        i += 1
      return self.Find_key(valuePassed, NodeCreate.kids[i])
	
 # def in_order(self,NodeCreate):
      #root=self.root
        #x=[]
        #for keys in NodeCreate.keys:
          #x.append(NodeCreate.keys)
          #print (x)
		#for keys in tree.root.keys:
          #x.append(tree.root.keys)
          #print(x)
        #if not NodeCreate.kids:
          #yield from NodeCreate.keys
          #print("Empty",NodeCreate.values)
        #else:
          #for i in NodeCreate.kids:
            #yield from self.items(NodeCreate.kids[i])
            #print ("hmmmm",NodeCreate.keys)
          #for index, value in enumerate(NodeCreate.keys):
            #yield value
            #yield from self.items(NodeCreate.kids[index+1])
          #print ("Enumerate",NodeCreate.keys)
        #return NodeCreate.keys
  
  def AddNewkey(self, valuePass):				#insert the key from the txt file line by line
    NodeCreate = self.root
    if NodeCreate.noRoom:						#if node is full, create a new one
      newNode = self.NodeCreate(self.ordered)
      newNode.kids.append(self.root)
      newNode.leaf = False
      NodeCreate = NodeCreate.halfway(newNode, valuePass)	#split the node
      self.root = newNode
      #print (NodeCreate.keys)
    while not NodeCreate.leaf:								#if the node is not the leaf then reduce size and check where to put value
      i = NodeCreate.size - 1
      while i > 0 and valuePass < NodeCreate.keys[i] :
        i -= 1
      if valuePass > NodeCreate.keys[i]:
        i += 1
      next = NodeCreate.kids[i]
      if next.noRoom:
        NodeCreate = next.halfway(NodeCreate, valuePass)
      else:
        NodeCreate = next
    NodeCreate.keyed_up(valuePass)

  def print_my_tree(self):					#print my tree output
      current_pos = [self.root]				#start at the root
      while current_pos:
        position = []						#create empty list to store it into
        store_val = []
        for node in current_pos:			#for the current node take its children and add it to the end of the list
          if node.kids:
           position.extend(node.kids)
          store_val.extend(node.keys)  #store the value as a string 
		#print(store_val[0])
        print(store_val)
        #for i in store:
		
        current_pos = position				#update the current position

  def calc_depth(self, NodeCreate):
      if NodeCreate is None:				#if root node is null then depth is zero
        NodeCreate=self.root
        return 0
      else:
        count=1
        #list=[]
        for kid in NodeCreate.kids[0:1]: 	#for the first child of the parent count the edge
          count += count					
          self.calc_depth(kid)				#recursively calculate the number of edges from the parent to first child
          #print (count)
        return count+1						#add the count value to 1 since root is at level 1		
		#list.append(count)
		  #self.calc_depth()
        #return count
		


if __name__ == '__main__':					#driver 
	
		f=open(sys.argv[1],'r')
		tree=As2(int(sys.argv[2]))			#create the tree by taking in passed in B-TREE order provided by user
		for line in f:
			#print(int(line))
			tree.AddNewkey(int(line))		#create tree by inserting all values from file
			
		search_k=input("Enter key to Find_key:")			#search for key provided by user
		k=int(search_k)
		tree.Find_key(k,tree.root)
		
		with open(sys.argv[1],'r') as ins:					#total number of keys in file
			array=[]
			for line in ins:
				array.append(line)
		print("number of keys", len(array))
		
		tree.count_node(tree.root)
		print ("Number of nodes", int(tree.count_node(tree.root)))		#number of nodes 
		
		print("Depth of tree is", int(tree.calc_depth(tree.root)))		#depth of tree
		
		print(tree.print_my_tree())										#print my tree
		
		
		
		#x=[]
		#for keys in tree.root.keys:
			#x.append(tree.root.keys)
			#print(x)
			#x[0][:]=[int(y) for y in x[0]]
			#x=[int("".join([str(y) for y in a])) for a in x]
			#print("In_order",(tree.in_order(x)))
		
		#depth of tree
		#print("Depth of tree is", int(tree.calc_depth(tree.root))
