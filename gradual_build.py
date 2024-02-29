import pygame
import sys
import math
import random

"""
This simulation is scaled to 1 pixel = 0.025 meters. Each agent has a diameter of 0.5 meters (20 pixels).

"""

# Constants
WIDTH, HEIGHT = 900, 750
BACKGROUND_COLOR = (255, 255, 255)
CHARACTER_COLOR = (0, 0, 0)
AGENT_COLOR = (255, 0, 0)
CHARACTER_RADIUS = 7 #10 is the desired atm
VELOCITY = 1.34   # Desired speed of the player
FPS = 60  # Frames per second
TIMESTEP = 1 / FPS  # Timestep for the simulation
NUMBER_OF_AGENTS = 50  # Number of agents in the simulation
X_CLOSEST_AGENTS = 5  # Number of closest agents to consider for the social force calculation
TARGET_CHANGE_RADIUS = 3 * CHARACTER_RADIUS  # Radius within which the agent changes target

# Targets
ROUTE_A_TARGET_1 = (780, 200)
ROUTE_A_TARGET_2 = (780, 80)
ROUTE_A_TARGET_3 = (220, 80)
ROUTE_A_TARGET_4 = (140, 80)
ROUTE_A_TARGET_5 = (60, 375)
ROUTE_A_TARGET_6 = (10, 375)

ROUTE_A = [ROUTE_A_TARGET_1, ROUTE_A_TARGET_2, ROUTE_A_TARGET_3, ROUTE_A_TARGET_4, ROUTE_A_TARGET_5, ROUTE_A_TARGET_6]

ROUTE_B_TARGET_1 = (780, 550)
ROUTE_B_TARGET_2 = (780, 670)
ROUTE_B_TARGET_3 = (220, 670)
ROUTE_B_TARGET_4 = (140, 670)
ROUTE_B_TARGET_5 = (60, 375)
ROUTE_B_TARGET_6 = (10, 375)

ROUTE_B = [ROUTE_B_TARGET_1, ROUTE_B_TARGET_2, ROUTE_B_TARGET_3, ROUTE_B_TARGET_4, ROUTE_B_TARGET_5, ROUTE_B_TARGET_6]



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
#Almost doesn't matter if the values are physical sensible, as long as the simulation looks realistic

# Constants for the social force calculation
# Directly from the Helbing paper:

v_0 = 1.34 * 1000   # Desired speed
T_alpha = 0.5       # Relaxation time ('smaller values make the agents walk mmore aggressively')
A_b = 10 * 500      # Boundary interaction strength
B_b = 0.1 * 150     # Boundary interaction range
A_s = 2.3 * 1000    # Social interaction strength (Interpreted from paper, not concrete. Helbing's paper uses these terms, but without a physcial component.)
B_s = 0.3 * 150     # Social interaction range

# Personally chosen values

N_lb = -0.5         # Noise lower bound
N_ub = 0.5          # Noise upper bound
m = 1               # Mass of the agent
R_s = 100           # Radius of the social force
R_b = 70            # Radius of the boundary force
A_p = 4000          # Physical interaction strength
B_p = 0.1 * 150     # Physical interaction range




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
class Agent:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.current_target = 0 

    def calculate_social_force(self, agent_coords, x_closest_agents=X_CLOSEST_AGENTS):
        FS = [0, 0]  # Initialize the social force vector

        P_alpha = (self.x, self.y)

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

        agent_coords.pop() # Remove the player from the list of agents

        return FS

    def calculate_boundary_force(self, rectangles_corners): #careful with small doorways
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
        R_s, R_b, A_p, A_s, B_p, B_s, A_b, B_b, v_0, T_alpha, N_lb, N_ub, m = constants

        # Calculate the social force
        FS = self.calculate_social_force(agent_coords)

        # Calculate the boundary force
        FB = self.calculate_boundary_force(rectangles)

        agent_target_x, agent_target_y = ROUTE_B[self.current_target]

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

        # Update the agent's position
        #new_x = self.x + 1 / 2 * F[0] * TIMESTEP ** 2
        #new_y = self.y + 1 / 2 * F[1] * TIMESTEP ** 2

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
        
        agent_coords.append((player.x, player.y))
        # Check if the new position is inside any of the agents or the player
        for agent in agent_coords:
            if agent == (self.x, self.y):
                continue
            distance_to_closest = math.hypot(new_x - agent[0], new_y - agent[1])
            if distance_to_closest < 2 * CHARACTER_RADIUS:
                collision_detected = True
                break  # Do not update position if it would intersect with an agent or the player

        agent_coords.pop()

        # Update the agent's position
        if not collision_detected:
            self.x = new_x
            self.y = new_y
            velocity_x = velocity_x_new
            velocity_y = velocity_y_new

        if distance_to_target < TARGET_CHANGE_RADIUS: # 2 * CHARACTER_RADIUS is the original value
            self.current_target += 1
            agent_target_x, agent_target_y = ROUTE_B[self.current_target]

        return self.x, self.y, velocity_x, velocity_y, agent_target_x, agent_target_y # Return the new position and velocity of the agent


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load the background image
#background = pygame.image.load("Graphics/background.png").convert_alpha()

# Create the player
player = Player(WIDTH // 2, HEIGHT // 2, CHARACTER_RADIUS)
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
    (810, 120, 50, 40),
    (810, 590, 50, 40), #
    (160, 100, 40, 550),
    (160, 690, 40, 20), #
    (160, 40, 40, 20), #
]

# Rectangles in the (x1, y1, x2, y2) format

rectangles_corners = [(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]) for rect in rectangles]

# Define agent coordinates
agent_coords = [(random.randint(170, 700), random.randint(170, 575)) for _ in range(NUMBER_OF_AGENTS)]

# Initialise agents' first target
agent_targets = [ROUTE_B[0] for _ in range(NUMBER_OF_AGENTS)]
print(agent_targets)

# Initialise agent velocities
agent_velocities = [(0, 0) for _ in range(NUMBER_OF_AGENTS)]

# Create agents
agents = [Agent(agent_coords[i][0], agent_coords[i][1], CHARACTER_RADIUS) for i in range(NUMBER_OF_AGENTS)]

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clickable Character Movement")

# Create a clock (For ceiling FPS limit. If the game becomes complex, it may be necessary to implement an FPS floor limit.)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            target_x, target_y = pygame.mouse.get_pos()
            moving = True

    if moving:

        player.move_towards(target_x, target_y, rectangles_corners, agent_coords)
        if math.hypot(target_x - player.x, target_y - player.y) < 1:
            moving = False

    # Print the mouse position
    #print(f"Mouse Position: ({pygame.mouse.get_pos()[0]}, {pygame.mouse.get_pos()[1]})")

    # Draw the background
    #screen.blit(background, (0, 0))
    screen.fill(BACKGROUND_COLOR)
            
    # Draw the rectangles
    for rect in rectangles:
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(rect[0], rect[1], rect[2], rect[3]))

    # Draw the character
    pygame.draw.circle(screen, CHARACTER_COLOR, (int(player.x), int(player.y)), player.radius)

    # Draw the agents
    #for i in range(NUMBER_OF_AGENTS):
    #    pygame.draw.circle(screen, AGENT_COLOR, agent_coords[i], CHARACTER_RADIUS)
    
    # List of indices of agents that have reached their final target 
    agents_to_remove = []

    # Move the agents
    for i in range(NUMBER_OF_AGENTS):
        agent = agents[i]
        pygame.draw.circle(screen, AGENT_COLOR, agent_coords[i], CHARACTER_RADIUS)
        prev_x, prev_y = agent_coords[i]
        prev_x, prev_y, prev_vel_x, prev_vel_y, agent_target_x, agent_target_y = agent.x, agent.y, agent_velocities[i][0], agent_velocities[i][1], agent_targets[i][0], agent_targets[i][1]
        agent_x, agent_y, agent_vel_x, agent_vel_y, agent_target_x, agent_target_y = agent.move_towards(
        prev_vel_x, prev_vel_y, rectangles_corners, agent_coords, [R_s, R_b, A_p, A_s, B_p, B_s, A_b, B_b, v_0, T_alpha, N_lb, N_ub, m])
        agent_coords[i] = (agent_x, agent_y)
        agent_velocities[i] = (agent_vel_x, agent_vel_y)
        agent_targets[i] = (agent_target_x, agent_target_y)

        distance_to_final_target = math.hypot(agent_x - ROUTE_B[-1][0], agent_y - ROUTE_B[-1][1])
        if distance_to_final_target < TARGET_CHANGE_RADIUS:
            agents_to_remove.append(i)

    # Remove agent i from all lists if it has reached its final target
    for i in reversed(agents_to_remove): # Reverse the list of indices to remove to avoid index errors
        agent_coords.pop(i)
        agent_velocities.pop(i)
        agent_targets.pop(i)
        agents.pop(i)
        NUMBER_OF_AGENTS -= 1

    pygame.display.update()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()