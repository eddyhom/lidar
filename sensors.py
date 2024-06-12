import pygame
import math
import numpy as np
import environment

class LaserSensor:
    def __init__(self, sensor_range, floor_plan, uncertainty):
        self.range = sensor_range
        self.speed = 4 # rounds per second --> TODO: Name rotation_speed?
        self.sigma = np.array([uncertainty[0], uncertainty[1]]) # Sensor noise
        self.position = (0, 0)
        self.map = floor_plan
        self.width, self.height = pygame.display.get_surface().get_size()
        self.sensed_obstacles = []

    def calculate_distance(self, obstacle_position):
        px = (obstacle_position[0] - self.position[0])**2
        py = (obstacle_position[1] - self.position[1])**2

        return math.sqrt(px + py)
    
    def found_obstacles(self):
        data = []
        x_sensor_pos, y_sensor_pos = self.position[0], self.position[1]
        # Rotate from 0 -> 360 degrees with a resolution of 60. 360/60=6.
        # Take a sample every 6 degrees.
        for angle in np.linspace(0, 2*math.pi, 60, False):
            # Create line between sensor and range
            # At every step angle, take 100 steps along the line.
            x_line_max, y_line_max = (x_sensor_pos + (self.range * math.cos(angle)), y_sensor_pos - (self.range * math.sin(angle)))
            for i in range(0, 100):
                line_step = i / 100
                x_step = int(x_line_max * line_step + x_sensor_pos * (1 - line_step))
                y_step = int(y_line_max * line_step + y_sensor_pos * (1 - line_step))

                # First check if coordinate is inside window
                if self.is_coord_inside_window((x_step, y_step)):
                    # Get the color from given coordinate
                    if self.map.get_at((x_step, y_step)) == pygame.Color("black"):
                        distance = self.calculate_distance((x_step, y_step))
                        output = add_uncertainty(distance, angle, self.sigma)
                        output.append(self.position)
                        # Store the measurements
                        data.append(output)
                        break
        if len(data) > 0:
            return data
        else:
            return []

    def is_coord_inside_window(self, coord):
        '''Check if coordinates are inside window'''
        return (0 < coord[0] < self.width and 0 < coord[1] < self.height)
        

def add_uncertainty(distance, angle, sigma):
    mean = np.array([distance, angle])
    covariance = np.diag(sigma ** 2)
    distance, angle = np.random.multivariate_normal(mean, covariance)
    distance = max(distance, 0)
    angle = max(angle, 0)
    return [distance, angle]


if __name__ == '__main__':
    env = environment.buildEnvironment((1200, 600))
    laser = LaserSensor(200, env.original_map, uncertainty=(0.5, 0.01))
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        pygame.display.update()

    pygame.quit()