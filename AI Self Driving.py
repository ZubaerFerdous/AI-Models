# %%
import pygame
import random
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60

# Colors
COLORS = {
    'GREY': (90, 90, 90),
    'DARK_GREY': (58, 58, 58),
    'ROAD': (42, 42, 42),
    'YELLOW': (255, 200, 0),
    'WHITE': (255, 255, 255),
    'RED': (230, 57, 70),
    'BLUE': (29, 53, 87),
    'GREEN': (42, 157, 143),
    'PURPLE': (155, 89, 182),
    'ORANGE': (231, 111, 81),
    'LIGHT_GREY': (170, 170, 170),
    'BLACK': (0, 0, 0),
    'GOLD': (255, 215, 0)
}

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Self-Driving Car Simulator")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 18)
tiny_font = pygame.font.Font(None, 14)

# Define lanes - cars stay in exact lanes
HORIZONTAL_LANES = {
    'top': 350,      # Westbound (right to left)
    'bottom': 430    # Eastbound (left to right)
}

VERTICAL_LANES = {
    'left_down': 425,     # Southbound (top to bottom)
    'left_up': 475,       # Northbound (bottom to top)
    'right_down': 725,    # Southbound (top to bottom)
    'right_up': 775       # Northbound (bottom to top)
}

# Intersection boundaries
INTERSECTIONS = [
    {'x': 450, 'y': 390, 'left': 400, 'right': 500, 'top': 300, 'bottom': 480},
    {'x': 750, 'y': 390, 'left': 700, 'right': 800, 'top': 300, 'bottom': 480}
]


class TrafficLight:
    """Traffic light with cycling states"""
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.state = random.choice(['green', 'red'])
        self.timer = random.randint(0, 180)
        self.green_time = 200
        self.yellow_time = 60
        self.red_time = 200
    
    def update(self):
        self.timer += 1
        if self.state == 'green' and self.timer > self.green_time:
            self.state = 'yellow'
            self.timer = 0
        elif self.state == 'yellow' and self.timer > self.yellow_time:
            self.state = 'red'
            self.timer = 0
        elif self.state == 'red' and self.timer > self.red_time:
            self.state = 'green'
            self.timer = 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, COLORS['DARK_GREY'], 
                        (self.x - 8, self.y - 28, 16, 60))
        
        colors_map = {'red': (255, 0, 0), 'yellow': (255, 255, 0), 'green': (0, 255, 0)}
        for i, light in enumerate(['red', 'yellow', 'green']):
            color = colors_map[light] if self.state == light else (51, 51, 51)
            pygame.draw.circle(screen, color, (self.x, self.y - 20 + i * 20), 6)


class Vehicle:
    """Car that drives in lanes without overlap"""
    def __init__(self, x, y, color, personality, lane_type, direction):
        self.x = x
        self.y = y
        self.color = color
        self.width = 40
        self.height = 60
        self.speed = 0
        self.personality = personality
        self.lane_type = lane_type  # 'horizontal' or 'vertical'
        self.direction = direction  # 'east', 'west', 'north', 'south'
        self.lane_y = y if lane_type == 'horizontal' else None
        self.lane_x = x if lane_type == 'vertical' else None
        
        # Personality parameters
        if personality == 'aggressive':
            self.max_speed = 5
            self.acceleration = 0.15
            self.stop_distance = 70
            self.safe_distance = 80
        elif personality == 'cautious':
            self.max_speed = 3
            self.acceleration = 0.08
            self.stop_distance = 100
            self.safe_distance = 120
        else:  # adaptive
            self.max_speed = 4
            self.acceleration = 0.1
            self.stop_distance = 85
            self.safe_distance = 100
        
        self.braking = False
        self.blinker = None
        self.blinker_timer = 0
        
        # Navigation
        self.next_action = None
        self.in_intersection = False
        self.intersection_entered = None
        self.turn_target_lane = None
        
        # Stats
        self.trips_completed = 0
        self.turns_made = 0
        
        self.decide_next_action()
    
    def decide_next_action(self):
        """Decide next action at intersection"""
        # More likely to go straight
        choices = ['straight'] * 7 + ['left'] * 2 + ['right'] * 1
        self.next_action = random.choice(choices)
        
        if self.next_action == 'left':
            self.blinker = 'left'
        elif self.next_action == 'right':
            self.blinker = 'right'
        else:
            self.blinker = None
    
    def get_intersection(self):
        """Check which intersection we're at"""
        for intersection in INTERSECTIONS:
            if (intersection['left'] <= self.x <= intersection['right'] and 
                intersection['top'] <= self.y <= intersection['bottom']):
                return intersection
        return None
    
    def detect_vehicle_ahead(self, vehicles):
        """Detect if another car is ahead in same lane"""
        min_distance = None
        
        for other in vehicles:
            if other == self:
                continue
            
            # Check if in same lane
            if self.lane_type == 'horizontal' and other.lane_type == 'horizontal':
                if abs(self.y - other.y) < 30:  # Same horizontal lane
                    if self.direction == 'east' and other.x > self.x:
                        distance = other.x - self.x
                        if min_distance is None or distance < min_distance:
                            min_distance = distance
                    elif self.direction == 'west' and other.x < self.x:
                        distance = self.x - other.x
                        if min_distance is None or distance < min_distance:
                            min_distance = distance
            
            elif self.lane_type == 'vertical' and other.lane_type == 'vertical':
                if abs(self.x - other.x) < 30:  # Same vertical lane
                    if self.direction == 'south' and other.y > self.y:
                        distance = other.y - self.y
                        if min_distance is None or distance < min_distance:
                            min_distance = distance
                    elif self.direction == 'north' and other.y < self.y:
                        distance = self.y - other.y
                        if min_distance is None or distance < min_distance:
                            min_distance = distance
        
        return min_distance
    
    def check_traffic_light(self, lights):
        """Check if we need to stop for red light"""
        intersection = self.get_intersection()
        if not intersection:
            return False
        
        for light in lights:
            if light.state in ['red', 'yellow']:
                # Check if light is ahead of us
                if self.direction == 'east' and abs(light.y - self.y) < 50:
                    if light.x > self.x and light.x - self.x < self.stop_distance:
                        return True
                elif self.direction == 'west' and abs(light.y - self.y) < 50:
                    if light.x < self.x and self.x - light.x < self.stop_distance:
                        return True
                elif self.direction == 'south' and abs(light.x - self.x) < 50:
                    if light.y > self.y and light.y - self.y < self.stop_distance:
                        return True
                elif self.direction == 'north' and abs(light.x - self.x) < 50:
                    if light.y < self.y and self.y - light.y < self.stop_distance:
                        return True
        
        return False
    
    def execute_turn_in_intersection(self):
        """Execute turn when in intersection"""
        intersection = self.intersection_entered
        if not intersection:
            return
        
        center_x = intersection['x']
        center_y = intersection['y']
        
        # Move toward center first
        if self.next_action == 'straight':
            # Just keep going straight
            pass
        
        elif self.next_action == 'left':
            # Execute left turn
            if self.direction == 'east':
                # Turn to go north
                if self.x >= center_x - 20:
                    self.lane_type = 'vertical'
                    self.direction = 'north'
                    self.lane_x = VERTICAL_LANES['left_up']
                    self.x = self.lane_x
                    self.lane_y = None
                    self.in_intersection = False
                    self.turns_made += 1
                    self.decide_next_action()
            
            elif self.direction == 'west':
                # Turn to go south
                if self.x <= center_x + 20:
                    self.lane_type = 'vertical'
                    self.direction = 'south'
                    self.lane_x = VERTICAL_LANES['right_down']
                    self.x = self.lane_x
                    self.lane_y = None
                    self.in_intersection = False
                    self.turns_made += 1
                    self.decide_next_action()
            
            elif self.direction == 'south':
                # Turn to go east
                if self.y >= center_y - 20:
                    self.lane_type = 'horizontal'
                    self.direction = 'east'
                    self.lane_y = HORIZONTAL_LANES['bottom']
                    self.y = self.lane_y
                    self.lane_x = None
                    self.in_intersection = False
                    self.turns_made += 1
                    self.decide_next_action()
            
            elif self.direction == 'north':
                # Turn to go west
                if self.y <= center_y + 20:
                    self.lane_type = 'horizontal'
                    self.direction = 'west'
                    self.lane_y = HORIZONTAL_LANES['top']
                    self.y = self.lane_y
                    self.lane_x = None
                    self.in_intersection = False
                    self.turns_made += 1
                    self.decide_next_action()
        
        elif self.next_action == 'right':
            # Execute right turn
            if self.direction == 'east':
                # Turn to go south
                if self.x >= center_x - 20:
                    self.lane_type = 'vertical'
                    self.direction = 'south'
                    self.lane_x = VERTICAL_LANES['left_down']
                    self.x = self.lane_x
                    self.lane_y = None
                    self.in_intersection = False
                    self.turns_made += 1
                    self.decide_next_action()
            
            elif self.direction == 'west':
                # Turn to go north
                if self.x <= center_x + 20:
                    self.lane_type = 'vertical'
                    self.direction = 'north'
                    self.lane_x = VERTICAL_LANES['right_up']
                    self.x = self.lane_x
                    self.lane_y = None
                    self.in_intersection = False
                    self.turns_made += 1
                    self.decide_next_action()
            
            elif self.direction == 'south':
                # Turn to go west
                if self.y >= center_y - 20:
                    self.lane_type = 'horizontal'
                    self.direction = 'west'
                    self.lane_y = HORIZONTAL_LANES['top']
                    self.y = self.lane_y
                    self.lane_x = None
                    self.in_intersection = False
                    self.turns_made += 1
                    self.decide_next_action()
            
            elif self.direction == 'north':
                # Turn to go east
                if self.y <= center_y + 20:
                    self.lane_type = 'horizontal'
                    self.direction = 'east'
                    self.lane_y = HORIZONTAL_LANES['bottom']
                    self.y = self.lane_y
                    self.lane_x = None
                    self.in_intersection = False
                    self.turns_made += 1
                    self.decide_next_action()
    
    def update(self, vehicles, lights):
        self.blinker_timer += 1
        
        # Check if entering intersection
        current_intersection = self.get_intersection()
        
        if current_intersection and not self.in_intersection:
            # Entering intersection
            self.in_intersection = True
            self.intersection_entered = current_intersection
        
        # Execute turn if in intersection
        if self.in_intersection:
            self.execute_turn_in_intersection()
        
        # Speed control
        should_stop = self.check_traffic_light(lights)
        vehicle_distance = self.detect_vehicle_ahead(vehicles)
        
        self.braking = False
        
        if should_stop:
            if self.speed > 0.5:
                self.speed *= 0.88
                self.braking = True
            else:
                self.speed = 0
        elif vehicle_distance and vehicle_distance < self.safe_distance:
            # Maintain safe distance
            if vehicle_distance < 60:
                self.speed *= 0.85
                self.braking = True
            else:
                target_speed = self.max_speed * (vehicle_distance / self.safe_distance) * 0.8
                if self.speed > target_speed:
                    self.speed *= 0.92
                    self.braking = True
                else:
                    self.speed += self.acceleration * 0.5
        else:
            if self.speed < self.max_speed:
                self.speed += self.acceleration
        
        # Move in current direction - STAY IN LANE
        if self.direction == 'east':
            self.x += self.speed
            if self.lane_y:
                self.y = self.lane_y  # Lock to lane
        elif self.direction == 'west':
            self.x -= self.speed
            if self.lane_y:
                self.y = self.lane_y  # Lock to lane
        elif self.direction == 'south':
            self.y += self.speed
            if self.lane_x:
                self.x = self.lane_x  # Lock to lane
        elif self.direction == 'north':
            self.y -= self.speed
            if self.lane_x:
                self.x = self.lane_x  # Lock to lane
        
        # Respawn if out of bounds
        if self.x < -100 or self.x > WIDTH + 100 or self.y < -100 or self.y > HEIGHT + 100:
            self.trips_completed += 1
            self.respawn()
    
    def respawn(self):
        """Respawn at entry point"""
        spawn_options = [
            {'x': -50, 'y': HORIZONTAL_LANES['bottom'], 'direction': 'east', 'lane_type': 'horizontal'},
            {'x': WIDTH + 50, 'y': HORIZONTAL_LANES['top'], 'direction': 'west', 'lane_type': 'horizontal'},
            {'x': VERTICAL_LANES['left_down'], 'y': -50, 'direction': 'south', 'lane_type': 'vertical'},
            {'x': VERTICAL_LANES['left_up'], 'y': HEIGHT + 50, 'direction': 'north', 'lane_type': 'vertical'},
            {'x': VERTICAL_LANES['right_down'], 'y': -50, 'direction': 'south', 'lane_type': 'vertical'},
            {'x': VERTICAL_LANES['right_up'], 'y': HEIGHT + 50, 'direction': 'north', 'lane_type': 'vertical'},
        ]
        
        spawn = random.choice(spawn_options)
        self.x = spawn['x']
        self.y = spawn['y']
        self.direction = spawn['direction']
        self.lane_type = spawn['lane_type']
        
        if self.lane_type == 'horizontal':
            self.lane_y = self.y
            self.lane_x = None
        else:
            self.lane_x = self.x
            self.lane_y = None
        
        self.speed = 0
        self.in_intersection = False
        self.intersection_entered = None
        self.decide_next_action()
    
    def draw(self, screen):
        # Draw car as rectangle (no rotation, always aligned)
        if self.direction in ['east', 'west']:
            # Horizontal car
            car_rect = pygame.Rect(int(self.x - self.height/2), int(self.y - self.width/2), 
                                  self.height, self.width)
        else:
            # Vertical car
            car_rect = pygame.Rect(int(self.x - self.width/2), int(self.y - self.height/2), 
                                  self.width, self.height)
        
        pygame.draw.rect(screen, self.color, car_rect)
        pygame.draw.rect(screen, COLORS['BLACK'], car_rect, 2)
        
        # Windshield
        if self.direction in ['east', 'west']:
            windshield = pygame.Rect(car_rect.x + car_rect.width//3, car_rect.y + 8, 
                                    car_rect.width//3, car_rect.height - 16)
        else:
            windshield = pygame.Rect(car_rect.x + 8, car_rect.y + car_rect.height//3, 
                                    car_rect.width - 16, car_rect.height//3)
        pygame.draw.rect(screen, (100, 200, 255), windshield)
        
        # Brake lights
        if self.braking:
            if self.direction == 'east':
                pygame.draw.circle(screen, (255, 0, 0), 
                                 (int(car_rect.right - 5), int(car_rect.top + 8)), 4)
                pygame.draw.circle(screen, (255, 0, 0), 
                                 (int(car_rect.right - 5), int(car_rect.bottom - 8)), 4)
            elif self.direction == 'west':
                pygame.draw.circle(screen, (255, 0, 0), 
                                 (int(car_rect.left + 5), int(car_rect.top + 8)), 4)
                pygame.draw.circle(screen, (255, 0, 0), 
                                 (int(car_rect.left + 5), int(car_rect.bottom - 8)), 4)
            elif self.direction == 'south':
                pygame.draw.circle(screen, (255, 0, 0), 
                                 (int(car_rect.left + 8), int(car_rect.bottom - 5)), 4)
                pygame.draw.circle(screen, (255, 0, 0), 
                                 (int(car_rect.right - 8), int(car_rect.bottom - 5)), 4)
            elif self.direction == 'north':
                pygame.draw.circle(screen, (255, 0, 0), 
                                 (int(car_rect.left + 8), int(car_rect.top + 5)), 4)
                pygame.draw.circle(screen, (255, 0, 0), 
                                 (int(car_rect.right - 8), int(car_rect.top + 5)), 4)
        
        # Turn signals
        if self.blinker and self.blinker_timer % 30 < 15:
            blinker_color = (255, 165, 0)
            if self.direction == 'east':
                x_pos = car_rect.right - 5 if self.blinker == 'right' else car_rect.left + 5
                pygame.draw.circle(screen, blinker_color, (int(x_pos), int(self.y)), 5)
            elif self.direction == 'west':
                x_pos = car_rect.left + 5 if self.blinker == 'right' else car_rect.right - 5
                pygame.draw.circle(screen, blinker_color, (int(x_pos), int(self.y)), 5)
            elif self.direction == 'south':
                y_pos = car_rect.bottom - 5 if self.blinker == 'right' else car_rect.top + 5
                pygame.draw.circle(screen, blinker_color, (int(self.x), int(y_pos)), 5)
            elif self.direction == 'north':
                y_pos = car_rect.top + 5 if self.blinker == 'right' else car_rect.bottom - 5
                pygame.draw.circle(screen, blinker_color, (int(self.x), int(y_pos)), 5)
        
        # Trip counter
        if self.trips_completed > 0:
            trip_text = tiny_font.render(f'{self.trips_completed}', True, COLORS['GOLD'])
            screen.blit(trip_text, (int(self.x - 8), int(self.y - 50)))


def draw_road(screen):
    """Draw road network"""
    screen.fill(COLORS['GREY'])
    
    # Main horizontal road
    pygame.draw.rect(screen, COLORS['ROAD'], (0, 300, WIDTH, 180))
    
    # Vertical roads
    pygame.draw.rect(screen, COLORS['ROAD'], (400, 0, 100, HEIGHT))
    pygame.draw.rect(screen, COLORS['ROAD'], (700, 0, 100, HEIGHT))
    
    # Center line (yellow dashed) - horizontal
    for x in range(0, WIDTH, 40):
        pygame.draw.rect(screen, COLORS['YELLOW'], (x, 388, 20, 4))
    
    # Center line - vertical
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, COLORS['YELLOW'], (448, y, 4, 20))
        pygame.draw.rect(screen, COLORS['YELLOW'], (748, y, 4, 20))
    
    # Road edges (white)
    pygame.draw.line(screen, COLORS['WHITE'], (0, 305), (WIDTH, 305), 3)
    pygame.draw.line(screen, COLORS['WHITE'], (0, 477), (WIDTH, 477), 3)
    pygame.draw.line(screen, COLORS['WHITE'], (403, 0), (403, HEIGHT), 3)
    pygame.draw.line(screen, COLORS['WHITE'], (497, 0), (497, HEIGHT), 3)
    pygame.draw.line(screen, COLORS['WHITE'], (703, 0), (703, HEIGHT), 3)
    pygame.draw.line(screen, COLORS['WHITE'], (797, 0), (797, HEIGHT), 3)


def draw_minimap(screen, vehicles):
    scale = 0.15
    mm_width = int(WIDTH * scale)
    mm_height = int(HEIGHT * scale)
    mm_x = WIDTH - mm_width - 20
    mm_y = 20
    
    s = pygame.Surface((mm_width, mm_height))
    s.set_alpha(180)
    s.fill((0, 0, 0))
    screen.blit(s, (mm_x, mm_y))
    pygame.draw.rect(screen, COLORS['WHITE'], (mm_x, mm_y, mm_width, mm_height), 2)
    
    pygame.draw.rect(screen, COLORS['ROAD'], 
                    (mm_x, mm_y + int(300 * scale), mm_width, int(180 * scale)))
    pygame.draw.rect(screen, COLORS['ROAD'], 
                    (mm_x + int(400 * scale), mm_y, int(100 * scale), mm_height))
    pygame.draw.rect(screen, COLORS['ROAD'], 
                    (mm_x + int(700 * scale), mm_y, int(100 * scale), mm_height))
    
    for v in vehicles:
        pygame.draw.circle(screen, v.color, 
                         (int(mm_x + v.x * scale), int(mm_y + v.y * scale)), 3)


def draw_hud(screen, vehicles, frame_count):
    s = pygame.Surface((250, 180))
    s.set_alpha(180)
    s.fill((0, 0, 0))
    screen.blit(s, (20, 20))
    
    title = font.render('AI Driving Simulator', True, COLORS['WHITE'])
    screen.blit(title, (30, 30))
    
    total_trips = sum(v.trips_completed for v in vehicles)
    total_turns = sum(v.turns_made for v in vehicles)
    
    stats_text = [
        f'Total Trips: {total_trips}',
        f'Total Turns: {total_turns}',
        f'Active Cars: {len(vehicles)}',
        f'Frame: {frame_count}'
    ]
    
    for i, text in enumerate(stats_text):
        rendered = small_font.render(text, True, COLORS['WHITE'])
        screen.blit(rendered, (30, 60 + i * 22))
    
    y_offset = 150
    for i, v in enumerate(vehicles[:3]):
        stat = tiny_font.render(
            f'{v.personality[0].upper()}: {v.trips_completed} trips, {v.turns_made} turns', 
            True, v.color
        )
        screen.blit(stat, (30, y_offset + i * 18))
    
    s2 = pygame.Surface((200, 100))
    s2.set_alpha(180)
    s2.fill((0, 0, 0))
    screen.blit(s2, (20, HEIGHT - 120))
    
    legends = [
        (COLORS['RED'], 'A - Aggressive'),
        (COLORS['BLUE'], 'D - Adaptive'),
        (COLORS['GREEN'], 'C - Cautious')
    ]
    
    for i, (color, text) in enumerate(legends):
        pygame.draw.rect(screen, color, (30, HEIGHT - 105 + i * 25, 15, 15))
        rendered = small_font.render(text, True, COLORS['WHITE'])
        screen.blit(rendered, (50, HEIGHT - 105 + i * 25))


def main():
    lights = [
        TrafficLight(420, 320, 'west'),
        TrafficLight(480, 320, 'east'),
        TrafficLight(720, 320, 'west'),
        TrafficLight(780, 320, 'east'),
    ]
    
    vehicles = [
        Vehicle(-50, HORIZONTAL_LANES['bottom'], COLORS['RED'], 'aggressive', 'horizontal', 'east'),
        Vehicle(WIDTH + 50, HORIZONTAL_LANES['top'], COLORS['BLUE'], 'adaptive', 'horizontal', 'west'),
        Vehicle(VERTICAL_LANES['left_down'], -50, COLORS['GREEN'], 'cautious', 'vertical', 'south'),
        Vehicle(VERTICAL_LANES['right_up'], HEIGHT + 50, COLORS['PURPLE'], 'adaptive', 'vertical', 'north'),
        Vehicle(VERTICAL_LANES['right_down'], -50, COLORS['ORANGE'], 'aggressive', 'vertical', 'south'),
        Vehicle(-50, HORIZONTAL_LANES['bottom'], COLORS['PURPLE'], 'adaptive', 'horizontal', 'east'),
    ]
    
    frame_count = 0
    running = True
    paused = False
    
    print("🚗 AI Self-Driving Car Simulator")
    print("Controls: SPACE=Pause, ESC=Quit")
    print("Cars stay in lanes and never overlap!")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        if not paused:
            for light in lights:
                light.update()
            
            for vehicle in vehicles:
                vehicle.update(vehicles, lights)
            
            frame_count += 1
        
        draw_road(screen)
        
        for light in lights:
            light.draw(screen)
        
        for vehicle in vehicles:
            vehicle.draw(screen)
        
        draw_minimap(screen, vehicles)
        draw_hud(screen, vehicles, frame_count)
        
        if paused:
            pause_text = font.render('PAUSED - Press SPACE', True, COLORS['WHITE'])
            text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            s = pygame.Surface(text_rect.inflate(40, 20).size)
            s.set_alpha(200)
            s.fill((0, 0, 0))
            screen.blit(s, text_rect.inflate(40, 20))
            screen.blit(pause_text, text_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    print("\n📊 Final Statistics:")
    for v in vehicles:
        print(f"  {v.personality.capitalize()}: {v.trips_completed} trips, {v.turns_made} turns")
    
    pygame.quit()


if __name__ == '__main__':
    main()

# %%


# %%



