

from NodeCreate import NodeCreate
import sys


#Citations-https://www.geeksforgeeks.org/b-tree-set-1-introduction-2/
#Citations-https://cs.stackexchange.com/questions/6799/are-degree-and-order-the-same-thing-when-referring-to-a-b-tree
#Citations-http://www.cs.carleton.edu/faculty/jgoldfea/cs201/spring11/inclass/Tree/BTreefinalNew.pdf- slide24
#Citations-https://github.com/alansammarone/BTree/blob/master/btree.py
#Citations-https://www.guru99.com/reading-and-writing-files-in-python.html#4
#Citations-https://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work
#Citations-https://www.nayuki.io/res/As2-set/btreeset.py
#Citations-

						
						
class As2(object):
  
  class NodeCreate(object):
    def __init__(self, order):
      self.leaf = True
      self.ordered = order
      self.pointers=[]
      self.keys = []
      self.kids = []
    @property
    def noRoom(self):
      return self.size == 2 * self.ordered - 1
    @property
    def size(self):
      return len(self.keys)
    def add_child(self, nodeCreate):
      i = len(self.kids) - 1
      while i >= 0 and self.kids[i].keys[0] > nodeCreate.keys[0]:
        i -= 1
      return self.kids[:i + 1]+ [nodeCreate] + self.kids[i + 1:]
    def keyed_up(self, valuePassed):
      self.keys.append(valuePassed)
      self.keys.sort()
    def halfway(self, parent, valuePass):
      nodeCreate = self.__class__(self.ordered)
      middle = self.size//2
      mid_val = self.keys[middle]
      parent.keyed_up(mid_val)
      nodeCreate.kids = self.kids[middle + 1:]
      self.kids = self.kids[:middle + 1]
      nodeCreate.keys = self.keys[middle+1:]
      self.keys = self.keys[:middle]
      if len(nodeCreate.kids) > 0:
        nodeCreate.leaf = False
      parent.kids = parent.add_child(nodeCreate)
      if valuePass < mid_val:
        return self
      else:
        return nodeCreate
  
  def __init__(self, order):
    
    self.ordered = order
    self.root = self.NodeCreate(order)
    return
  def count_node(self, NodeCreate):
    #NodeCreate = self.root
    if NodeCreate is None:      
      NodeCreate=self.root
      return 0
    else:
      count=1
      for child in NodeCreate.kids:
        count += self.count_node(child)
        #count=count+self.count_node(child)
      return count
  def Find_key(self, valuePassed, NodeCreate):
    if NodeCreate is None:
      NodeCreate = self.root
      print ("no NodeCreate exists")
      return 
    if valuePassed in NodeCreate.keys:
      print ("Key is present in the data set")
	  #return True
    elif NodeCreate.leaf:
      # If we are in a leaf, there is no more to check.
      print ("Key is not present in the data set")
	  #return False
    else:
      i = 0
      while i < NodeCreate.size and valuePassed > NodeCreate.keys[i]:
        i += 1
      return self.Find_key(valuePassed, NodeCreate.kids[i]) 
  def AddNewkey(self, valuePass):
    NodeCreate = self.root
    if NodeCreate.noRoom:
      new_root = self.NodeCreate(self.ordered)
      new_root.kids.append(self.root)
      new_root.leaf = False
      NodeCreate = NodeCreate.halfway(new_root, valuePass)
      self.root = new_root
    while not NodeCreate.leaf:
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

    
  #def calc_depth(self, NodeCreate):
      
      #if NodeCreate is None:
        #NodeCreate=self.root
        #return 0
	  
      #else:
	   #count=1
	    #list=[]
        #for i in NodeCreate.kids: 
          #count += NodeCreate.kids[i]
		  #self.calc_depth(NodeCreate.kids[i])
		  
		#list.append(count)
		  #self.calc_depth()
        #return count
	  
if __name__ == '__main__':
	
		f=open(sys.argv[1],'r')
		tree=As2(int(sys.argv[2]))
		for line in f:
			print(int(line))
			tree.AddNewkey(int(line))
			
		search_k=input("Enter key to Find_key:")
		k=int(search_k)
		tree.Find_key(k,tree.root)
		
		with open(sys.argv[1],'r') as ins:
			array=[]
			for line in ins:
				array.append(line)
		print("number of keys", len(array))
		
		tree.count_node(tree.root)
		print ("Number of nodes", int(tree.count_node(tree.root)))
		
		#depth of tree
		#print("Depth of tree is", int(tree.calc_depth(tree.root))
		
