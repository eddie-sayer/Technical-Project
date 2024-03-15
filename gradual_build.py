import pygame
import sys
import math
import random
import csv
import pandas as pd

"""
This simulation is scaled to 1 pixel = 0.025 meters. Each agent has a diameter of 0.5 meters (20 pixels).

The simulation will be tested with many participants and responses recorded, subject to two different types of treatment.
The first treatement is homogeneous vs heterogeneous agent movement . In the heterogeneous treatment, agents will have different
parameters for their movement, such as their desired speed, relaxation time, and noise. In the homogeneous treatment, all agents
will have the same parameters for their movement.
The second treatment will be a symmetric vs asymmetric split of the room. In the symmetric treatment, agents will divide evenly between
two routes, with the same number of agents on each route. In the asymmetric treatment, there will be a different number of agents on each route.

This gives rise to four treatment combinations:

1. Control: Homogeneous and symmetric (C)
2. Heterogeneous: Heterogeneous and symmetric (H)
3. Asymmetric: Homogeneous and asymmetric (A)
4. Combination: Heterogeneous and asymmetric (HA)

The terms varied to represent heterogeneity in the population are the noise term, the relaxation time, the desired speed and the mass.
All other terms are kept constant across all agents.
- The ub noise term is a random value between 0.5 and 5000, and the lb noise term is a random value between -0.5 and -5000.
- The relaxation time is a random value between 0.4 and 0.7.
- The desired speed is a Guassian distribution with mean 1.34 m/s and standard deviation 0.26 m/s. Actual speed is capped at 1.3 x v_0.
  The result is then scaled to the simulation by multiplying by 1000.
- The mass of the agent is a random value between 0.8 and 1.2.
"""

## Add general information at the start of the simulation (what kind of data, indicating consent, fully anonymous, etc.)
# Could email around, set the treatment before email. Tell them I'm gonna delete the email, preserve anonymity.
## Create a separate document, offer to give to people who play on your laptop. Email PDF.
## Informed consent, the right to withdraw from the research. Just be clear to people on this. 
## Prescribe paratemter values specifically.
## The time the player spends away from the doors before they decide to exit.
## Just have the stats write to a file
## Record all agent and player paths.
# Send a report draft during Easter.


SELECTED_TREATMENT = "HA"
# Constants
WIDTH, HEIGHT = 900, 750
SPAWN_BOX_COORDS = (200,160,750,590) # (x1, y1, x2, y2)
BACKGROUND_COLOR = (255, 255, 205)
CHARACTER_COLOR = (0, 0, 0)
AGENT_COLOR = (255, 0, 0)
CROSS_COLOR = (255, 0, 0)
CHARACTER_RADIUS = 6 #10 is the desired atm
VELOCITY = 1.1 #1.34   # Desired speed of the player
FPS = 60  # Frames per second
TIMESTEP = 1 / FPS  # Timestep for the simulation
NUMBER_OF_AGENTS = 80 # Number of agents in the simulation
X_CLOSEST_AGENTS = 5  # Number of closest agents to consider for the social force calculation
#TARGET_CHANGE_RADIUS = 3 * CHARACTER_RADIUS  # Radius within which the agent changes target

# Targets
ROUTE_A_TARGET_1 = (790, 200, 20) # (x, y, TARGET CHANGE RADIUS) #(780, 200, 20)
ROUTE_A_TARGET_2 = (790, 80, 3 * CHARACTER_RADIUS) # (780, 80, 3 * CHARACTER_RADIUS)
ROUTE_A_TARGET_3 = (205, 80, 15) # (220, 80, 3 * CHARACTER_RADIUS)
ROUTE_A_TARGET_4 = (130, 80, 3 * CHARACTER_RADIUS)
ROUTE_A_TARGET_5 = (60, 375, 3 * CHARACTER_RADIUS)
ROUTE_A_TARGET_6 = (10, 375, 3 * CHARACTER_RADIUS)

ROUTE_A = [ROUTE_A_TARGET_1, ROUTE_A_TARGET_2, ROUTE_A_TARGET_3, ROUTE_A_TARGET_4, ROUTE_A_TARGET_5, ROUTE_A_TARGET_6]

ROUTE_B_TARGET_1 = (790, 550, 20) # (780, 550, 20)
ROUTE_B_TARGET_2 = (790, 670, 3 * CHARACTER_RADIUS) # (780, 670, 3 * CHARACTER_RADIUS)
ROUTE_B_TARGET_3 = (205, 670, 15) # (220, 670, 3 * CHARACTER_RADIUS)
ROUTE_B_TARGET_4 = (130, 670, 3 * CHARACTER_RADIUS)
ROUTE_B_TARGET_5 = (60, 375, 3 * CHARACTER_RADIUS)
ROUTE_B_TARGET_6 = (10, 375, 3 * CHARACTER_RADIUS)

ROUTE_B = [ROUTE_B_TARGET_1, ROUTE_B_TARGET_2, ROUTE_B_TARGET_3, ROUTE_B_TARGET_4, ROUTE_B_TARGET_5, ROUTE_B_TARGET_6]

# Initialize Pygame
pygame.init()
game_start = pygame.time.get_ticks()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

"""
In the original Helbing model, he defines the following constants used in his computer simulations:

v_0: Desired speed = Guassian distribution with mean 1.34 m/s and standard deviation 0.26 m/s. Actual speed is capped at 1.3 x v_0.
T_alpha: Relaxation time = 0.5 s
N_lb: Noise lower bound = No noise defined in the original simulation
N_ub: Noise upper bound = No noise defined in the original simulation
m: Mass of the agent = No mass defined in the original simulation

R_s: Radius of the social force = No social force radius defined in the original simulation
R_b: Radius of the boundary force = No boundary force radius defined in the original simulation #Choose sensible values

A_p: Physical interaction strength = 2000 N #
A_s: Social interaction strength = 2000 N #
B_p: Physical interaction range = 0.08 m #
B_s: Social interaction range = 0.08 m #

A_b: Boundary interaction strength = 10 m/s^2
B_b: Boundary interaction range = 0.1 m

"""
"""
Decent set of values:

R_s = 2 / 0.025  # Radius of the social force
R_b = 0.3 / 0.025  # Radius of the boundary force
A_p = 500 / 0.025  # Social Physical interaction strength
A_s = 200 / 0.025 # Social interaction strength
B_p = 0.2 / 0.025  # Social Physical interaction range
B_s = 1 / 0.025  # Social interaction range
A_b = 200 / 0.025 # Boundary interaction strength
B_b = 0.3 / 0.025  # Boundary interaction range
v_0 = 1.34 / 0.025 * 100  # Desired speed
T_alpha = 0.5  # Relaxation time
N_lb = -0.5  # Noise lower bound
N_ub = 0.5  # Noise upper bound
m = 70 * 0.025  # Mass of the agent
"""

# Constants for the social force calculation
# Directly from the Helbing paper:


# Functions
def lerp(start, end, t):  # Linear interpolation function
    return start + t * (end - start)


# Player class
class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def move_towards(self, target_x, target_y, rectangles_corners, agent_coords):
        distance = math.hypot(target_x - self.x, target_y - self.y)
        
        if distance > 1:
            t = VELOCITY / distance
            new_x = lerp(self.x, target_x, t)
            new_y = lerp(self.y, target_y, t)

            collision_detected = False

            # Check if the new position is inside any of the rectangles
            for rect in rectangles_corners:
                rect_x1, rect_y1, rect_x2, rect_y2 = rect
                closest_x = max(rect_x1, min(new_x, rect_x2))
                closest_y = max(rect_y1, min(new_y, rect_y2))

                distance_to_closest = math.hypot(new_x - closest_x, new_y - closest_y)

                if distance_to_closest < self.radius:
                    collision_detected = True
                    break # Do not update position if it would intersect with a rectangle
            
            if main_simulation:
                # Check if the new position is inside any of the agents
                for agent in agent_coords:
                    distance_to_closest = math.hypot(new_x - agent[0], new_y - agent[1])
                    if distance_to_closest < 2*CHARACTER_RADIUS:
                        collision_detected = True
                        break  # Do not update position if it would intersect with an agent


            # Update the player's position
            if not collision_detected:
            
                self.x = new_x
                self.y = new_y


# Agent class
#agent_count = 0
class Agent:
    def __init__(self, x, y, radius, index):
        self.x = x
        self.y = y
        self.radius = radius
        self.index = index
        self.current_target = 0
        self.route = []

    def calculate_social_force(self, agent_coords, constants, x_closest_agents=X_CLOSEST_AGENTS):

        # Unpack the constants
        R_s = constants[0]
        #R_b = constants[1]
        A_p = constants[2]
        A_s = constants[3]
        B_p = constants[4]
        B_s = constants[5]
        #A_b = constants[6]
        #B_b = constants[7]
        #v_0 = constants[8]
        #T_alpha = constants[9]
        #N_lb = constants[10]
        #N_ub = constants[11]
        #m = constants[12]

        FS = [0, 0]  # Initialize the social force vector

        P_alpha = (self.x, self.y)

        if player_present:
            agent_coords.append((player.x, player.y))

        # Sort agents based on distance
        sorted_agents = sorted(agent_coords, key=lambda agent: math.hypot(agent[0] - P_alpha[0], agent[1] - P_alpha[1]))

        for agent in sorted_agents[:x_closest_agents]:
            if agent == P_alpha:
                continue  # Skip the current agent
            # Check if the agent is within the social force radius
            P_beta = (agent[0], agent[1])
            distance = math.hypot(P_beta[0] - P_alpha[0], P_beta[1] - P_alpha[1])  # Distance between the two agents
            if distance > R_s:
                continue  # Skip the current agent
            else:
                direction_unit_vector = [
                    (P_beta[0] - P_alpha[0]) / distance,
                    (P_beta[1] - P_alpha[1]) / distance,
                ]  # Direction vector from the current agent to the other agent
                FS[0] -= A_p * direction_unit_vector[0] * math.exp(-distance / B_p) + A_s * direction_unit_vector[0] * math.exp(-distance / B_s)
                FS[1] -= A_p * direction_unit_vector[1] * math.exp(-distance / B_p) + A_s * direction_unit_vector[1] * math.exp(-distance / B_s)

        if player_present:
            agent_coords.pop() # Remove the player from the list of agents

        return FS

    def calculate_boundary_force(self, rectangles_corners, constants): #careful with small doorways

        # Unpack the constants
        #R_s = constants[0]
        R_b = constants[1]
        #A_p = constants[2]
        #A_s = constants[3]
        #B_p = constants[4]
        #B_s = constants[5]
        A_b = constants[6]
        B_b = constants[7]
        #v_0 = constants[8]
        #T_alpha = constants[9]
        #N_lb = constants[10]
        #N_ub = constants[11]
        #m = constants[12]

        P_alpha = (self.x, self.y)
        FB = [0, 0]
        for rect in rectangles_corners:
            rect_x1, rect_y1, rect_x2, rect_y2 = rect
            closest_x = max(rect_x1, min(self.x, rect_x2))  # Closest x coordinate to the agent
            closest_y = max(rect_y1, min(self.y, rect_y2))  # Closest y coordinate to the agent

            distance_to_closest = math.hypot(self.x - closest_x, self.y - closest_y)

            if distance_to_closest > R_b:
                continue  # Skip the current rectangle
            else:
                direction_unit_vector = [
                    (closest_x - P_alpha[0]) / distance_to_closest,
                    (closest_y - P_alpha[1]) / distance_to_closest,
                ]
                FB[0] -= A_b * direction_unit_vector[0] * math.exp(-distance_to_closest / B_b)
                FB[1] -= A_b * direction_unit_vector[1] * math.exp(-distance_to_closest / B_b)

        return FB

    def move_towards(self, velocity_x, velocity_y, rectangles_corners, agent_coords, constants):
        """
        Move the agent towards the target position while avoiding obstacles and other agents, with a noise term.
        ----------
        Parameters
        ----------
        target_x: x coordinate of the target position
        target_y: y coordinate of the target position
        velocity_x: x component of the agent's velocity
        velocity_y: y component of the agent's velocity
        rectangles_corners: list of coordinates of the top left and bottom right corners of the rectangles
        agent_coords: list of coordinates of the agents within the social force radius
        constants: list of constants for the social force calculation. [R_s, R_b, A_p, A_s, B_p, B_s, A_b, B_b]:
        {R_s: radius of the social force
        R_b: radius of the boundary force
        A_p: Physical interaction strength
        A_s: Social interaction strength
        B_p: Physical interaction range
        B_s: Social interaction range
        A_b: Boundary interaction strength
        B_b: Boundary interaction range
        v_0: Desired speed
        T_alpha: Relaxation time
        N_lb: Noise lower bound
        N_ub: Noise upper bound
        m: Mass of the agent}
        ----------
        """
        # Unpack the constants
        #R_s = self.constants[0]
        #R_b = self.constants[1]
        #A_p = self.constants[2]
        #A_s = self.constants[3]
        #B_p = self.constants[4]
        #B_s = self.constants[5]
        #A_b = self.constants[6]
        #B_b = self.constants[7]
        v_0 = constants[8]
        T_alpha = constants[9]
        N_lb = constants[10]
        N_ub = constants[11]
        m = constants[12]


        # Calculate the social force
        FS = self.calculate_social_force(agent_coords, constants)

        # Calculate the boundary force
        FB = self.calculate_boundary_force(rectangles, constants)

        agent_target_x, agent_target_y, TARGET_CHANGE_RADIUS = self.route[self.current_target]

        # Calculate the target force
        distance_to_target = math.hypot(agent_target_x - self.x, agent_target_y - self.y)
        direction_unit_vector = [
            (agent_target_x - self.x) / distance_to_target,
            (agent_target_y - self.y) / distance_to_target,
        ]
        FT = [
            (1 / T_alpha) * (v_0 * direction_unit_vector[0] - velocity_x),
            (1 / T_alpha) * (v_0 * direction_unit_vector[1] - velocity_y),
        ]

        # Calculate the noise force
        FN = [random.uniform(N_lb, N_ub), random.uniform(N_lb, N_ub)]

        # Calculate the total force
        F = [
            FS[0] + FB[0] + FT[0] + FN[0],
            FS[1] + FB[1] + FT[1] + FN[1],
        ] 

        #Update the agent's position
        velocity_x_new = F[0]/m * TIMESTEP
        velocity_y_new = F[1]/m * TIMESTEP

        new_x = self.x + velocity_x_new * TIMESTEP
        new_y = self.y + velocity_y_new * TIMESTEP

        collision_detected = False

        # Check if the new position is inside any of the rectangles
        for rect in rectangles_corners:
            rect_x1, rect_y1, rect_x2, rect_y2 = rect
            closest_x = max(rect_x1, min(new_x, rect_x2))
            closest_y = max(rect_y1, min(new_y, rect_y2))

            distance_to_closest = math.hypot(new_x - closest_x, new_y - closest_y)

            if distance_to_closest < self.radius:
                collision_detected = True
                break  # Do not update position if it would intersect with a rectangle
        
        if player_present:
            agent_coords.append((player.x, player.y))
        # Check if the new position is inside any of the agents or the player
        for agent in agent_coords:
            if agent == (self.x, self.y):
                continue
            distance_to_closest = math.hypot(new_x - agent[0], new_y - agent[1])
            if distance_to_closest < 2 * CHARACTER_RADIUS:
                collision_detected = True
                break  # Do not update position if it would intersect with an agent or the player
        
        if player_present:
            agent_coords.pop()

        # Update the agent's position
        if not collision_detected:
            self.x = new_x
            self.y = new_y
            velocity_x = velocity_x_new
            velocity_y = velocity_y_new

        velocity_magnitude = math.hypot(velocity_x, velocity_y) # Caps actual speed at 1.3 * v_0
        if velocity_magnitude > 1.05 * v_0:
            velocity_x = (1.05 * v_0 / velocity_magnitude) * velocity_x
            velocity_y = (1.05 * v_0 / velocity_magnitude) * velocity_y

        if distance_to_target < TARGET_CHANGE_RADIUS: # 2 * CHARACTER_RADIUS is the original value
            self.current_target += 1
            agent_target_x, agent_target_y = self.route[self.current_target][0], self.route[self.current_target][1]

        return self.x, self.y, velocity_x, velocity_y, agent_target_x, agent_target_y # Return the new position and velocity of the agent


# Function to generate agent positions
def generate_agent_positions(num_agents, spawn_box, avoid_positions, min_distance):

    agent_positions = []

    for i in range(num_agents):
        while True:
            x = random.uniform(spawn_box[0] + 2 * CHARACTER_RADIUS, spawn_box[2] - 2 * CHARACTER_RADIUS)
            y = random.uniform(spawn_box[1] + 2 * CHARACTER_RADIUS, spawn_box[3] - 2 * CHARACTER_RADIUS)

            # Check if the agent is too close / overlapping with any other agents
            too_close = False
            for position in avoid_positions:
                distance = math.hypot(x - position[0], y - position[1])
                if distance < min_distance:
                    too_close = True
                    break

            if not too_close:
                agent_positions.append((x, y))
                avoid_positions.append((x, y)) # Add the new position to the list of positions to avoid
                break

    return agent_positions

# Function to determine the route split

def route_split(agents, agent_coords, route_a_percentage):

    sorted_agents = sorted(agents, key=lambda agent: agent_coords[agents.index(agent)][1])

    num_agents = int(len(sorted_agents) * route_a_percentage / 100)

    agents_route_a = sorted_agents[:num_agents]
    agents_route_b = sorted_agents[num_agents:]

    # Assign routes to agents
    for agent in agents_route_a:
        agent.route = ROUTE_A.copy()

    for agent in agents_route_b:
        agent.route = ROUTE_B.copy()

    agent_targets = [agent.route[0] for agent in agents]

    return agent_targets

# Function to generate agent constants
def generate_agent_constants(agents, homohetero):
    
    agent_constants = []
    
    if homohetero == "homo":
        
        for agent in agents:

            v_0 = 1.34 * 1000 # Desired speed
            T_alpha = 0.55 #0.5 # Relaxation time
            A_b = 10 * 500  #50 Boundary interaction strength 
            B_b = 0.1 * 150 #5 #0.1 * 150 # Boundary interaction range
            A_s = 2.3 * 1000 #2.3 * 500 # * 1000 # Social interaction strength
            B_s = 0.3 * 150 #0.1 * 150 # 0.3 * 150 # Social interaction range
            N_lb = -1000 #-500 #-0.5 # Noise lb
            N_ub = 1000 #500 #0.5 Noise ub
            m = 1 # Mass of the agent
            R_s = 100 # Radius of the social force
            R_b = 70 # Radius of the boundary force 
            A_p = 4000 # Social physical interaction strength 
            B_p = 0.1 * 150 # Social physical interaction range 
            constants = [R_s, R_b, A_p, A_s, B_p, B_s, A_b, B_b, v_0, T_alpha, N_lb, N_ub, m]

            agent_constants.append(constants)

    elif homohetero == "hetero":
        
        third = int(NUMBER_OF_AGENTS / 3)
        for agent in agents[0:third]:
            
            #Young

            v_0 = 1 * 1000 # Desired speed
            T_alpha = 0.4 # Relaxation time
            A_b = 10 * 500 # Boundary interaction strength
            B_b = 0.1 * 150 # Boundary interaction range    
            A_s = 2.3 * 1000 # Social interaction strength
            B_s = 0.3 * 150 # Social interaction range
            N_lb = -3000 # Noise lower bound
            N_ub = 3000 # Noise upper bound
            m = 1   # Mass of the agent
            R_s = 100 # Radius of the social force
            R_b = 70 # Radius of the boundary force
            A_p = 4000 # Physical interaction strength
            B_p = 0.1 * 150 # Physical interaction range

            constants = [R_s, R_b, A_p, A_s, B_p, B_s, A_b, B_b, v_0, T_alpha, N_lb, N_ub, m]

            agent_constants.append(constants)

        for agent in agents[third:2*third]:
            
            #Middle aged

            v_0 = 1.34 * 1000 # Desired speed
            T_alpha = 0.55 # Relaxation time
            A_b = 10 * 500 # Boundary interaction strength
            B_b = 0.1 * 150 # Boundary interaction range    
            A_s = 2.3 * 1000 # Social interaction strength
            B_s = 0.3 * 150 # Social interaction range
            N_lb = -1000 # Noise lower bound
            N_ub = 1000 # Noise upper bound
            m = 1   # Mass of the agent
            R_s = 100 # Radius of the social force
            R_b = 70 # Radius of the boundary force
            A_p = 4000 # Physical interaction strength
            B_p = 0.1 * 150 # Physical interaction range
            
            constants = [R_s, R_b, A_p, A_s, B_p, B_s, A_b, B_b, v_0, T_alpha, N_lb, N_ub, m]

            agent_constants.append(constants)

        for agent in agents[2*third:]:
            
            #Old

            v_0 = 1 * 1000 # Desired speed
            T_alpha = 0.7 # Relaxation time
            A_b = 10 * 500 # Boundary interaction strength
            B_b = 0.1 * 150 # Boundary interaction range    
            A_s = 2.3 * 1000 # Social interaction strength
            B_s = 0.3 * 150 # Social interaction range
            N_lb = -200 # Noise lower bound
            N_ub = 200 # Noise upper bound
            m = 1   # Mass of the agent
            R_s = 100 # Radius of the social force
            R_b = 70 # Radius of the boundary force
            A_p = 4000 # Physical interaction strength
            B_p = 0.1 * 150 # Physical interaction range

            constants = [R_s, R_b, A_p, A_s, B_p, B_s, A_b, B_b, v_0, T_alpha, N_lb, N_ub, m]

            agent_constants.append(constants)


    elif homohetero == "test":

        third = int(NUMBER_OF_AGENTS / 3)
        for agent in agents[0:third]:
            
            #Young

            v_0 = 1 * 1000 # Desired speed
            T_alpha = 0.4 # Relaxation time
            A_b = 10 * 500 # Boundary interaction strength
            B_b = 0.1 * 150 # Boundary interaction range    
            A_s = 2.3 * 1000 # Social interaction strength
            B_s = 0.3 * 150 # Social interaction range
            N_lb = -3000 # Noise lower bound
            N_ub = 3000 # Noise upper bound
            m = 1   # Mass of the agent
            R_s = 100 # Radius of the social force
            R_b = 70 # Radius of the boundary force
            A_p = 4000 # Physical interaction strength
            B_p = 0.1 * 150 # Physical interaction range

            constants = [R_s, R_b, A_p, A_s, B_p, B_s, A_b, B_b, v_0, T_alpha, N_lb, N_ub, m]

            agent_constants.append(constants)

        for agent in agents[third:2*third]:
            
            #Middle aged

            v_0 = 1.34 * 1000 # Desired speed
            T_alpha = 0.55 # Relaxation time
            A_b = 10 * 500 # Boundary interaction strength
            B_b = 0.1 * 150 # Boundary interaction range    
            A_s = 2.3 * 1000 # Social interaction strength
            B_s = 0.3 * 150 # Social interaction range
            N_lb = -1000 # Noise lower bound
            N_ub = 1000 # Noise upper bound
            m = 1   # Mass of the agent
            R_s = 100 # Radius of the social force
            R_b = 70 # Radius of the boundary force
            A_p = 4000 # Physical interaction strength
            B_p = 0.1 * 150 # Physical interaction range
            
            constants = [R_s, R_b, A_p, A_s, B_p, B_s, A_b, B_b, v_0, T_alpha, N_lb, N_ub, m]

            agent_constants.append(constants)

        for agent in agents[2*third:]:
            
            #Old

            v_0 = 1 * 1000 # Desired speed
            T_alpha = 0.7 # Relaxation time
            A_b = 10 * 500 # Boundary interaction strength
            B_b = 0.1 * 150 # Boundary interaction range    
            A_s = 2.3 * 1000 # Social interaction strength
            B_s = 0.3 * 150 # Social interaction range
            N_lb = -200 # Noise lower bound
            N_ub = 200 # Noise upper bound
            m = 1   # Mass of the agent
            R_s = 100 # Radius of the social force
            R_b = 70 # Radius of the boundary force
            A_p = 4000 # Physical interaction strength
            B_p = 0.1 * 150 # Physical interaction range

            constants = [R_s, R_b, A_p, A_s, B_p, B_s, A_b, B_b, v_0, T_alpha, N_lb, N_ub, m]

            agent_constants.append(constants)

    return agent_constants

INSTRUCT_1_TEXT = [ "Welcome to a simple evacuation simulation!",
                    " ",
                    "Empirical data will be collected for research purposes only.",
                    "The data collected will be fully anonymous.",
                    "By starting the simulation, you are consenting to collection of your data.",
                    "You have the right to withdraw from the research at any time before",
                    "your data is receieved.",
                    "Simply close the window to withdraw from the experiment.",
                    " ",
                    "Click the mouse to move your character.",
                    "First, navigate your way to the red cross.",   
                    " ",                   
                    "Press SPACE to start",
                   ]

INSTRUCT_2_TEXT = [ "Great!", 
                    "Now, reach the exit as quickly as possible.",
                    "Try to collide with as few red agents as possible on your way.",
                    "Press SPACE to start",
                    ]

INSTRUCT_FONT = pygame.font.Font(None, 36)
INSTRUCT_TEXT_COLOR = (0, 0, 0)

TIMER_FONT = pygame.font.Font(None, 36)
TIMER_TEXT_COLOR = (0, 0, 0)

# Function to display the first instructional screen
def display_instructional_screen_1(screen):
    screen.fill(BACKGROUND_COLOR)
    for i, line in enumerate(INSTRUCT_1_TEXT):
        text = INSTRUCT_FONT.render(line, True, INSTRUCT_TEXT_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - len(INSTRUCT_1_TEXT) * text.get_height() // 2 + i * text.get_height()))
    pygame.display.flip()

# Function to display the second instructional screen
def display_instructional_screen_2(screen):
    screen.fill(BACKGROUND_COLOR)
    for i, line in enumerate(INSTRUCT_2_TEXT):
        text = INSTRUCT_FONT.render(line, True, INSTRUCT_TEXT_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - len(INSTRUCT_2_TEXT) * text.get_height() // 2 + i * text.get_height()))
    pygame.display.flip()

# Function to write data collected to a file
def save_data_to_file(evac_time, collisions, clicks, route_choice, indecisive_time, data_records):
    # Create a Pandas DataFrame with the data_records
    df = pd.DataFrame(data_records)
    #Save the dataframe to a file
    df.to_csv("output_data_records.csv")
    # Now, write the other information to a new sheet
    other_data = {
        'Treatment': [SELECTED_TREATMENT],
        'Evacuation Time': [evac_time],
        'Collisions': [collisions],
        'Clicks': [clicks],
        'Route Choice': [route_choice],
        'Indecisive Time': [indecisive_time]
    }
    # Write to a new sheet
    df_other = pd.DataFrame(other_data)
    df_other.to_csv("output.csv", mode='a', header=True)


# Initialize Pygame
#pygame.init()
#screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load the background image
#background = pygame.image.load("Graphics/background.png").convert_alpha()

# Create the player
#player = Player(WIDTH // 2, HEIGHT // 2, CHARACTER_RADIUS)
player = Player(10, 375, CHARACTER_RADIUS)
target_x, target_y = player.x, player.y
moving = False

# Define rectangle coordinates

rectangles = [              # Rectangles, in the format (x1, y1, width, height)
    (40, 710, 820, 40),
    (40, 0, 820, 40),
    (860, 0, 40, 900),
    (0, 0, 40, 335),
    (0, 415, 40, 335),
    (200, 590, 550, 40),
    (200, 120, 550, 40),
    (830, 120, 30, 40), #(810, 120, 50, 40)
    (830, 590, 30, 40), #(810, 590, 50, 40)
    (160, 105, 40, 540), #(160, 100, 40, 550)
    (160, 695, 40, 15), #(160, 690, 40, 20)
    (160, 40, 40, 15), #(160, 40, 40, 20)
]
#Make sure to change manually if the doorways are changed
#When the player enters one of these rectangles, the route choice is noted
ROUTE_CHOICE_A_RECT = (750, 40, 830, 160) # (x1,y1,x2,y2)
ROUTE_CHOICE_B_RECT = (750, 590, 830, 710) # (x1,y1,x2,y2)

# Rectangles in the (x1, y1, x2, y2) format

rectangles_corners = [(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]) for rect in rectangles]

# Define agent coordinates
agent_coords = generate_agent_positions(NUMBER_OF_AGENTS, SPAWN_BOX_COORDS, [(WIDTH//2, HEIGHT//2)], 2 * CHARACTER_RADIUS)

# Initialise agent velocities
agent_velocities = [(0, 0) for _ in range(NUMBER_OF_AGENTS)]

# Create agents
agents = [Agent(agent_coords[i][0], agent_coords[i][1], CHARACTER_RADIUS, i) for i in range(NUMBER_OF_AGENTS)]

# Apply treatments
if SELECTED_TREATMENT == "C":

    agent_targets = route_split(agents, agent_coords, 50)

    agent_constants = generate_agent_constants(agents, "homo")

    agent_constant_list = []

    for i in range(NUMBER_OF_AGENTS):
        agent_constant_list.append(agent_constants[i])
    

elif SELECTED_TREATMENT == "H":

    agent_targets = route_split(agents, agent_coords, 50)

    agent_constants = generate_agent_constants(agents, "hetero")

    agent_constant_list = []

    for i in range(NUMBER_OF_AGENTS):
        agent_constant_list.append(agent_constants[i])


elif SELECTED_TREATMENT == "A":

    agent_targets = route_split(agents, agent_coords, 70)

    agent_constants = generate_agent_constants(agents, "homo")

    agent_constant_list = []

    for i in range(NUMBER_OF_AGENTS):
        agent_constant_list.append(agent_constants[i])


elif SELECTED_TREATMENT == "HA":

    agent_targets = route_split(agents, agent_coords, 70)

    agent_constants = generate_agent_constants(agents, "hetero")

    agent_constant_list = []

    for i in range(NUMBER_OF_AGENTS):
        agent_constant_list.append(agent_constants[i])


elif SELECTED_TREATMENT == "T":

    agent_targets = route_split(agents, agent_coords, 50)

    agent_constants = generate_agent_constants(agents, "test")

    agent_constant_list = []

    for i in range(NUMBER_OF_AGENTS):
        agent_constant_list.append(agent_constants[i])

else:
    raise ValueError("Invalid treatment selected")

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evacuation Simulation")

# Create a clock (For ceiling FPS limit. If the game becomes complex, it may be necessary to implement an FPS floor limit.)
clock = pygame.time.Clock()

# Display instructional screen 1
display_instructional_screen_1(screen)
instructional_screen_1_active = True #True 
instructional_screen_2_active = False
initial_navigation = False
main_simulation = False #False
#agents_present = True
player_present = True
final_screen = False
collisions = 0
collison_occurred = [False] * NUMBER_OF_AGENTS
original_indices = list(range(NUMBER_OF_AGENTS))
clicks = 0
route_choice = None
data_records = [[] for _ in range(NUMBER_OF_AGENTS + 1)]
removed_indices = []
counter = 0
reset_counter = False

# Game loop

running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and instructional_screen_1_active:
            instructional_screen_1_active = False
            initial_navigation = True
            VELOCITY = VELOCITY / 15 # Slow down the player for the initial navigation as the simulation is running faster

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and instructional_screen_2_active:
            instructional_screen_2_active = False
            main_simulation = True
            VELOCITY = VELOCITY * 13 # Speed up the player for the main simulation as the simulation is running slower
            main_simulation_start = pygame.time.get_ticks() # Start the timer for the main simulation

        elif event.type == pygame.MOUSEBUTTONDOWN:
            target_x, target_y = pygame.mouse.get_pos()
            moving = True
            if main_simulation:
                clicks += 1


    if instructional_screen_1_active:
        continue # Skip the rest of the loop if the first instructional screen is active    

    # Print the mouse position
    #print(f"Mouse Position: ({pygame.mouse.get_pos()[0]}, {pygame.mouse.get_pos()[1]})")

    if initial_navigation:
        
        if moving:
            player.move_towards(target_x, target_y, rectangles_corners, agent_coords)
            if math.hypot(target_x - player.x, target_y - player.y) < 1:
                moving = False

        #Draw the background
        screen.fill(BACKGROUND_COLOR)
        # Draw the rectangles
        for rect in rectangles:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(rect[0], rect[1], rect[2], rect[3]))
        # Draw the character
        pygame.draw.circle(screen, CHARACTER_COLOR, (int(player.x), int(player.y)), player.radius)            
        # Draw the target
        cross_size = 10 
        pygame.draw.line(screen, CROSS_COLOR, (WIDTH // 2 - cross_size, HEIGHT // 2 - cross_size), (WIDTH // 2 + cross_size, HEIGHT // 2 + cross_size), 4)
        pygame.draw.line(screen, CROSS_COLOR, (WIDTH // 2 - cross_size, HEIGHT // 2 + cross_size), (WIDTH // 2 + cross_size, HEIGHT // 2 - cross_size), 4)

        pygame.display.flip()

        if math.hypot(WIDTH // 2 - player.x, HEIGHT // 2 - player.y) < CHARACTER_RADIUS:
            initial_navigation = False
            instructional_screen_2_active = True

            # Reset player's position to the center before main_simulation
            player.x, player.y = WIDTH // 2, HEIGHT // 2
            # Reset the target coordinates as well, if needed
            target_x, target_y = player.x, player.y

        continue # Skip the rest of the loop if initial navigation is active

    if instructional_screen_2_active:
        display_instructional_screen_2(screen)
        continue

    if main_simulation:
        
        counter += 1

        if player_present:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - main_simulation_start) / 1000 # Elapsed time in seconds

        if moving:
            player.move_towards(target_x, target_y, rectangles_corners, agent_coords)
            if math.hypot(target_x - player.x, target_y - player.y) < 1:
                moving = False

        # Draw the background
        #screen.blit(background, (0, 0))
        screen.fill(BACKGROUND_COLOR)
                
        # Draw the rectangles
        for rect in rectangles:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(rect[0], rect[1], rect[2], rect[3]))

        # Draw the character
        if player_present:
            pygame.draw.circle(screen, CHARACTER_COLOR, (int(player.x), int(player.y)), player.radius)

        # Draw the target
        cross_size = 10 
        pygame.draw.line(screen, CROSS_COLOR, (10 - cross_size, 375 - cross_size), (10 + cross_size, 375 + cross_size), 4)
        pygame.draw.line(screen, CROSS_COLOR, (10 - cross_size, 375 + cross_size), (10 + cross_size, 375 - cross_size), 4)

        # Determine player route choice
        if route_choice == None:
            if player.x > ROUTE_CHOICE_A_RECT[0] and player.y > ROUTE_CHOICE_A_RECT[1] and player.x < ROUTE_CHOICE_A_RECT[2] and player.y < ROUTE_CHOICE_A_RECT[3]:
                route_choice = "A"
                choice_made_time = pygame.time.get_ticks()
            elif player.x > ROUTE_CHOICE_B_RECT[0] and player.y > ROUTE_CHOICE_B_RECT[1] and player.x < ROUTE_CHOICE_B_RECT[2] and player.y < ROUTE_CHOICE_B_RECT[3]:
                route_choice = "B"
                choice_made_time = pygame.time.get_ticks()
        
        # List of indices of agents that have reached their final target 
        agents_to_remove = []

        # Move the agents
        for i in range(NUMBER_OF_AGENTS):
            agent = agents[i]

            # Collision counter
            distance_to_player = math.hypot(player.x - agent_coords[i][0], player.y - agent_coords[i][1])
            if collison_occurred[i] == False and distance_to_player <= 2.5 * CHARACTER_RADIUS:
                collisions += 1
                collison_occurred[i] = True
            if distance_to_player > 2.5 * CHARACTER_RADIUS:
                collison_occurred[i] = False

            if counter == 60:
                data_records[agent.index + 1].append((round(agent_coords[i][0], 3), round(agent_coords[i][1], 3), round(agent_velocities[i][0], 3), round(agent_velocities[i][1], 3)))
                reset_counter = True

            pygame.draw.circle(screen, AGENT_COLOR, agent_coords[i], CHARACTER_RADIUS) # Draw the agent
            prev_x, prev_y = agent_coords[i]
            agent_constant = agent_constants[i]
            prev_x, prev_y, prev_vel_x, prev_vel_y, agent_target_x, agent_target_y = agent.x, agent.y, agent_velocities[i][0], agent_velocities[i][1], agent_targets[i][0], agent_targets[i][1]
            agent_x, agent_y, agent_vel_x, agent_vel_y, agent_target_x, agent_target_y = agent.move_towards(
            prev_vel_x, prev_vel_y, rectangles_corners, agent_coords, agent_constant)
            agent_coords[i] = (agent_x, agent_y)
            agent_velocities[i] = (agent_vel_x, agent_vel_y)
            agent_targets[i] = (agent_target_x, agent_target_y)

            distance_to_final_target = math.hypot(agent_x - agent.route[-1][0], agent_y - agent.route[-1][1])
            if distance_to_final_target < ROUTE_A_TARGET_6[2]:
                agents_to_remove.append(i)
                removed_indices.append(agent.index)

        

        # Remove agent i from all lists if it has reached its final target
        for i in reversed(agents_to_remove): # Reverse the list of indices to remove to avoid index errors
            agent_coords.pop(i)
            agent_velocities.pop(i)
            agent_targets.pop(i)
            agent_constant_list.pop(i)
            collison_occurred.pop(i)
            agents.pop(i)
            NUMBER_OF_AGENTS -= 1

        if counter == 60:
            data_records[0].append((round(player.x, 3), round(player.y, 3), None, None))
            for i in removed_indices:
                data_records[i + 1].append((None,None,None,None))
            reset_counter = True

        if reset_counter:
            counter = 0
            reset_counter = False

        player_distance_to_final_target = math.hypot(player.x - ROUTE_A_TARGET_6[0], player.y - ROUTE_A_TARGET_6[1])
        if player_distance_to_final_target < ROUTE_A_TARGET_6[2]:
            player_present = False

        font = pygame.font.Font(None, 36)

        if player_present == False:
            
            main_simulation = False
            final_screen = True
            main_simulation_end = pygame.time.get_ticks()

        # Draw the timer
        timer_text = TIMER_FONT.render(f"Time: {elapsed_time:.2f}", True, TIMER_TEXT_COLOR)
        screen.blit(timer_text, (10, 10))

        # Draw the collision counter
        collision_text = TIMER_FONT.render(f"Collisions: {collisions}", True, TIMER_TEXT_COLOR)
        screen.blit(collision_text, (700, 10))

        if player_present == False:
            main_simulation = False
            final_screen = True
            main_simulation_end = pygame.time.get_ticks()

    if final_screen:
        evac_time = (main_simulation_end - main_simulation_start) / 1000
        indecisive_time = (choice_made_time - main_simulation_start) / 1000
        #display_final_screen(screen, evac_time)
        """
        END_STATS_TEXT = [ "Evacuation complete!",
                    "Time taken (player): " + str(evac_time) + " seconds",
                    "Collisions: " + str(collisions),
                    "Click counter: " + str(clicks),
                    "Route choice: " + str(route_choice),
                    "Time to leave starting room: " + str(indecisive_time) + " seconds",
                    "You may now close the window.",
                    ]
        """
        END_STATS_TEXT = [  "Evacuation complete!",
                            "Thank you very much for participating!",
                            "Two files named 'output.csv' and 'output_data_records.csv' will be",
                            "downloaded to your computer when this window is closed.",
                            "They should appear in the same location that you saved this simulation.",
                            "If you were emailed this simulation, please send the files to:",
                            " ",
                            "gj20079@bristol.ac.uk",
                            " ",
                            "If you have any questions, please do not hesitate to ask.",
                            " ",
                            "You may now close the window.",]
        screen.fill(BACKGROUND_COLOR)
        for i, line in enumerate(END_STATS_TEXT):
            text = INSTRUCT_FONT.render(line, True, INSTRUCT_TEXT_COLOR)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - len(END_STATS_TEXT) * text.get_height() // 2 + i * text.get_height()))

        

    pygame.display.update()
    clock.tick(FPS)

# Save data at the end of the simulation
save_data_to_file(evac_time, collisions, clicks, route_choice, indecisive_time, data_records)

# Quit Pygame
pygame.quit()
sys.exit()