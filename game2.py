import numpy as np
import matplotlib.pyplot as plt
import curses
import time
#A spaceshift flying around

number_particles = 5
x0 = 0.
y0 = 0.
xlim = 100
ylim = xlim
position_vector = np.zeros(2)
v0x = 0.
v0y = 0.
velocity_vector = np.zeros(2)
a0x = 0.
a0y = 0. 
acceleration_vector = np.array([a0x,a0y])
acceleration = 90.
dt = 0.01
direction = [0,np.pi/2,np.pi,3./2.*np.pi] #0 right, 1 up, 2 left, 3 bottom
def random_angle(direction):
    return np.random.choice(direction)

#times = 1000
i = 0
print("Starting the spaceship game!")
attack_position = []
def game_loop(stdscr, position_vector, velocity_vector, acceleration, attack_position, i):
    # Set up curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Make getch() non-blocking
    stdscr.clear()
    stdscr.addstr(0, 0, "Press 'q' to quit.")
    vel_attack = 100.
    attack_bool = False
    j = 0
    while True:
        key = stdscr.getch()
        plt.clf()
        plt.xlim(-xlim,xlim)
        plt.ylim(-ylim,ylim)
        plt.title('Position:' + '{:.0f}'.format(position_vector[0]) + ', ' +  '{:.0f}'.format(position_vector[1]) + ',' + 'Time:' + '{:.2f}'.format(i*dt))
        plt.scatter(position_vector[0],position_vector[1], s=50)
        plt.quiver(position_vector[0],position_vector[1],velocity_vector[0],velocity_vector[1], scale = 30)
        if attack_bool:
            for k in range(len(attack_position)):
                attack_position[k][0][0] += attack_position[k][1][0]*dt
                attack_position[k][0][1] += attack_position[k][1][1]*dt
                plt.scatter(attack_position[k][0][0],attack_position[k][0][1], s=30, color = 'black')
            attack_position[:] = [x for x in attack_position if abs(x[0][0]) < xlim and abs(x[0][1]) < ylim]    
        plt.pause(0.01)
        if key == ord("w"):
            stdscr.addstr(1, 0, "Move Up!    ")
            angle = np.pi/2
            position_vector += velocity_vector*dt + acceleration*np.array([np.cos(angle),np.sin(angle)])*dt**2/2.
            velocity_vector += acceleration*np.array([np.cos(angle),np.sin(angle)])*dt
        elif key == ord("a"):
            stdscr.addstr(1, 0, "Move Left!    ")
            angle = np.pi
            position_vector += velocity_vector*dt + acceleration*np.array([np.cos(angle),np.sin(angle)])*dt**2/2.
            velocity_vector += acceleration*np.array([np.cos(angle),np.sin(angle)])*dt
        elif key == ord("s"):
            stdscr.addstr(1, 0, "Move Down!    ")
            angle = 3./2.*np.pi
            position_vector += velocity_vector*dt + acceleration*np.array([np.cos(angle),np.sin(angle)])*dt**2/2.
            velocity_vector += acceleration*np.array([np.cos(angle),np.sin(angle)])*dt
        elif key == ord("d"):
            stdscr.addstr(1, 0, "Move Right!    ")
            angle = 0.
            position_vector += velocity_vector*dt + acceleration*np.array([np.cos(angle),np.sin(angle)])*dt**2/2.
            velocity_vector += acceleration*np.array([np.cos(angle),np.sin(angle)])*dt
        elif key == ord("z"):
            stdscr.addstr(1, 0, "STOP!    ")
            velocity_vector = np.array([0.,0.])
        elif key == ord("f"):
            stdscr.addstr(1, 0, "Attack!    ")
            if velocity_vector.sum() != 0:
                new_vector = (velocity_vector/(velocity_vector**2).sum()**0.5)*vel_attack
                attack_position.append([position_vector.copy(), new_vector])
                attack_bool = True      
        else:
            position_vector += velocity_vector*dt
        if key == ord("q"):
            print("Exiting game")
            break
        stdscr.refresh()
        i += 1
        #time.sleep(0.01)
 
# Run the game loop within curses wrapper
def start_game():
    curses.wrapper(game_loop, position_vector, velocity_vector, acceleration,attack_position, i )
start_game()