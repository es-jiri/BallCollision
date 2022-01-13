
import turtle
from math import acos, asin, sin, cos, pi, sqrt, exp
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

Cm = 3.5
a = 0.3
multibody_coeff = Cm/(1+Cm)
def rebound(ut,un):
    en = (1-exp(-abs(un))) * exp(-a*abs(un)) * (1+a)
    un = max(un - (1+en) * multibody_coeff * un, 0.0)
    if(un>0):
        ut = ut - 2.0/7*multibody_coeff * ut # no-slip collision
    else:
        ut = 0
    print('en =', en, 'un =', un)
    return ut,un

def update_xy_velocity(impactor,ai,bi):
    epsilon = bi - ai
    impactor.dt, impactor.dn = rotate(impactor.dx, impactor.dy, epsilon)
    impactor.dt, impactor.dn = rebound(impactor.dt, impactor.dn)
    vmag = sqrt(impactor.dt**2 + impactor.dn**2)
    if(vmag>0):
        br = acos(impactor.dt/vmag)
    else:
        br = bi
    ar = br + bi - ai
    impactor.dx, impactor.dy = rotate(impactor.dt, impactor.dn, -epsilon)
    return impactor, ar


ai = pi/8
vi_mag = 5

rp = 10
rmax = 100
max_space = 0

#create deposited particles
N = 4 # "A" will have index "N"

ri = [] # radii
for i in range(N+2):
    ri.append(rmax*rand())
rA = ri[-2]
rC = ri[-1]

xA = 0
xC = xA + (rA+rC+max_space*rand())
xi = []
for j in range(N+2):
    xi.append(0)
xi[-2] = xA
xi[-1] = xC
for i in range(N-1,-1,-1):
    xi[i] = xi[i+1] - (ri[i+1]+ri[i]+max_space*rand())


ru = rA + rp
xu = rA*(0.5-rand())*2*sin(ai) #the p's initial trajectory crosses the "A" mid plane


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


dep_particles = []
for i in range(N+2):
    dep_particles.append(turtle.Turtle())
    dep_particles[i].shape("circle")
    dep_particles[i].shapesize(ri[i]/10)
    dep_particles[i].color("black")
    dep_particles[i].speed(0)
    dep_particles[i].penup()
    dep_particles[i].goto(xi[i],0)

dep_particles[N].color("green")


ru = rA + rp

x_imp = 0.0
y_imp = 0.0


xu0 = xu
ru0 = ru
will_be_hitted_id = N
bi = acos(xu/ru)
dl_min = 0
for i in range(N+2):
    #increment particle indices in the direction of the "p" movement until a collision occurs
    #calculate closest approach of "p" to the j-th particle
    if i==N:
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
hitted_id = -1
collision = False
ar = 0

while time < 120:
    time += 1
    #bounce
    for i in range(N+2):
        if turtle_distance(impactor,dep_particles[i]) <= (ri[i]+rp) and hitted_id != i:
            collision = True
            impactor, ar = update_xy_velocity(impactor,ai,bi)
            hitted_id = will_be_hitted_id

    if impactor.ycor()<=0 and impactor.dy<0:
        impactor, ar = update_xy_velocity(impactor,ai,ai)
        hitted_id = -1


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

        #if "p" collided with the last particle and still descends, 
        #the last particle has to be moved to a new location to prevent further descent of "p"
        if(hitted_id==N+1 and impactor.dy<0 and impactor.dx>0):
            #shift the last particle's position and alter its diameter
            xC0 = xi[-1]
            rC0 = ri[-1]
            ri[-1] = rmax*rand() #choose new particle's radius
            xi[-1] = xC0+(ri[-1]+rC0) #determine shift in the x direction
            dep_particles[-1].goto(xi[-1],0) #shift the patricle
            dep_particles[-1].shapesize(ri[-1]/10) #update its radius     
            hitted_id = N
            will_be_hitted_id = N+1
            j = N+1  

        fate_updates = 0
        max_fate_updates = 3
        #increment particle indices in the direction of the "p" movement until a collision occurs
        while -1<j<N+2 and fate_updates<max_fate_updates:
            fate_updates += 1
            #calculate closest approach of "p" to the j-th particle
            xu = y_imp*cos(ai) + (x_imp-xi[j])*sin(ai)
            ru = ri[j]+rp
            if(abs(xu) < ru): #"p" hits the jth particle
                bi = acos(xu/ru)
                break #collision with jth particle will occur, break the loop

            elif j==N+1 and impactor.dy<0 and impactor.dx>0: #particle missed the last particle, but still descends to the surface
                #shift the last particle's position and alter its diameter
                xC0 = xi[-1]
                rC0 = ri[-1]
                ri[-1] = rmax*rand() #choose new particle's radius
                xi[-1] = xC0+(ri[-1]+rC0) #determine shift in the x direction
                dep_particles[-1].goto(xi[-1],0) #shift the patricle
                dep_particles[-1].shapesize(ri[-1]/10) #update its radius     
                hitted_id = N  
            
            else:  #"p" missed the jth particle, go to the next
                j += int(sign(impactor.dx))
 
            will_be_hitted_id = j
                
        #"p" leaves the particle's surface, collision ends  
        collision = False


    #update impactor position
    impactor.setx(impactor.xcor() + impactor.dx)
    impactor.sety(impactor.ycor() + impactor.dy)


wn.mainloop()
