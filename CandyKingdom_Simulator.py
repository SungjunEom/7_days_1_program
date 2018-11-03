#CandyKingdom_Simulator v0.0.0

from enum import Enum
from random import *
from time import sleep
import numpy as np
import cv2
from math import sqrt

img = np.zeros((600,600,3), np.uint8)

class Alive(Enum):
    Mad = 0
    Angry = 1
    Curious = 2
    Chasing = 3
    Starving = 4
    Happy = 5
    Sleepy = 6
    Gravity = 7

class ST(Enum):
    Dead = -1
    Sleep = 0
    Alive = 1

class State:
    def __init__(self, cur_stat = ST.Alive, cur_doing = Alive.Happy):
        self.CurrentState = cur_stat
        self.Doing = cur_doing
        self.x = randint(0,600)
        self.y=  randint(0,600)

def ShowCandyPeopleStates(people):
    iter = 0
    for i in people:
        #print('CandyPerson number', iter, ' is now ', i.CurrentState, ' and ', i.Doing, ' in ', '(',i.x,', ', i.y, ')', sep = '')
        if i.CurrentState == ST.Dead:
            cv2.circle(img,(i.x,i.y), 3, (0,0,255), -1)
            #cv2.circle(img,(i.x,i.y), 3, (0,0,0), -1)
        elif i.CurrentState == ST.Alive:
            if i.Doing == Alive.Chasing:
                cv2.circle(img, (i.x, i.y), 3, (0,255,255), -1)
            elif i.Doing == Alive.Mad:
                cv2.circle(img, (i.x, i.y), 3, (255,0,255), -1)
            else:
                cv2.circle(img,(i.x,i.y), 3,(0,255,0), -1)
        #cv2.imshow('CandyKingdom', img)
        #cv2.waitKey(0)
        iter += 1
    cv2.imshow('CandyKingdom', img)
    cv2.rectangle(img,(0,0),(600,600),(0,0,0),-1)
    cv2.waitKey(1)

def CreateCandyPeople(people, cur_stat = None, cur_alive_stat = None):
    if cur_stat == None:
        cur_stat = choice(list(ST))
        cur_alive_stat = choice(list(Alive))
        people.append(State(cur_stat, cur_alive_stat))
    elif cur_stat == ST.Dead:
        people.append(State(ST.Dead, Alive.Sleepy))
    elif cur_stat == ST.Sleep:
        people.append(State(ST.Sleep, Alive.Sleepy))
    elif cur_stat == ST.Alive:
        if cur_alive_stat == None:
            people.append(State(ST.Alive,choice(list(Alive))))
        else:
            people.append(State(ST.Alive, cur_alive_stat))
    else:
        pass

def IsBoarder(person):
    if person.x > 600:
        person.x = 600
    if person.y > 600:
        person.y = 600
    if person.x < 0:
        person.x = 0
    if person.y < 0:
        person.y = 0

def UpdateWorld(people):
    #Mad interrupt
    for  outer in people:
        counter = 0
        if outer.CurrentState == ST.Alive and outer.Doing == Alive.Mad:
            for inner in people:
                if outer is inner:
                    continue
                elif abs(outer.x - inner.x) < 5 and abs(outer.y - inner.y) < 5:
                    if inner.Doing == Alive.Mad:
                        pass
                        #outer.CurrentState = ST.Dead
                        #inner.CurrentState = ST.Dead
                    elif inner.Doing == Alive.Chasing:
                        #outer.Doing = Alive.Angry
                        outer.Doing = Alive.Happy
                    else:
                        #inner.CurrentState = ST.Dead
                        inner.Doing = Alive.Mad
                        #outer.Doing = Alive.Happy
        if outer.CurrentState == ST.Sleep:
            for inner in people:
                if outer is inner:
                    continue
                elif abs(outer.x - inner.x) < 5 and abs(outer.y - inner.y) < 5:
                    if inner.CurrentState != ST.Sleep:
                        outer.CurrentState = ST.Alive
                        #Angry or Starving go to Mad
        if outer.CurrentState == ST.Alive and (outer.Doing == Alive.Starving or outer.Doing == Alive.Angry):
            for inner in people:
                if outer is inner:
                    continue
                elif abs(outer.x - inner.x) < 15 and abs(outer.y - inner.y) < 15:
                    if counter > 2:
                        outer.Doing = Alive.Mad
                        counter = 0
                    counter += 1
        if outer.CurrentState == ST.Alive and (outer.Doing != Alive.Mad and outer.Doing != Alive.Chasing):
            for inner in people:
                if outer is inner:
                    continue
                elif abs(outer.x - inner.x) < 15 and abs(outer.y - inner.y) < 15 and inner.Doing == Alive.Chasing:
                    #inner.Doing = Alive.Happy
                    pass
                    
        if outer.CurrentState == ST.Alive and outer.Doing == Alive.Curious:
            Coord = [600,600]
            Length = sqrt(Coord[0]*Coord[0] + Coord[1]*Coord[1])
            for inner in people:
                if outer is inner:
                    continue
                
                x__ = outer.x - inner.x
                y__ = outer.y - inner.y

                Length__ = sqrt(x__*x__ + y__*y__)
                if Length > Length__:
                    Coord[0] = x__
                    Coord[1] = y__
                    Length = Length__
                
            if Coord[0] < 200:
                if Coord[0] != 0:
                    outer.x -= int(5*(Coord[0] / abs(Coord[0])))
            if Coord[1] < 200:
                if Coord[1] != 0:
                    outer.y -= int(5*(Coord[1]/ abs(Coord[1])))
                    ''' #Gravity
        if outer.CurrentState == ST.Dead:
            Coord = [600, 600]
            for inner in people:
                if outer is inner:
                    continue
                if inner.Doing == Alive.Gravity:
                    x__ = outer.x - inner.x
                    y__ = outer.y - inner.y
                    if x__ != 0:
                        outer.x -= int(3*(x__/abs(x__)*(1/x__*x__)))
                    if y__ != 0:
                        outer.y -= int(3*(y__/abs(y__)*(1/y__*y__)))
                        '''


    #Move people
    for person in people:
        if person.CurrentState == ST.Alive and person.Doing == Alive.Chasing:
            x_plus = randint(-15, 15)
            y_plus = randint(-15, 15)
            person.x += x_plus
            person.y += y_plus
            IsBoarder(person)
            
        elif person.CurrentState == ST.Alive and person.Doing == Alive.Mad:
            x_plus = randint(-5, 5)
            y_plus = randint(-5, 5)
            person.x += x_plus
            person.y += y_plus
            IsBoarder(person)
            
        elif person.CurrentState == ST.Dead:
            continue
        elif person.CurrentState == ST.Sleep and person.Doing == Alive.Chasing:
            x_plus = randint(-1, +1)
            y_plus = randint(-1, +1)
            person.x += x_plus
            person.y += y_plus
            IsBoarder(person)
        else:
            person.x += randint(-2, +2)
            person.y += randint(-2, +2)
            IsBoarder(person)


CandyPeopleList = list()
#CreateCandyPeople(CandyPeopleList)
#ShowCandyPeopleStates(CandyPeopleList)

while(True):
    print("How many candypeople do you want to create?>", end = '')
    create_num = input()
    try:
        create_num = int(create_num)
        for i in range(create_num):
            CreateCandyPeople(CandyPeopleList,ST.Alive)
    except ValueError:
        if create_num == 'end':
            break
        else:
            print('Please enter an integer')
    ShowCandyPeopleStates(CandyPeopleList)
'''
#스크린 버퍼 문제
print('Entered a simulated reality.', end='')
print('',end='')
sleep(0.5)
print('.', end='')
print('',end='')
sleep(0.5)
print('.', end='')
print('',end='')
sleep(0.5)
print('.', end='')
'''
count = 0
while(True):
    UpdateWorld(CandyPeopleList)
    #sleep(0.005)
    ShowCandyPeopleStates(CandyPeopleList)

    if count > 50:
        AliveNormal = 0
        AliveAngry = 0
        AliveMad = 0
        Dead = 0
        for person in CandyPeopleList:
            if person.CurrentState == ST.Alive:
                if person.Doing == Alive.Angry:
                    AliveAngry += 1
                elif person.Doing == Alive.Mad:
                    AliveMad += 1
                else:
                    AliveNormal += 1
            elif person.CurrentState == ST.Dead:
                Dead += 1
            else:
                pass
        print('Normal:Angry:Mad:Dead')
        print(AliveNormal, AliveAngry, AliveMad, Dead)
        count = 0

    count += 1