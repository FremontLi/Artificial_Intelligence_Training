# python中面向对象的开发
class Plane():
    # 构造方法，这是必须的
    def __init__(self,x,y,width,height): # 所有参数的第一个必须是self
        #super(ClassName, self).__init__(*args)#父类的方法
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    # 功能方法
    def move(self,step):
        self.x = self.x + step
        
# TODO lalala
# 创建对象
p1 = Plane(0,0,100,100)
for item in range(10):
    p1.move(5)
print(p1.x)

# 定义敌机类 继承Plane
class Enermy(Plane):
    def __init__(self,x,y,width,height):
        super(Enermy,self).__init__(x,y,width,height)
    # 特殊方法
    def shoot(self):
        print("射击")

e1 = Enermy(10,10,100,100)
e1.shoot()
e1.move(5)
print(e1.x)