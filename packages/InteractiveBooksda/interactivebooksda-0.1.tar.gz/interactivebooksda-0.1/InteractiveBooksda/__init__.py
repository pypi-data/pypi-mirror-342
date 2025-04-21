__author__ = 'DavidYdin'
__version__ = '1'
__email__ = 'David.2280@yandex.ru'
from webbrowser import *
from random import randint
print("Глава 1")
print("сначяло сознайте персонаж(а/ей) команда: 'имя персонажа = character()'")
print("патом запустите сюжет day_номер дня(имя играка название переменной при создание игра на одного!!!)")
print("всего дней ")
print("авторы David Yudin и ")
alive = True
def cube(n, k):
    a = 0
    for i in range(n):
        b = randint(1, k)
        print(f'вы выбили {b}')
        a += b
    print(f'в суме вышло {a}')
    return a
def sheker (ilist, eliment):
    for i in ilist:
        if i[0] == eliment:
            return i
class character :
    def __init__ (self):
        self.character_name = input('Кто ты воин: ')
        self.money = 0
        open(url='https://ttg.club/tools/ability-calc')
        print('из страки под названием Модиф')
        self.strength = int(input('сила: '))  #bonus
        self.sleight = int(input('ловкость: '))  #bonus
        self.physique = int(input('телосложение: '))  #bonus
        self.intelligence = int(input('интеллект: '))  #bonus
        self.wisdom = int(input('мудрость: '))  #bonus
        self.charisma = int(input('харизма: '))  #bonus
        open(url='https://ttg.club/classes')
        class_bonus = input("бонус класса заполнать 'название +-сколько' или 'нет': ").split()
        if class_bonus[0] =='сила':
            self.strength += int(class_bonus[1])
        elif class_bonus[0] =='ловкость':
            self.sleight += int(class_bonus[1])
        elif class_bonus[0] =='телосложение':
            self.physique += int(class_bonus[1])
        elif class_bonus[0] =='интеллект':
            self.intelligence += int(class_bonus[1])
        elif class_bonus[0] =='мудрость':
            self.wisdom += int(class_bonus[1])
        elif class_bonus[0] =='харнзма':
            self.charisma += int(class_bonus[1])
        Capabilities_bonus = input("выберети 2 бонуса умения: ").split()
        for i in Capabilities_bonus:
            if i =='сила':
                self.strength += 2
            elif i =='ловкость':
                self.sleight += 2
            elif i =='телосложение':
                self.physique += 2
            elif i =='интеллект':
                self.intelligence += 2
            elif i =='мудрость':
                self.wisdom += 2
            elif i =='харнзма':
                self.charisma += 2
        self.Mindfulness = int((self.wisdom-10)//2)
        self.Survival = int((self.wisdom-10)//2)
        self.Intimidation = int((self.charisma-10)//2)
        self.Sleight_of_Hand = int((self.sleight-10)//2)
        self.Magic = int((self.intelligence-10)//2)
        self.Medicine = int((self.wisdom-10)//2)
        self.Deception = int((self.charisma-10)//2)
        self.Persuasion = int((self.charisma-10)//2)
        self.weapon = []
        for i in range(int(input('сколько в тваём класе изначяльно оружия! из раздела Снаряжение: '))):
            self.weapon += [[input('название: '), input('колачество бросков на урон: '), input('кол во гаенй 1-го такого кубика: ')]]
        self.armor = []
        for i in range(int(input('сколько в тваём класе изначяльнй брони! из раздела Снаряжение: '))):
            self.armor += [[input('название: '), int(input('какая у этой брони зашита: '))]]
        self.spells = []
        for i in range(int(input('сколько в тваём класе закленаний из раздела закленания: '))):
                    self.spells += [[input('название: '), input('колачество бросков на урон: '), input('кол во гаенй 1-го такого кубика: ')]]
        ar = 0
        for i in self.armor:
            ar += i[1]
        self.xp = 100 + self.physique*10 + ar
    def say (self):
        # character_name money initiative xp bonus bonus bonus bonus bonus bonus Skills Skills Skills Skills Skills Skills Skills Skills weapon
        a = [self.character_name, self.money, self.xp, self.strength, self.sleight, self.physique, self.intelligence, self.wisdom, self.charisma, self.Mindfulness, self.Survival, self.Intimidation, self.Sleight_of_Hand, self.Magic, self.Medicine, self.Deception, self.Persuasion, self.weapon, self.armor, self.spells]
        return a
    def characteristics (self):
        # character_name money initiative xp bonus bonus bonus bonus bonus bonus Skills Skills Skills Skills Skills Skills Skills Skills
        a = [self.character_name, self.money, '1234567890', self.xp, self.strength, self.sleight, self.physique, self.intelligence, self.wisdom, self.charisma, self.Mindfulness, self.Survival, self.Intimidation, self.Sleight_of_Hand, self.Magic, self.Medicine, self.Deception, self.Persuasion]
        return a
    def inventory (self):
        # 
        a = [self.weapon, self.armor, self.spells]
        return a
    def damage (self, damag):
        self.xp -= damag
    def redakt_xp (self, xp):
        self.xp = xp
    def predmetw (self, predmet):
        self.weapon += predmet
    def predmeta (self, predmet):
        self.armor += predmet
    def mani1 (self, mani2):
        self.money += mani2
def monster (pers, name):
    global alive
    #   имя : [xp, урон, mani]
    a = {
        'test_monster':[100, 50, 10]
    }
    print(f'вы видете {name}')
    xp = a[name][0]
    print(f'у него здаровя {xp}')
    print(f'у него урон {a[name][1]}')
    ar = 0
    for i in pers.inventory()[1]:
        ar += i[1]
    pers.redakt_xp ( 100 + pers.characteristics()[6]*10 + ar )
    print(f'твоё здорове {pers.characteristics()[3]}')
    while True:
        if (xp > 0) and (pers.characteristics()[3] > 0) :
            b = input('атакуеш аружеем или магией (оружее/магия): ')
            if b == 'оружее':
                c = input('какое у аружее (название): ')
                d = sheker(pers.inventory()[0], c)
                e = cube(d[1], d[2])
                xp -= e
                print(f'вы натесли урона {e}')
            elif b == 'магия':
                c = input('какое у заклинание (название): ')
                d = sheker (pers.inventory()[0], c)
                e = cube(d[1], d[2]) + pers.characteristics()[5]
                xp -= e
                print(f'вы натесли урона {e}')
            pers.damage(a[name][1])
            print(f'твоё здорове {pers.characteristics()[3]}')
        elif xp < 0 or xp == 0:
            print('ты победил:', name)
            pers.mani1 (a[name][2])
            print(f'у тебя манет в сумме {pers.characteristics()[1]}')
            break
        elif pers.characteristics()[3] < 0 or pers.characteristics()[3] == 0:
            print('ты умер')
            if cube(4, 20) > 32:
                xp = a[name][0]
                ar = 0
                for i in pers.inventory()[1]:
                    ar += i[1]
                pers.redakt_xp ( 100 + pers.characteristics()[6]*10 + ar )
                print(f'твоё здорове {pers.characteristics()[3]}')
                break
            else :
                alive = False
                break
def find (pers, name, a):
    # a=0/1
    #0 = armor 1 = weapon
    ar = {
        'test_armor' : 10
    }
    #               броски, клв-ограней
    we = {
        'test_weapon' : [2, 20]
    }
    if a == 0:
        pers.predmeta([[name, ar[name]]])
        print(f'вы подобрали браню {name} на + {ar[name]} xp')
    elif a == 1:
        b = [name]
        b += we[name]
        pers.predmetw([b])
        print(f'вы подобрали аружее {name} кубик брасается {we[name][0]}K{we[name][1]}')
#______
David = character()
find (David, 'test_armor', 0)
find (David, 'test_weapon', 1)
monster (David, 'test_monster')