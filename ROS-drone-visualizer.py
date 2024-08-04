#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32MultiArray
import pygame
import math

_FREQUENCY = 20

class Tracker:
    def __init__(self):
        rospy.init_node('tracker')
        self._last_received = rospy.get_time()
        self._rate = rospy.get_param('~rate', _FREQUENCY)
        rospy.Subscriber('radio', Int32MultiArray, self.cmds)
        
        # pygame setup
        pygame.init()
        pygame.display.set_caption("Drone Path Tracking")
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.path = [self.player_pos.copy()]  # List to store the path
        self.circles = []  # List to store circles' positions
        
        # Load and scale the drone image
        self.drone = pygame.image.load('/home/karun/code/dronecode/Drone-with-heading.bmp').convert()
        self.drone = pygame.transform.scale(self.drone, (100, 100))  # Scale image to 100x100 pixels
        
        # Initial rotation angle
        self.angle = 0

        # Initialize control values
        self.roll = 1500
        self.pitch = 1500
        self.throttle = 1500
        self.yaw = 1500
        self.channel5 = 0
        self.channel6 = 0

    def cmds(self, message):
        self._last_received = rospy.get_time()
        channels = message.data
        self.roll = channels[0]
        self.pitch = channels[1]
        self.throttle = channels[2]
        self.yaw = channels[3]
        self.channel5 = channels[4]
        self.channel6 = channels[5]

    def run(self):
        rate = rospy.Rate(self._rate)
        while not rospy.is_shutdown() and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill("white")

            if self.channel5 is not None and self.channel6 is not None:
                if self.channel5 == 1100 and self.channel6 == 1200:
                    if self.yaw > 1500:
                        self.angle += (self.yaw - 1500) * self.dt  # Rotate clockwise
                    if self.yaw < 1500:
                        self.angle -= (1500 - self.yaw) * self.dt  # Rotate counterclockwise

                    # Calculate heading direction
                    radians = math.radians(self.angle)
                    heading_x = math.cos(radians)
                    heading_y = -math.sin(radians)

                    if self.pitch > 1500:
                        self.player_pos.x += heading_x * (self.pitch - 1500) * self.dt
                        self.player_pos.y += heading_y * (self.pitch - 1500) * self.dt
                    if self.pitch < 1500:
                        self.player_pos.x -= heading_x * (1500 - self.pitch) * self.dt
                        self.player_pos.y -= heading_y * (1500 - self.pitch) * self.dt
                    if self.roll > 1500:
                        self.player_pos.x += heading_y * (self.roll - 1500) * self.dt
                        self.player_pos.y -= heading_x * (self.roll - 1500) * self.dt
                    if self.roll < 1500:
                        self.player_pos.x -= heading_y * (1500 - self.roll) * self.dt
                        self.player_pos.y += heading_x * (1500 - self.roll) * self.dt
            
                    # Append the new position to the path
                    self.path.append(self.player_pos.copy())

                    # Draw the path
                    for i in range(len(self.path) - 1):
                        pygame.draw.line(self.screen, "green", self.path[i], self.path[i + 1], 4)

                    keys = pygame.key.get_pressed()
                    # Draw circles when B key is pressed
                    if keys[pygame.K_b]:
                        self.circles.append(self.player_pos.copy())
                    
                    for circle_pos in self.circles:
                        pygame.draw.circle(self.screen, "red", (int(circle_pos.x), int(circle_pos.y)), 10)
                    
                    # Rotate the drone image
                    rotated_drone = pygame.transform.rotate(self.drone, self.angle)
                    rect = rotated_drone.get_rect(center=self.player_pos)
                    
                    # Render game here
                    self.screen.blit(rotated_drone, rect.topleft)
                    
                    # Flip display
                    pygame.display.flip()

                    self.dt = self.clock.tick(60) / 1000

        pygame.quit()

if __name__ == '__main__':
    tracker = Tracker()
    tracker.run()
