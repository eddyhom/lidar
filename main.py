import environment as env
import sensors
import pygame
import math



if __name__ == '__main__':
    environment = env.buildEnvironment((1200, 600))
    environment.original_map = environment.map.copy()
    laser = sensors.LaserSensor(75, environment.original_map, uncertainty=(0.5, 0.01))
    environment.map.fill(pygame.Color("black"))
    environment.info_map = environment.map.copy()

    run = True

    while run:
        sensor_on = False # Only On if mouse cursor inside window

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_focused():
                sensor_on = True
            elif not pygame.mouse.get_focused():
                sensor_on = False

        if sensor_on:
            position = pygame.mouse.get_pos()
            laser.position = position
            sensor_data = laser.found_obstacles()
            environment.data_storage(sensor_data)
            environment.draw_sensor_data()
        environment.map.blit(environment.info_map, (0,0))

        pygame.display.update()

    pygame.quit()