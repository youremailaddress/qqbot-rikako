class A:
    def __init__(self) -> None:
        self.A = 1
    
    def wjjj(func):
        def decor(self,**kwargs):
            return func(self,_a=3,b=2,c=1)
        return decor
    
    @wjjj
    def jajajaj(self,**kwargs):
        print(f"this is jajajaj {kwargs}")
    

m = A()
m.jajajaj(a=1,b=2,c=3)