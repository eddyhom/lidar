import math
import pygame


class buildEnvironment:
    def __init__(self, map_dimensions):
        self.point_cloud = []
        self.map_width, self.map_height = map_dimensions
        self.window_name = "Lidar Project"
        self.external_map = pygame.image.load('map1.png')

        pygame.init()
        pygame.display.set_caption(self.window_name)
        
        self.map = pygame.display.set_mode((self.map_width, self.map_height)) ## Empty screen!!!
        self.original_map = self.map.copy()
        self.map.blit(self.external_map, (0, 0)) # Add Map to screen

        self.info_map = self.map.copy()

    def convert_ad_to_pos(self, distance, angle, sensor_pos):
        '''Convert Angle-Distance to coordinate position'''
        x_pos = distance * math.cos(angle) + sensor_pos[0]
        y_pos = -distance * math.sin(angle) + sensor_pos[1]

        return (int(x_pos), int(y_pos))
    
    def data_storage(self, data):
        '''Store data in point cloud, we get distance, angle and sensor position in data'''
        for element in data:
            point = self.convert_ad_to_pos(element[0], element[1], element[2])
            if point not in self.point_cloud:
                self.point_cloud.append(point)


    def draw_sensor_data(self):
        self.info_map = self.map.copy()
        for point in self.point_cloud:
            self.info_map.set_at((int(point[0]), int(point[1])), pygame.Color("red"))

if __name__ == '__main__':
    env = buildEnvironment((1200, 600))
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        pygame.display.update()

    pygame.quit()