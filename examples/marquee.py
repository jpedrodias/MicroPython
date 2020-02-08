# filename: marquee.py
class Marquee():
  def __init__(self, lst=[], counts=5):
    self.lst = []
    self.counts = counts
    self.idx = 0
    self.count = 0
    self.add_lst( lst )
  def add(self, item=None):
    if item and type(item) == str:
      self.lst.append( item )
      return True
    else:
      return False
  def add_lst(self, lst=[]):
    for item in lst:
      self.add( item )
  def show(self):
    return self.lst
  def __repr__(self):
    _text = self.lst[self.idx]
    if self.count == self.counts - 1 :
      self.idx = (self.idx + 1) % len(self.lst)
    self.count = (self.count + 1 ) % self.counts
    return _text
  def __str__(self):
    return self.__repr__()
#End class Marquee

if __name__ == "__main__":
  pub = Marquee([ "*Clube Robotica*"," Laboratorio FQ ", "ColegioAtlantico"])
  for i in range(10):
    print(pub)
    
