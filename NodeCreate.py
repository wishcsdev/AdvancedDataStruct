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
    def add_child(self, NodeCreate):
      i = len(self.kids) - 1
      while i >= 0 and self.kids[i].keys[0] > NodeCreate.keys[0]:
        i -= 1
      return self.kids[:i + 1]+ [NodeCreate] + self.kids[i + 1:]
    def keyed_up(self, valuePassed):
      self.keys.append(valuePassed)
      self.keys.sort()
    def halfway(self, parent, valuePass):
      NodeCreate = self.__class__(self.ordered)
      middle = self.size//2
      mid_val = self.keys[middle]
      parent.keyed_up(mid_val)
      NodeCreate.kids = self.kids[middle + 1:]
      self.kids = self.kids[:middle + 1]
      NodeCreate.keys = self.keys[middle+1:]
      self.keys = self.keys[:middle]
      if len(NodeCreate.kids) > 0:
        NodeCreate.leaf = False
      parent.kids = parent.add_child(NodeCreate)
      if valuePass < mid_val:
        return self
      else:
        return NodeCreate