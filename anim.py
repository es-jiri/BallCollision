
import turtle
from math import acos, asin, ceil, sin, cos, pi, sqrt, exp, tan
from numpy.random import rand
from numpy import sign
from time import sleep


wn  = turtle.Screen()
wn.bgcolor("white")
wn.title("Impact simulation")


def rotate(x0,y0,angle):  
    x1 =  x0*cos(angle) + y0*sin(angle)
    y1 = -x0*sin(angle) + y0*cos(angle)
    return x1,y1

def rebound(ut,un):
    un *= -1
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


rads = [5, 25, 40, 60]
r_dep_masses = [1.0, 0.5, 0.3, 0.2]
tot_dep_mass = sum(r_dep_masses)
rel_dep_mass = [mass/tot_dep_mass for mass in r_dep_masses]
cum_prob = [rel_dep_mass[0]]
for i in range(1,len(rads)):
    cum_prob.append(cum_prob[i-1] + rel_dep_mass[i])


def random_radius():
    psi = rand()
    for i in range(1,len(rads)-1):
        if cum_prob[i] <= psi < cum_prob[i+1]:
            return rads[i]

    if psi < cum_prob[0]:
        return rads[0]

    return rads[-1]


while True:
    #animation parameters
    start_distance = 300
    exit_distance = 200

    #impactor properties
    ai = 45*pi/180
    vi_mag = 5
    rp = 10

    #deposit parameters
    rmax = 100
    max_space = 0


    #create deposited particles
    N = int(1/tan(ai)) + 1  # "A" will have index "N"

    ri = [] # radii
    for i in range(N+2):
        ri.append(random_radius())

    xi = []
    for j in range(N+2):
        xi.append(0)

    xi[-2] = 0
    xi[-1] = xi[N] + (ri[N]+ri[-1]+max_space*rand())
    for i in range(N-1,-1,-1):
        xi[i] = xi[i+1] - (ri[i+1]+ri[i]+max_space*rand())

    ru = ri[N] + rp
    xu = ri[N]*(0.5-rand())*2*sin(ai) #the p's initial trajectory crosses the "A" mid plane


    impactor_scale = 1
    draw_deposit = True
    clear_previous = True

    impactor = turtle.Turtle()
    impactor.shape("circle")
    impactor.color("red")
    impactor.shapesize(rp/10*impactor_scale)
    impactor.speed(0)
    impactor.penup()
    impactor.goto(-start_distance*cos(ai) + xu*sin(ai),start_distance*sin(ai) + xu*cos(ai))
    impactor.dx =  vi_mag*cos(ai)
    impactor.dy = -vi_mag*sin(ai)
    impactor.pendown()


    if draw_deposit:
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


    ru = ri[N] + rp

    x_imp = impactor.xcor()
    y_imp = impactor.ycor()


    xu0 = xu
    ru0 = ru
    next_p = N
    bi = acos(xu/ru)
    dl_min = 0
    for i in range(N+2):
        #increment particle indices in the direction of the "p" movement until a collision occurs
        #calculate closest approach of "p" to the j-th particle
        if i==N:
            continue
        rui = rp + ri[i]
        xui = (xi[N] - xi[i])*sin(ai) + xu0
        if(abs(xui)<rui):
            dl_i = sqrt(ru0**2-xu0**2) - sqrt(rui **2-xui**2) - cos(ai)*(xi[N] - xi[i])
            if(dl_i<dl_min):
                dl_min = dl_i
                xu = xui
                ru = rui
                bi = acos(xui/rui) #rebound angle, if p hits the A first
                next_p = i

    time = 0
    hitted_id = -1
    ar = 0

    max_hits = 10
    hits = 0

    while hits < max_hits:
        hitted_id = next_p
        
        hits += 1
        if(-1 < next_p < N+2):
            impactor, ar = update_xy_velocity(impactor,ai,bi)
            if impactor.dx**2+impactor.dy**2 == 0 :
                break
            #calculate coordinates of the center of "p" in the moment of collision
            x_imp = -(ri[hitted_id]+rp)*sin(bi-ai) + xi[hitted_id]
            y_imp = (ri[hitted_id]+rp)*cos(bi-ai)
            impactor.goto((x_imp,y_imp))
            #update the particle impaction angle
            ai = -ar
            #adjust the particle index according to the direction of particle movement
            next_p = hitted_id + int(sign(impactor.dx))

            #if "p" collided with the last particle and still descends, 
            #the last particle has to be moved to a new location to prevent further descent of "p"
            if(hitted_id==N+1 and impactor.dy<0 and impactor.dx>0):
                #shift the last particle's position and alter its diameter
                xC0 = xi[-1]
                rC0 = ri[-1]
                ri[-1] = rmax*rand() #choose new particle's radius
                xi[-1] = xC0+(ri[-1]+rC0+max_space*rand()) #determine shift in the x direction
                if draw_deposit:
                    dep_particles[-1].goto(xi[-1],0) #shift the patricle
                    dep_particles[-1].shapesize(ri[-1]/10) #update its radius     

                hitted_id = N
                next_p = N+1

            elif(hitted_id==0 and impactor.dy<0 and impactor.dx<0):
                #shift the last particle's position and alter its diameter
                x0 = xi[0]
                r0 = ri[0]
                ri[0] = rmax*rand() #choose new particle's radius
                xi[0] = x0+(ri[0]+r0+max_space*rand()) #determine shift in the x direction
                if draw_deposit:
                    dep_particles[0].goto(xi[0],0) #shift the patricle
                    dep_particles[0].shapesize(ri[0]/10) #update its radius     

                hitted_id = 1
                next_p = 0

            fate_updates = 0
            max_fate_updates = 50
            #increment particle indices in the direction of the "p" movement until a collision occurs
            while -1<next_p<N+2 and fate_updates<max_fate_updates:
                fate_updates += 1
                #calculate closest approach of "p" to the j-th particle
                xu = y_imp*cos(ai) + (x_imp-xi[next_p])*sin(ai)
                ru = ri[next_p]+rp                
                if(abs(xu) < ru and impactor.dx*(x_imp-xi[next_p])+impactor.dy*y_imp < 0): #"p" hits the jth particle
                    bi = acos(xu/ru)
                    break #collision with jth particle will occur, break the loop

                elif next_p==N+1 and impactor.dy<0 and impactor.dx>0: #particle missed the last particle, but still descends to the surface
                    #shift the last particle's position and alter its diameter
                    xC0 = xi[-1]
                    rC0 = ri[-1]
                    ri[-1] = rmax*rand() #choose new particle's radius
                    xi[-1] = xC0+(ri[-1]+rC0+max_space*rand()) #determine shift in the x direction
                    if draw_deposit:
                        dep_particles[-1].goto(xi[-1],0) #shift the patricle
                        dep_particles[-1].shapesize(ri[-1]/10) #update its radius   

                elif next_p==0 and impactor.dy<0 and impactor.dx<0: #particle missed the last particle, but still descends to the surface
                    #shift the last particle's position and alter its diameter
                    x0 = xi[0]
                    r0 = ri[0]
                    ri[0] = rmax*rand() #choose new particle's radius
                    xi[0] = x0-(ri[0]+r0+max_space*rand()) #determine shift in the x direction
                    if draw_deposit:
                        dep_particles[0].goto(xi[0],0) #shift the patricle
                        dep_particles[0].shapesize(ri[0]/10) #update its radius   
                     
                    hitted_id = 1  
                
                else:  #"p" missed the jth particle, go to the next
                    next_p += int(sign(impactor.dx))

        else:
            if(impactor.dx**2+impactor.dy**2 > 0):
                x_imp = x_imp + exit_distance*cos(ar)
                y_imp = y_imp + exit_distance*sin(ar)
            impactor.color(sqrt(impactor.dx**2+impactor.dy**2)/vi_mag, 0, 0)
            impactor.goto((x_imp,y_imp))
            break

    input()
    if clear_previous:
        wn.clear()


wn.mainloop()

