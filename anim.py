from abc import abstractstaticmethod
import turtle
from math import acos, asin, sin, cos, pi, sqrt
from typing import Reversible

wn  = turtle.Screen()
wn.bgcolor("white")
wn.title("Impact simulation")


def rotate(x0,y0,angle):  
    x1 =  x0*cos(angle) + y0*sin(angle)
    y1 = -x0*sin(angle) + y0*cos(angle)
    return x1,y1


def distance(turtle1, turtle2):
    r1 = [turtle1.xcor(),turtle1.ycor()]
    r2 = [turtle2.xcor(),turtle2.ycor()]
    return sqrt((r1[0]-r2[0])**2 + (r1[1]-r2[1])**2)

def rebound(ut,un):
    un *= -0.5
    return ut,un


rp = 10
rA = 50
rB = 150
xA = 0
xB = -(rA+rB)
ai = pi/2
vi_mag = 4
xu = -40
ru = rA + rp

if abs(xu) < ru: #p can collide with particle A
    xuB = (rB+rA)*sin(ai) + xu #shortest distance between centers of p and B
    ruB = rp+rB #shortest distance for p to be able to collide with B
    bi = acos(xu/ru) #set the impaction angle to A particle first
    if abs(xuB) <= ruB: # p hits the B first
        dl_AB = sqrt(ru**2-xu**2) - sqrt(ruB**2-xuB**2) - cos(ai)*(rA+rB)
        if(dl_AB<0): #p hits the B first
            bi = acos(xuB/ruB) #rebound angle, if p hits the A first

else: #p does not hit A nor B 
    print("vedle")
    bi = 0


impactor = turtle.Turtle()
impactor.shape("circle")
impactor.color("red")
impactor.shapesize(rp/10)
impactor.speed(0)
impactor.penup()
impactor.goto(-200*cos(ai) + xu*sin(ai),200*sin(ai) + xu*cos(ai))
impactor.dx =  vi_mag*cos(ai)
impactor.dy = -vi_mag*sin(ai)
impactor.pendown()


particle_A = turtle.Turtle()
particle_A.shape("circle")
particle_A.shapesize(rA/10)
particle_A.color("black")
particle_A.speed(0)
particle_A.penup()
particle_A.goto(0,0)


particle_B = turtle.Turtle()
particle_B.shape("circle")
particle_B.shapesize(rB/10)
particle_B.color("black")
particle_B.speed(0)
particle_B.penup()
particle_B.goto(-(rA+rB),0)


reboundA = False
reboundB = False
time = 0
while time < 100:
    time += 1
    #bounce
    if distance(impactor,particle_A) <= (rA+rp) and not reboundA:
        epsilon = bi - ai
        impactor.dt, impactor.dn = rotate(impactor.dx, impactor.dy, epsilon)
        impactor.dt, impactor.dn = rebound(impactor.dt, impactor.dn)
        br = bi
        ar = br + bi - ai
        impactor.dx, impactor.dy = rotate(impactor.dt, impactor.dn, -epsilon)
        print(impactor.dx, impactor.dy)

        ai = ar

        reboundA = True
        reboundB = False

        x_imp = (rA+rp)*sin(epsilon)
        y_imp = (rA+rp)*cos(epsilon)
        xu = y_imp*cos(ai) + (x_imp-xA)*sin(ai)
        if(abs(xu) < (rB+rp)):
            bi = acos(xu/(rB+rp))


    elif distance(impactor,particle_B) <= (rB+rp) and not reboundB:
        epsilon = bi - ai
        impactor.dt, impactor.dn = rotate(impactor.dx, impactor.dy, epsilon)
        impactor.dt, impactor.dn = rebound(impactor.dt, impactor.dn)
        br = bi

        ar = br + bi - ai

        impactor.dx, impactor.dy = rotate(impactor.dt, impactor.dn, -epsilon)

        ai = ar

        reboundB = True
        reboundA = False

        x_imp = xB + (rB+rp)*sin(epsilon)
        y_imp = (rB+rp)*cos(epsilon)
        xu = y_imp*cos(ai) + (x_imp-xA)*sin(ai)
        if(abs(xu) < (rA+rp)):
            bi = acos(abs(xu)/(rA+rp))


    #update impactor position
    impactor.setx(impactor.xcor() + impactor.dx)
    impactor.sety(impactor.ycor() + impactor.dy)


wn.mainloop()
