import turtle
from math import acos, sin, cos, pi

wn  = turtle.Screen()
wn.bgcolor("white")
wn.title("Impact simulation")


def rotate(x0,y0,angle):  
    x1 =  x0*cos(angle) + y0*sin(angle)
    y1 = -x0*sin(angle) + y0*cos(angle)
    return x1,y1


dp = 5
d1 = 6
ai1 = pi/4
vi_mag = 5
xu = -50.0
du = 20*(dp + d1)*0.5
bi1 = acos(xu/du)


impactor = turtle.Turtle()
impactor.shape("circle")
impactor.color("red")
impactor.shapesize(dp)
impactor.speed(0)
impactor.penup()
impactor.goto(-200*cos(ai1) + xu*sin(ai1),200*sin(ai1) + xu*cos(ai1))
impactor.dx =  vi_mag*cos(ai1)
impactor.dy = -vi_mag*sin(ai1)
impactor.pendown()


impactor.dx1, impactor.dy1 = rotate(impactor.dx, impactor.dy, ai1)
impactor.dn, impactor.dt = rotate(impactor.dx1, impactor.dy1, bi1)


particle_1 = turtle.Turtle()
particle_1.shape("circle")
particle_1.shapesize(d1)
particle_1.color("black")
particle_1.speed(0)
particle_1.penup()
particle_1.goto(0,0)


rebound1 = False
time = 0
while time < 150:
    time += 1
    #bounce
    if turtle.distance(impactor,particle_1) <= 20*(d1+dp)/2 and not rebound1:
        impactor.dn *= -1

        impactor.dx1, impactor.dy1 = rotate(impactor.dn, impactor.dt, -bi1)
        impactor.dx, impactor.dy = rotate(impactor.dx1, impactor.dy1, -ai1)

        rebound1 = True
    #update impactor position
    impactor.setx(impactor.xcor() + impactor.dx)
    impactor.sety(impactor.ycor() + impactor.dy)


wn.mainloop()