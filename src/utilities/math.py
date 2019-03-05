class Complex:
   def __init__(self, real, img):
      self.real = real
      self.img = img

   def toString(self):
      print('real:' , self.real, ' img:', self.img)

   def add(self, real, img):
      self.real += real
      self.img += img
