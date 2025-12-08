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

# Define lanes for realistic driving
HORIZONTAL_LANES = {
    'top': 350,
    'bottom': 430
}

VERTICAL_LANES = {
    'left_left': 425,
    'left_right': 475,
    'right_left': 725,
    'right_right': 775
}

# Intersection centers
INTERSECTIONS = [
    {'x': 450, 'y': 390},
    {'x': 750, 'y': 390}
]


class TrafficLight:
    """Traffic light with cycling states"""
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # 'north', 'south', 'east', 'west'
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
    """Realistic car with lane-based driving"""
    def __init__(self, x, y, color, personality, initial_direction):
        self.x = x
        self.y = y
        self.color = color
        self.width = 35
        self.height = 60
        self.speed = 0
        self.personality = personality
        self.direction = initial_direction  # 'north', 'south', 'east', 'west'
        
        # Set initial angle based on direction
        angle_map = {'east': 0, 'south': math.pi/2, 'west': math.pi, 'north': -math.pi/2}
        self.angle = angle_map[initial_direction]
        
        # Personality parameters
        if personality == 'aggressive':
            self.max_speed = 5
            self.acceleration = 0.15
            self.stop_distance = 60
        elif personality == 'cautious':
            self.max_speed = 3
            self.acceleration = 0.08
            self.stop_distance = 90
        else:  # adaptive
            self.max_speed = 4
            self.acceleration = 0.1
            self.stop_distance = 75
        
        self.braking = False
        self.blinker = None
        self.blinker_timer = 0
        
        # Navigation
        self.current_lane = self.get_current_lane()
        self.next_action = None  # 'straight', 'left', 'right'
        self.at_intersection = False
        self.turning = False
        self.turn_progress = 0
        
        # Stats
        self.trips_completed = 0
        self.turns_made = 0
        
        # Decide next action at start
        self.decide_next_action()
    
    def get_current_lane(self):
        """Determine which lane the car is in"""
        if 340 <= self.y <= 360:
            return 'horizontal_top'
        elif 420 <= self.y <= 440:
            return 'horizontal_bottom'
        elif 420 <= self.x <= 440:
            return 'vertical_left_left'
        elif 470 <= self.x <= 490:
            return 'vertical_left_right'
        elif 720 <= self.x <= 740:
            return 'vertical_right_left'
        elif 770 <= self.x <= 790:
            return 'vertical_right_right'
        return 'unknown'
    
    def decide_next_action(self):
        """Decide whether to go straight, turn left, or turn right"""
        choices = ['straight', 'straight', 'straight', 'left', 'right']  # Bias towards going straight
        self.next_action = random.choice(choices)
        
        if self.next_action == 'left':
            self.blinker = 'left'
        elif self.next_action == 'right':
            self.blinker = 'right'
    
    def is_at_intersection(self):
        """Check if car is at an intersection"""
        for intersection in INTERSECTIONS:
            dx = abs(self.x - intersection['x'])
            dy = abs(self.y - intersection['y'])
            if dx < 100 and dy < 100:
                return True
        return False
    
    def detect_nearby_vehicle(self, vehicles):
        """Detect vehicle ahead"""
        for other in vehicles:
            if other == self:
                continue
            
            dx = other.x - self.x
            dy = other.y - self.y
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < 120:
                angle_to_vehicle = math.atan2(dy, dx)
                angle_diff = abs((angle_to_vehicle - self.angle) % (2 * math.pi))
                
                if angle_diff < math.pi / 4 or angle_diff > 7 * math.pi / 4:
                    return distance
        return None
    
    def check_traffic_light(self, lights):
        """Check if we need to stop for traffic light"""
        if not self.is_at_intersection():
            return False
            
        for light in lights:
            if light.state in ['red', 'yellow']:
                dx = self.x - light.x
                dy = self.y - light.y
                distance = math.sqrt(dx * dx + dy * dy)
                
                # Check if light is relevant to our direction
                if distance < 100:
                    angle_to_light = math.atan2(dy, dx)
                    # Light should be ahead (opposite direction)
                    angle_diff = abs((angle_to_light - self.angle + math.pi) % (2 * math.pi))
                    
                    if distance < self.stop_distance and angle_diff < math.pi / 3:
                        return True
        return False
    
    def execute_turn(self):
        """Execute the turn smoothly"""
        if not self.turning:
            return
        
        self.turn_progress += 0.05
        
        if self.turn_progress >= 1.0:
            # Turn complete
            self.turning = False
            self.turn_progress = 0
            self.blinker = None
            self.turns_made += 1
            
            # Update direction after turn
            if self.next_action == 'left':
                direction_map = {'north': 'west', 'west': 'south', 'south': 'east', 'east': 'north'}
                self.direction = direction_map[self.direction]
            elif self.next_action == 'right':
                direction_map = {'north': 'east', 'east': 'south', 'south': 'west', 'west': 'north'}
                self.direction = direction_map[self.direction]
            
            # Decide next action
            self.decide_next_action()
        else:
            # Smooth turn
            if self.next_action == 'left':
                self.angle -= math.pi / 2 * 0.05
            elif self.next_action == 'right':
                self.angle += math.pi / 2 * 0.05
    
    def update(self, vehicles, lights):
        self.blinker_timer += 1
        
        # Check if at intersection
        currently_at_intersection = self.is_at_intersection()
        
        # Start turn when at intersection center
        if currently_at_intersection and not self.at_intersection and not self.turning:
            if self.next_action in ['left', 'right']:
                # Check if we can turn (no red light)
                if not self.check_traffic_light(lights):
                    self.turning = True
            self.at_intersection = True
        
        if not currently_at_intersection:
            self.at_intersection = False
        
        # Execute turn if turning
        if self.turning:
            self.execute_turn()
        
        # Speed control
        should_stop = self.check_traffic_light(lights)
        vehicle_distance = self.detect_nearby_vehicle(vehicles)
        
        self.braking = False
        
        if should_stop:
            self.speed *= 0.85
            self.braking = True
        elif vehicle_distance and vehicle_distance < 100:
            target_speed = max(0, self.max_speed * (vehicle_distance / 100) * 0.6)
            if self.speed > target_speed:
                self.speed *= 0.90
                self.braking = True
            else:
                self.speed += self.acceleration * 0.3
        else:
            if self.speed < self.max_speed:
                self.speed += self.acceleration
        
        # Move forward
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Keep in bounds and respawn if out
        if self.x < -50 or self.x > WIDTH + 50 or self.y < -50 or self.y > HEIGHT + 50:
            self.trips_completed += 1
            self.respawn()
    
    def respawn(self):
        """Respawn car at a random entry point"""
        spawn_points = [
            # Coming from left (going east)
            {'x': 50, 'y': HORIZONTAL_LANES['top'], 'direction': 'east'},
            # Coming from right (going west)
            {'x': WIDTH - 50, 'y': HORIZONTAL_LANES['bottom'], 'direction': 'west'},
            # Coming from top (going south)
            {'x': VERTICAL_LANES['left_left'], 'y': 50, 'direction': 'south'},
            {'x': VERTICAL_LANES['right_left'], 'y': 50, 'direction': 'south'},
            # Coming from bottom (going north)
            {'x': VERTICAL_LANES['left_right'], 'y': HEIGHT - 50, 'direction': 'north'},
            {'x': VERTICAL_LANES['right_right'], 'y': HEIGHT - 50, 'direction': 'north'},
        ]
        
        spawn = random.choice(spawn_points)
        self.x = spawn['x']
        self.y = spawn['y']
        self.direction = spawn['direction']
        
        angle_map = {'east': 0, 'south': math.pi/2, 'west': math.pi, 'north': -math.pi/2}
        self.angle = angle_map[self.direction]
        
        self.speed = 0
        self.turning = False
        self.turn_progress = 0
        self.at_intersection = False
        self.decide_next_action()
    
    def draw(self, screen):
        car_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
        
        # Car body
        rect = pygame.Rect(10, 10, self.width, self.height)
        pygame.draw.rect(car_surface, self.color, rect)
        pygame.draw.rect(car_surface, COLORS['BLACK'], rect, 2)
        
        # Windshield
        windshield_rect = pygame.Rect(self.width // 4 + 10, self.height // 4 + 10, 
                                      self.width // 2, self.height // 4)
        pygame.draw.rect(car_surface, (100, 200, 255, 128), windshield_rect)
        
        # Brake lights
        if self.braking:
            pygame.draw.circle(car_surface, (255, 0, 0), (15, self.height + 5), 4)
            pygame.draw.circle(car_surface, (255, 0, 0), (self.width + 5, self.height + 5), 4)
        
        # Turn signals
        if self.blinker and self.blinker_timer % 30 < 15:
            blinker_color = (255, 165, 0)
            if self.blinker == 'left':
                pygame.draw.circle(car_surface, blinker_color, (12, 15), 5)
            elif self.blinker == 'right':
                pygame.draw.circle(car_surface, blinker_color, (self.width + 8, 15), 5)
        
        # Rotate and draw
        rotated_surface = pygame.transform.rotate(car_surface, -math.degrees(self.angle))
        rotated_rect = rotated_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_surface, rotated_rect)
        
        # Trip counter
        if self.trips_completed > 0:
            trip_text = tiny_font.render(f'🏁{self.trips_completed}', True, COLORS['GOLD'])
            screen.blit(trip_text, (int(self.x - 15), int(self.y - 45)))


def draw_road(screen):
    """Draw realistic road network"""
    screen.fill(COLORS['GREY'])
    
    # Main horizontal road
    pygame.draw.rect(screen, COLORS['ROAD'], (0, 300, WIDTH, 180))
    
    # Vertical roads
    pygame.draw.rect(screen, COLORS['ROAD'], (400, 0, 100, HEIGHT))
    pygame.draw.rect(screen, COLORS['ROAD'], (700, 0, 100, HEIGHT))
    
    # Center line (yellow) - horizontal
    for x in range(0, WIDTH, 40):
        pygame.draw.rect(screen, COLORS['YELLOW'], (x, 388, 20, 4))
    
    # Center line - vertical left
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, COLORS['YELLOW'], (448, y, 4, 20))
    
    # Center line - vertical right
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, COLORS['YELLOW'], (748, y, 4, 20))
    
    # Road edges (white)
    pygame.draw.rect(screen, COLORS['WHITE'], (0, 305, WIDTH, 3))
    pygame.draw.rect(screen, COLORS['WHITE'], (0, 477, WIDTH, 3))
    pygame.draw.rect(screen, COLORS['WHITE'], (403, 0, 3, HEIGHT))
    pygame.draw.rect(screen, COLORS['WHITE'], (497, 0, 3, HEIGHT))
    pygame.draw.rect(screen, COLORS['WHITE'], (703, 0, 3, HEIGHT))
    pygame.draw.rect(screen, COLORS['WHITE'], (797, 0, 3, HEIGHT))


def draw_minimap(screen, vehicles):
    """Draw minimap"""
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
    
    # Roads
    pygame.draw.rect(screen, COLORS['ROAD'], 
                    (mm_x, mm_y + int(300 * scale), mm_width, int(180 * scale)))
    pygame.draw.rect(screen, COLORS['ROAD'], 
                    (mm_x + int(400 * scale), mm_y, int(100 * scale), mm_height))
    pygame.draw.rect(screen, COLORS['ROAD'], 
                    (mm_x + int(700 * scale), mm_y, int(100 * scale), mm_height))
    
    # Vehicles
    for v in vehicles:
        pygame.draw.circle(screen, v.color, 
                         (int(mm_x + v.x * scale), int(mm_y + v.y * scale)), 3)


def draw_hud(screen, vehicles, frame_count):
    """Draw HUD"""
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
    
    # Legend
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


def run():
    """Main run function for the simulator"""
    # Initialize traffic lights
    lights = [
        TrafficLight(420, 320, 'west'),
        TrafficLight(480, 320, 'east'),
        TrafficLight(720, 320, 'west'),
        TrafficLight(780, 320, 'east'),
    ]
    
    # Initialize vehicles with realistic starting positions
    vehicles = [
        Vehicle(100, HORIZONTAL_LANES['top'], COLORS['RED'], 'aggressive', 'east'),
        Vehicle(WIDTH - 100, HORIZONTAL_LANES['bottom'], COLORS['BLUE'], 'adaptive', 'west'),
        Vehicle(VERTICAL_LANES['left_left'], 100, COLORS['GREEN'], 'cautious', 'south'),
        Vehicle(VERTICAL_LANES['right_right'], HEIGHT - 100, COLORS['PURPLE'], 'adaptive', 'north'),
        Vehicle(VERTICAL_LANES['right_left'], 100, COLORS['ORANGE'], 'aggressive', 'south'),
    ]
    
    frame_count = 0
    running = True
    paused = False
    
    print("🚗 AI Self-Driving Car Simulator")
    print("Controls: SPACE=Pause, ESC=Quit")
    print("Watch cars drive realistically with proper turns!")
    
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
    run()

# %%



