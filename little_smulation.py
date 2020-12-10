import random
import copy
'''wrote by chaospriest'''



class Team():
    def __init__(self,name):
        self.team_name = name
        self.members = []
        #self.attacking = False
        self.attack_turn = 0
        self.enemyTeam = None

    def set_enemyTeam(self,team):
        self.enemyTeam = team

    def pass_atk_limit(self):
        self.attack_turn += 1
        if self.attack_turn == len(self.members):
            self.attack_turn = 0

    def team_attack(self):
        target = get_attack_target(self.enemyTeam)
        if self.attack_turn >= len(self.members):
            self.attack_turn = 0
        attacker = self.members[self.attack_turn]
        attacker.attack(self.enemyTeam.members[target])
        death_balance(self,target)                          #红蓝队进行死亡结算,清除死亡随从，添加亡语
        

        if attacker.wind and not attacker.death and len(self.enemyTeam):
            target = get_attack_target(self.enemyTeam)
            attacker.attack(self.enemyTeam.members[target])
            death_balance(self,target)                       #红蓝队进行死亡结算,清除死亡随从，添加亡语


    def apperence(self):                                  #显示当前状况       
        myTeam = self.members
        enemyTean = self.enemyTeam.members
        appstr = self.team_name + '>>'
        for u in myTeam:
            appstr += u.name + ':' + str(u.atk) + '-' + str(u.hp) + '===='
        print(appstr)

class Unit():
    def __init__(self,name,atk,hp,sheild,poison,wind,deathword,ready_to_attack=0):   #实例化单位，具有种类，位置，圣盾，风怒,亡语属性，攻击权限
        self.name = name                         #如实例化风怒鱼人为Unit('murloc',x,1,1,2) ；实例化植物为Unit('plant',x,0,0,0)；目前将非鱼人都视为1-1植物，还有欠缺                         
        # self.place = place                      #这个属性最后好像没用到...等以后开发狂战斧之类的可能有用
        self.sheild = sheild
        self.wind = wind
        self.deathword = deathword
        self.death = 0                           #death = 1判为单位死亡
        #self.ready_to_attack = ready_to_attack   #为1时该随从在自己的回合便会攻击
        self.hp = hp
        self.atk = atk
        self.poison = poison


   
        
    
    def attack(self,enemy):
        attack_balance(self,enemy)
        #以上为结算攻击者的生命和死亡

               




def attack_balance(attacker,be_attacked):            #攻击结算函数
    if attacker.sheild:                           #圣盾为最高优先级
        attacker.sheild = 0
    else:
        if be_attacked.poison:                #然后判断剧毒
            attacker.death = 1
        else:
            attacker.hp -= be_attacked.atk            #最后判断atk和hp
            if attacker.hp <= 0:
                attacker.death = 1
    #以上为结算攻击者的生命和死亡

    if be_attacked.sheild:
        be_attacked.sheild = 0              
    else:
        if attacker.poison:
            be_attacked.death = 1
        else:
            be_attacked.hp -= attacker.atk
            if be_attacked.hp <= 0:
                be_attacked.death = 1

    #以上为结算被攻击的生命和死亡

def get_attack_target(enemyTeam):                #获取攻击对象函数
    target = 0
    if len(enemyTeam.members) > 1:
        target = random.randint(0,len(enemyTeam.members)-1) #随机选取一个敌方单位
    elif len(enemyTeam.members) == 1:
        target = 0   
    return target

def death_balance(myTeam,target):               #死亡结算函数
    enemyTeam =  myTeam.enemyTeam                              
    attacker = myTeam.members[myTeam.attack_turn]
    enemy = myTeam.enemyTeam.members[target]
    if attacker.death:                                  
        num = 0                                  #存储生成植物数量的变量
        place = myTeam.attack_turn                 #记录死亡随从位置的变量
        myTeam.members.pop(place)                   #将死亡随从移除列表
        if attacker.deathword:             
            if attacker.deathword + len(myTeam.members) > 7:           #如果有亡语，判断亡语数量是否超过随从上限
                num = 7-len(myTeam.members)
            else:
                num = attacker.deathword

            while num:                              #生成植物对象，place属性会在后面统一改，暂时用x
                num -= 1
                u = Unit('plant',1,1,0,0,0,0)
                myTeam.members.insert(place,u)                   
    else:
        myTeam.pass_atk_limit()            
    if enemy.death:
        num = 0                                  #存储生成植物数量的变量
        place = target                 #记录死亡随从位置的变量
        if place < enemyTeam.attack_turn:
            enemyTeam.attack_turn -= 1
        enemyTeam.members.pop(place)                   #将死亡随从移除列表
        if attacker.deathword:             
            if attacker.deathword + len(enemyTeam.members) > 7:           #如果有亡语，判断亡语数量是否超过随从上限
                num = 7-len(enemyTeam.members)
            else:
                num = attacker.deathword

            while num:                              #生成植物对象，place属性会在后面统一改，暂时用x
                num -= 1
                u = Unit('plant',1,1,0,0,0,0)
                enemyTeam.members.insert(place,u) 

def game(redmem,bluemem,red_first,nums):
    red = Team("red")
    blue = Team("blue")

    
    redWin = 0
    blueWin = 0
    draw = 0
    red.set_enemyTeam(blue)
    blue.set_enemyTeam(red)


    for i in range(nums):
        red.members = copy.deepcopy(redmem)
        blue.members = copy.deepcopy(bluemem)
        if red_first:     #红方先手
            while len(red.members) and len(blue.members):                  
                red.team_attack()
                # red.apperence()
                # blue.apperence()
                if len(red.members) and len(blue.members):
                    blue.team_attack()
                    # red.apperence()
                    # blue.apperence()
                
                
        if not red_first:
            while len(red.members) and len(blue.members):                  
                blue.team_attack()
                if len(red.members) and len(blue.members):
                    red.team_attack()

        if (len(blue.members)==0) and (len(red.members)==0):
                draw += 1
        elif len(blue.members)==0:
            redWin += 1
        else:
            blueWin += 1

    return draw,redWin,blueWin



if __name__ == "__main__":
    from itertools import permutations
    redWin = 0
    blueWin = 0
    draw = 0    
    red_first = 1

    game_nums = 100000
    redmem = []
    bluemem = []

    redmem.append(Unit("孢子",1,1,0,1,0,0))
    redmem.append(Unit("孢子",1,1,0,1,0,0))
    redmem.append(Unit("白板33",3,3,0,0,0,0))
    redmem.append(Unit("白板33",3,3,0,0,0,0))

    bluememPool = []
    bluememPool.append(Unit("白板55",5,5,0,0,0,0))
    bluememPool.append(Unit("白板44",4,4,0,0,0,0))
    bluememPool.append(Unit("白板33",3,3,0,0,0,0))
    bluememPool.append(Unit("白板22",2,2,0,0,0,0))
    # random.shuffle(bluememPool)
    # for i in bluememPool:
    #     bluemem.append(i) 
    arrays = permutations(bluememPool)
    for a in arrays:
        a = list(a)
        draw,redWin,blueWin = game(redmem,a,red_first,game_nums)    
       
        title = "剧毒队先手"        
        
        
        blueTeamApperence = "--"

        for i in a:
            blueTeamApperence += i.name+"--"
        print("蓝队阵容："+blueTeamApperence)
        print(title+str(game_nums)+'盘的情况:剧毒队赢--'+str(redWin)+"  白板队赢--"+str(blueWin)+"  平局--"+str(draw)) 
        
        
        draw,redWin,blueWin = game(redmem,a,red_first-1,game_nums) 
        title = "剧毒队后手"  
        blueTeamApperence = "--"
        for i in a:
            blueTeamApperence += i.name+"--"
        print("蓝队阵容："+blueTeamApperence)
        print(title+str(game_nums)+'盘的情况:剧毒队赢--'+str(redWin)+"  白板队赢--"+str(blueWin)+"  平局--"+str(draw))