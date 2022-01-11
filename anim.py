from abc import abstractstaticmethod
import turtle
from math import acos, asin, sin, cos, pi, sqrt

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


def impact_location(d1, dp, off, ai):
    ru = (d1+dp)/2
    xspr = ru*cos(acos(xu/ru) + pi/2 - ai)
    yspr = sqrt(ru**2 - xspr**2)
    return [xspr,yspr]


def dot(u,v):
    dot_uv = 0.0
    for i in range(len(u)):
        dot_uv += u[i]*v[i]
    return dot_uv

def mag2(u):
    return dot(u,u)



dp = 20
dA = 120
dB = 120
ai = pi/3
vi_mag = 5
xu = -1.0
du = (dp + dA)/2

if xu < (dA+dp)/2:
    if xu > (dB - (dB+dA)*sin(ai) + dp) / 2:
        bi = acos(2*xu/(dA+dp))
    else:
        bi = acos(2/(dB+dp)*(xu +(dA+dB)*sin(ai)/2))
else:
    print("vedle")
    bi = 0


impactor = turtle.Turtle()
impactor.shape("circle")
impactor.color("red")
impactor.shapesize(dp/20)
impactor.speed(0)
impactor.penup()
impactor.goto(-200*cos(ai) + xu*sin(ai),200*sin(ai) + xu*cos(ai))
impactor.dx =  vi_mag*cos(ai)
impactor.dy = -vi_mag*sin(ai)
impactor.pendown()


particle_A = turtle.Turtle()
particle_A.shape("circle")
particle_A.shapesize(dA/20)
particle_A.color("black")
particle_A.speed(0)
particle_A.penup()
particle_A.goto(0,0)


particle_B = turtle.Turtle()
particle_B.shape("circle")
particle_B.shapesize(dB/20)
particle_B.color("black")
particle_B.speed(0)
particle_B.penup()
particle_B.goto(-(dA+dB)/2,0)


reboundA = False
reboundB = False
time = 0
while time < 100:
    time += 1
    #bounce
    if distance(impactor,particle_A) <= (dA+dp)/2 and not reboundA:
        impactor.dx1, impactor.dy1 = rotate(impactor.dx, impactor.dy, ai)
        impactor.dn, impactor.dt = rotate(impactor.dx1, impactor.dy1, bi)

        impactor.dn *= -1

        br = -bi
        ar = br + bi - ai

        impactor.dx1, impactor.dy1 = rotate(impactor.dn, impactor.dt, br)
        impactor.dx, impactor.dy = rotate(impactor.dx1, impactor.dy1, -ai)

        spr = impact_location(dA,dp,xu,ai)
        sB = [-dB/2, 0]
        s = [spr[0]-sB[0],spr[1]-sB[1]]
        ur = (impactor.dx, impactor.dy)
        xu2 = sqrt(mag2(s) - (dot(s,ur))**2/mag2(ur))
        ai = ar
        if 2*xu2/(dB+dp) <= 1:
            bi = acos(2*xu2/(dB+dp))
        print(ai)
        print(bi)

        reboundA = True
        reboundB = False


    elif distance(impactor,particle_B) <= (dB+dp)/2 and not reboundB:
        impactor.dx1, impactor.dy1 = rotate(impactor.dx, impactor.dy, ai)
        impactor.dn, impactor.dt = rotate(impactor.dx1, impactor.dy1, bi)

        impactor.dn *= -1

        br = -bi
        ar = br + bi - ai

        impactor.dx1, impactor.dy1 = rotate(impactor.dn, impactor.dt, br)
        impactor.dx, impactor.dy = rotate(impactor.dx1, impactor.dy1, -ai)

        spr = impact_location(dB,dp,xu,ai)
        sA = [-dA/2, 0]
        s = [spr[0]-sA[0],spr[1]-sA[1]]
        ur = (impactor.dx, impactor.dy)
        xu2 = sqrt(mag2(s) - (dot(s,ur))**2/mag2(ur))
        ai = ar
        if 2*xu2/(dA+dp) <= 1:
            bi = acos(2*xu2/(dA+dp))
        print(ai)
        print(bi)

        reboundB = True
        reboundA = False



    #update impactor position
    impactor.setx(impactor.xcor() + impactor.dx)
    impactor.sety(impactor.ycor() + impactor.dy)


wn.mainloop()
