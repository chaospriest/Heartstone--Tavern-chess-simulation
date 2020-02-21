import random

'''wrote by chaospriest'''


class Team(list):
    def __init__(self,name):                #其实好像没必要实例化重写list，思维江住了但后面都写好了就这样吧...
        self.name = name
        self.lose = 0


    def if_lost(self):
        if not len(self):
            self.lose = 1
    
    def __str__(self):                       #重写str以测试实际战斗情况（虽然最后还是很难看...）
        l = [self.name]
        for i in self:
            l.append('%s:%s%d'%(i.place,i.name,i.sheild))
        return str(l)


class Unit():
    def __init__(self,name,place,sheild,wind,deathword,ready_to_attack=0):   #实例化单位，具有种类，位置，圣盾，风怒,亡语属性，攻击权限
        self.name = name                         #如实例化风怒鱼人为Unit('murloc',x,1,1,2) ；实例化植物为Unit('plant',x,0,0,0)；目前将非鱼人都视为1-1植物，还有欠缺                         
        self.place = place                      #这个属性最后好像没用到...等以后开发狂战斧之类的可能有用
        self.sheild = sheild
        self.wind = wind
        self.deathword = deathword
        self.death = 0                           #death = 1判为单位死亡
        self.ready_to_attack = ready_to_attack   #为1时该随从在自己的回合便会攻击
    
    def attack(self,myteam,enemy):
        if len(enemy) > 1:
            target = random.randint(0,len(enemy)-1) #随机选取一个敌方单位
        elif len(enemy) == 1:
            target = 0   
        else:
            return
        if self.sheild:                            #自己有圣盾则圣盾消除
            self.sheild = 0
            
        else:
            if enemy[target].name == 'murloc' or self.name =='plant':
                self.death = 1                     #没有圣盾的情况下，如果自己是'植物'，无论敌方单位是什么，自己都死亡
                                                    #相反，如果敌方单位是鱼人，无论自己是什么，自己都死亡
            
         
        if enemy[target].sheild:
            enemy[target].sheild = 0               #如果敌方单位有圣盾则消除
        else:
            if enemy[target].name == 'plant' or self.name == 'murloc':
                enemy[target].death = 1            #同上理，在敌方单位没有圣盾的情况下，如果敌方是'植物'，无论自己是什么，敌方都死亡
                                                     #相反，如果自己是鱼人，无论敌方单位是什么，敌方单位都死亡
        death_balance(red)                          #红蓝队进行死亡结算
        death_balance(blue)

        if self.wind and not self.death and len(enemy):               #如果自己具有风怒同时未死亡同时敌方还有单位，再攻击一次
            if len(enemy) > 1:
                target = random.randint(0,len(enemy)-1) 
            else:
                target = 0     
            if self.sheild:                           
                self.sheild = 0
                
            else:
                if enemy[target].name == 'murloc' or self.name =='plant':
                    self.death = 1                    
             
            
            if enemy[target].sheild:
                enemy[target].sheild = 0              
            else:
                if enemy[target].name == 'plant' or self.name == 'murloc':
                    enemy[target].death = 1            
            death_balance(red)
            death_balance(blue)

            if not self.death:                                          #如果自己攻击后未死亡，将攻击权限传递给下一个随从
                self.ready_to_attack = 0                                
                place = myteam.index(self)+1
                if place == len(myteam):                                #如果自己是最后一个随从，传递给队伍第一个随从
                    myteam[0].ready_to_attack = 1
                else:
                    myteam[place].ready_to_attack = 1   
               



def death_balance(L):                                #死亡结算函数
    for r in L:                                      
        if r.death:                                  
            num = 0                                  #存储生成植物数量的变量
            place = L.index(r)                       #记录死亡随从位置的变量
            L.remove(r)                              #将死亡随从移除列表
            
            
            if r.deathword:             
                if r.deathword + len(L) > 7:           #如果有亡语，判断亡语数量是否超过随从上限
                    num = 7-len(L)
                else:
                    num = r.deathword

                while num:                              #生成植物对象，place属性会在后面统一改，暂时用x
                    num -= 1
                    u = Unit('plant','x',0,0,0)
                    L.insert(place,u)                   
                
            for i in L:
                i.place = L.index(i)                       #将单位place属性与列表位置统一


            # print(str(len(L))+str(place))
            if r.ready_to_attack and L:                    #如果死亡随从有攻击权限同时自己队伍还有单位，将攻击权限传递
                if place == len(L):                        #如果恰好最后一位随从死亡同时无随从替换自己位置，将权限递给队伍第一个；否则递给交替自己位置的随从
                    L[0].ready_to_attack = 1
                else:
                    L[place].ready_to_attack = 1
            break                                  #一次只会死亡一个随从，结算后立即跳出遍历


rw = 0
bw = 0
draw = 0

def game(fw,sw):

    for i in range(7):                              #初始化红蓝队，先生成鱼人，fw为红队是否风怒，sw为蓝队是否风怒
        red.append(Unit('murloc',i,1,fw,2))
        blue.append(Unit('murloc',i,1,sw,2))

    red[0] = Unit('plant',0,0,0,0,1)                #将红蓝队1和7号位改成植物，赋予1号攻击权限
    red[6] = Unit('plant',6,0,0,0)
    blue[0] = Unit('plant',0,0,0,0,1)
    blue[6] = Unit('plant',6,0,0,0)
   


    while (red.lose==0) and (blue.lose==0):   #红方先手
        for r in red:
            if r.ready_to_attack:
                r.attack(red,blue)
                break
        # print(str(red)+str(blue))
        
        red.if_lost()
        blue.if_lost()
        if (red.lose==1) or (blue.lose==1):
            break
        for b in blue:
            if b.ready_to_attack:
                b.attack(blue,red)
                break
        # print(str(red)+str(blue))
   
        red.if_lost()
        blue.if_lost()

    if red.lose and not blue.lose:
        global bw
        # print('blue win')
        bw += 1

    if blue.lose and not red.lose:
        global rw
        # print('red win')
        rw += 1
    
    if blue.lose and red.lose:
        global draw
        # print('draw')
        draw += 1


for i in range(1000000):      #测试结果代码，统计100000盘比赛结果，请小心运行，根据自己电脑情况决定具体数字
    red = Team('red')
    blue = Team('blue')
    game(1,0)

print('风怒先手赢'+str(rw))
print('无风怒后手赢'+str(bw))
print('平'+str(draw))



# for i in range(100000):
#     red = Team('red')
#     blue = Team('blue')
#     game(0,1)

# print('风怒后手赢'+str(rw))
# print('无风怒先手赢'+str(bw))
# print('平'+str(draw))