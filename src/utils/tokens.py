class Token :
    class Token:
          """
          A class representing a token in a program.
          """
    def _init_(self,val:str,type_:str):
         self.type=type_
         self.value=val
    
    def get_val(self) -> str:
         return self.value
    
    def get_type(self) ->str:
         return self.type
    
    def set_type(self,type_:str):
         self.type=type_

    def set_val(self,val:str):
         self.value=val

    def _str_(self):
         return f"<{self.type}:{self.value}>"
    
    def _repr_(self):
          return f"<{self.type}: {self.value}>"
    
    def _eq_(self,other):
         return self.type==other.type and self.value==other.value
    
    def _noteq_(self,other):
         return not self._eq_(other)
    
    def _hash_(self):
         return hash((self.type,self.value))

         