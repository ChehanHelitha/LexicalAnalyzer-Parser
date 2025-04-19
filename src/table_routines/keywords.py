# Set of reserved keywords in RPAL
class Keywords:
     def _init_(self):
          
          self.keyword={
               "let",   # Used for variable declaration
               "in" ,   # Used for scoping
               "fn",    #Used for function definition
               "where", #Used for local definitions
               "aug",   #Augmentation operator
               "or",    #Logical OR operator
               "not",   #Logical NOT operator
               "gr",    #Greater than operator
               "ge",    #Greater than or equal to operator
               "ls",    #Less than operator
               "le",    #Less than or equal to operator
               "ne",    #Not equal to operator
               "true",  #Boolen value for true
               "false", #Boolean value for false
               "nil", #Empty list value,
               "dummy", #Dummy value
               "within",#Used for scoping
               "and",  #Logical AND operator
               "rec", #Used for recursive function definition
          }