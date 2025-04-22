class Calculator:
    # def __init__(self,firstoperand,secondoperand):
    #     self.firstoperand=firstoperand
    #     self.secondoperand=secondoperand
    
    def add(self,firstoperand,secondoperand):
        return float(firstoperand+secondoperand)
    
    def substract(self,firstoperand,secondoperand):
        return float(firstoperand-secondoperand)
    
    def multiply(self,firstoperand,secondoperand):
        return float(firstoperand*secondoperand)
    
    def divide(self,firstoperand,secondoperand):
        if self.secondoperand==0:
            print("The result leads to infinity bcz of zero, Pls provide valid number!!")
        else:
            return float(firstoperand/secondoperand)
        
# c=Calculator()
# print(c.add(10,11.5))
# print(c.multiply(10,11.5))
