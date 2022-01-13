from abc import abstractstaticmethod
import turtle
from math import acos, asin, sin, cos, pi, sqrt
from numpy.core.fromnumeric import amin
from numpy.random import rand
from numpy import sign


from numpy.random import rand

wn  = turtle.Screen()
wn.bgcolor("white")
wn.title("Impact simulation")


def rotate(x0,y0,angle):  
    x1 =  x0*cos(angle) + y0*sin(angle)
    y1 = -x0*sin(angle) + y0*cos(angle)

    return x1,y1


def distance(ax, ay, bx, by):
    return sqrt((ax-bx)**2 + (ay-by)**2)


def turtle_distance(turtle1, turtle2):
    r1 = [turtle1.xcor(),turtle1.ycor()]
    r2 = [turtle2.xcor(),turtle2.ycor()]
    return sqrt((r1[0]-r2[0])**2 + (r1[1]-r2[1])**2)


def rebound(ut,un):
    un *= -1
    return ut,un

def update_xy_velocity(impactor,ai,bi):
    epsilon = bi - ai
    impactor.dt, impactor.dn = rotate(impactor.dx, impactor.dy, epsilon)
    impactor.dt, impactor.dn = rebound(impactor.dt, impactor.dn)
    vmag = sqrt(impactor.dt**2 + impactor.dn**2)
    br = acos(impactor.dt/vmag)
    ar = br + bi - ai
    impactor.dx, impactor.dy = rotate(impactor.dt, impactor.dn, -epsilon)
    return impactor, ar

ai = pi/4
vi_mag = 5

rp = 10
rmax = 100


rA = rmax*rand()
rB = rmax*rand()
rC = rmax*rand()
rD = rmax*rand()
ru = rA + rp
xu = rA*(0.5-rand())*2*sin(ai) #the p's initial trajectory crosses the "A" mid plane

xA = 0
xB = -(rA+rB)
xC = rA+rC
xD = -(rA+2*rB+rD)

ri = [rD, rB, rA, rC]
xi = [xD, xB, xA, xC]



impactor = turtle.Turtle()
impactor.shape("circle")
impactor.color("red")
impactor.shapesize(rp/10)
impactor.speed(0)
impactor.penup()
impactor.goto(-300*cos(ai) + xu*sin(ai),300*sin(ai) + xu*cos(ai))
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


particle_C = turtle.Turtle()
particle_C.shape("circle")
particle_C.shapesize(rC/10)
particle_C.color("black")
particle_C.speed(0)
particle_C.penup()
particle_C.goto(xC,0)

particle_D = turtle.Turtle()
particle_D.shape("circle")
particle_D.shapesize(rD/10)
particle_D.color("black")
particle_D.speed(0)
particle_D.penup()
particle_D.goto(xD,0)


ru = rA + rp

x_imp = 0.0
y_imp = 0.0


xu0 = xu
ru0 = ru
bi = acos(xu/ru)
dl_min = 0
for i in range(4):
    #increment particle indices in the direction of the "p" movement until a collision occurs
    #calculate closest approach of "p" to the j-th particle
    if i==2:
        continue
    rui = rp + ri[i]
    xui = (xA - xi[i])*sin(ai) + xu0
    if(abs(xui)<rui):
        dl_i = sqrt(ru0**2-xu0**2) - sqrt(rui **2-xui**2) - cos(ai)*(xA - xi[i])
        if(dl_i<dl_min):
            dl_min = dl_i
            xu = xui
            ru = rui
            bi = acos(xui/rui) #rebound angle, if p hits the A first
            will_be_hitted_id = i


time = 0
hitted_id = -2
collision = False
ar = 0

while time < 120:
    time += 1
    #bounce
    if turtle_distance(impactor,particle_A) <= (rA+rp) and hitted_id != 2:
        collision = True
        impactor, ar = update_xy_velocity(impactor,ai,bi)
        hitted_id = 2

    elif turtle_distance(impactor,particle_B) <= (rB+rp) and hitted_id != 1:
        collision = True
        impactor, ar = update_xy_velocity(impactor,ai,bi)
        hitted_id = 1
    
    elif turtle_distance(impactor,particle_C) <= (rC+rp) and hitted_id != 3:
        collision = True
        impactor, ar = update_xy_velocity(impactor,ai,bi)
        hitted_id = 3
    
    elif turtle_distance(impactor,particle_D) <= (rD+rp) and hitted_id != 0:
        collision = True
        impactor, ar = update_xy_velocity(impactor,ai,bi)
        hitted_id = 0


    #update bi
    if collision:
        #calculate coordinates of the center of "p" in the moment of collision
        x_imp = -(ri[hitted_id]+rp)*sin(bi-ai) + xi[hitted_id]
        y_imp = (ri[hitted_id]+rp)*cos(bi-ai)
        #update the particle impaction angle
        ai = -ar
        #adjust the particle index according to the direction of particle movement
        will_be_hitted_id = hitted_id + int(sign(impactor.dx))
        j = will_be_hitted_id
        
        #increment particle indices in the direction of the "p" movement until a collision occurs
        while -1<j<4:
            #calculate closest approach of "p" to the j-th particle
            xu = y_imp*cos(ai) + (x_imp-xi[j])*sin(ai)
            ru = ri[j]+rp
            if(abs(xu) < ru): #"p" hits the jth particle
                bi = acos(xu/ru)
                break #collision with jth particle will occur, break the loop

            if j==3 and impactor.dy<0 and impactor.dx>0: #particle missed the last particle, but still descends to the surface
                #shift the last particle's position and alter its diameter
                xC0 = xC
                rC0 = rC
                rC = rmax*rand() #choose new particle's radius
                xC = xC0+(rC+rC0) #determine shift in the x direction
                particle_C.goto(xC,0) #shift the patricle
                particle_C.shapesize(rC/10) #update its radius     
                xi[3] = xC
                ri[3] = rC  

            elif j==0 and impactor.dy<0 and impactor.dx<0: #particle missed the first particle, but still descends to the surface
                xD0 = xD
                rD0 = rD
                rD = rmax*rand() #choose new particle's radius
                xD = xD0-(rD+rD0) #determine shift in the x direction
                particle_D.goto(xD,0) #shift the patricle
                particle_D.shapesize(rD/10) #update its radius     
                xi[0] = xD
                ri[0] = rD      
            
            else:  #"p" missed the jth particle, go to the next
                j += int(sign(impactor.dx))
                
                
            will_be_hitted_id = j
                
        #"p" leaves the particle's surface, collision ends  
        collision = False


    #update impactor position
    impactor.setx(impactor.xcor() + impactor.dx)
    impactor.sety(impactor.ycor() + impactor.dy)


wn.mainloop()
