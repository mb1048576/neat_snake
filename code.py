# imports
import pygame
import random
import neat
import numpy as np
import pickle

##############
# Defining colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
dark_green = (0, 100, 0)

# Choice of colors
grid_color = white
background_color = green
food_color = red
snake_color = black
head_color = black


lato = 50
bordo = 80
number_of_squares = 20

pygame.init()
screen = pygame.display.set_mode((2 * bordo + number_of_squares * lato, 2 * bordo + number_of_squares * lato))
schermo_di_gioco = pygame.Rect(bordo, bordo, number_of_squares * lato, number_of_squares * lato)
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 32)

grid_bool = False
directions = {0:(0, -1), 1:(0, 1), 2:(-1, 0), 3:(1, 0)}



class Snake:
    def __init__(self, index):
        self.list = [pygame.Rect(bordo + lato + 1, bordo + lato * 2 + 1, lato - 2, lato - 2),
                     pygame.Rect(bordo + lato * 2 + 1, bordo + lato * 2 + 1, lato - 2, lato - 2)]
        self.head = pygame.Rect(bordo + lato * 3 + 1, bordo + lato * 2 + 1, lato - 2, lato - 2)
        self.score = 0
        self.direction = 3
        self.color = snake_color
        self.head_color = head_color
        self.wall_distance_list = [self.head.y, lato * number_of_squares - self.head.y - lato, self.head.x, lato * number_of_squares - self.head.x - lato]
        self.tail_distance_list = []
        self.food_position_list = []
        self.food_distance_list = [0, 0]
        self.time = 0
        self.tracking_score = -1
        self.number_of_turns = 0
        self.got_closer = True
        self.index = index
    def draw(self):
        for i in self.list:
            pygame.draw.rect(screen, self.color, i)
        pygame.draw.rect(screen, self.color, self.head)
        return
    def update(self):
        self.wall_distance_list = [(self.head.y - bordo) // lato, 0, (self.head.x - bordo) // lato, 0]
        self.wall_distance_list[1] = number_of_squares - 1 - self.wall_distance_list[0]
        self.wall_distance_list[3] = number_of_squares - 1 - self.wall_distance_list[2]
        distance_tail_north = 0
        distance_tail_south = 0
        distance_tail_west = 0
        distance_tail_east = 0
        for r in self.list:
            if r.x == self.head.x and r.y > self.head.y:
                distance_tail_north = number_of_squares - min(number_of_squares  - distance_tail_north, (r.y - self.head.y) // lato)
            elif r.x == self.head.x:
                distance_tail_south = number_of_squares - min(number_of_squares - distance_tail_south, (self.head.y - r.y) // lato)
            elif r.x < self.head.x and r.y == self.head.y:
                distance_tail_west = number_of_squares - min(number_of_squares - distance_tail_west, (self.head.x - r.x) // lato)
            elif r.y == self.head.y:
                distance_tail_east = number_of_squares - min(number_of_squares - distance_tail_east, (r.x - self.head.x) // lato)
        self.tail_distance_list = [distance_tail_north, distance_tail_south, distance_tail_west, distance_tail_east]

    def update_food(self, food):
        self.food_position_list = [0, 0, 0, 0]
        x = food.rectangle.x
        y = food.rectangle.y
        if self.head.y > y:
            self.food_position_list[0] = 1
        elif self.head.y < y:
            self.food_position_list[1] = 1
        if self.head.x > x:
            self.food_position_list[2] = 1
        elif self.head.x < x:
            self.food_position_list[3] = 1
        self.got_closer = abs(y - self.head.y) // lato < self.food_distance_list[0] or abs(x - self.head.x) // lato < self.food_distance_list[1]
        self.food_distance_list = [abs(y - self.head.y) // lato, abs(x - self.head.x) // lato]

    def move(self):
        self.list.pop(0)
        x = self.head.x
        y = self.head.y
        self.list.append(pygame.Rect(x, y, lato - 2, lato - 2))
        self.head.x += directions[self.direction][0] * lato
        self.head.y += directions[self.direction][1] * lato
        return

    def eat(self, g):
        return pygame.Rect.colliderect(self.head, g)

    def grow(self):
        x = self.head.x
        y = self.head.y
        self.list.append(pygame.Rect(x, y, lato - 2, lato - 2))
        self.head.x += directions[self.direction][0] * lato
        self.head.y += directions[self.direction][1] * lato


    def self_eating(self):
        x = 0
        for i in self.list:
            if pygame.Rect.colliderect(i, self.head):
                x += 1
        return x > 0

    def inside(self):
        return bordo <= self.head.x <= bordo + number_of_squares * lato and bordo <= self.head.y <= bordo + number_of_squares * lato

    def check(self):
        pass

    def check_stalling(self):
        return self.number_of_turns > self.score * 2 + 20



class Food:
    def __init__(self):
        self.colour = food_color
        self.value = 10
        self.radius = lato//2
        self.center = (random.randint(0, number_of_squares - 1) * lato + bordo + lato // 2,
                       random.randint(0, number_of_squares - 1) * lato + bordo + lato // 2)
        self.rectangle = pygame.Rect(self.center[0] - lato // 2 + 1, self.center[1] - lato // 2 + 1,
                                     lato - number_of_squares + 2, lato - number_of_squares + 2)
        self.list = [0 for _ in range(number_of_squares * 2)]
        self.list[(self.rectangle.x - bordo) // lato] = 20
        self.list[(self.rectangle.y - bordo) // lato + number_of_squares] = 20

    def new(self):
        self.center = (random.randint(1, number_of_squares - 2) * lato + bordo + lato//2, random.randint(1, number_of_squares - 2) * lato + bordo + lato//2)
        self.rectangle = pygame.Rect(self.center[0] - lato//2 + 1, self.center[1] - lato //2 + 1, lato - number_of_squares + 2, lato - number_of_squares + 2)

    def check(self):
        pass
    def draw(self):
        pygame.draw.circle(screen, self.colour, self.center, self.radius, 0)



def draw_screen(snakes, food_list, frame_rate, genomes):
    screen.fill(black)
    if snakes and snakes[0].score >= 0:
        text = font.render(f"Score {snakes[0].score} Fitness {round(genomes[snakes[0].index][1].fitness, 3)}", True, white, black)
        text_rect = text.get_rect()
        text_rect.center = (bordo + number_of_squares * lato // 2, bordo//2)
        screen.blit(text, text_rect)
    pygame.draw.rect(screen, background_color, schermo_di_gioco)
    clock.tick(frame_rate)
    if grid_bool:
        for i in range(0, number_of_squares + 1):
            pygame.draw.line(screen, grid_color, (bordo, bordo + lato * i), (bordo + number_of_squares * lato, bordo + lato*i))
            pygame.draw.line(screen, grid_color, (bordo + lato * i, bordo), (bordo + lato * i, bordo + number_of_squares * lato))
    if snakes:
        snakes[0].draw()
        food_list[0].draw()
        food_list[0].check()
    pygame.display.flip()

frame_rate = 1000

def main(genomes, config_file):
    global frame_rate
    snakes = []
    food_list = []
    nn_list = []
    #genome_list = []
    count = 0
    for _, g in genomes:
        nn = neat.nn.FeedForwardNetwork.create(g, config_file)
        nn_list.append(nn)
        snakes.append(Snake(count))
        food_list.append(Food())
        g.fitness = 0
        #genome_list.append(g)
        count += 1
    running = True
    while running:
        draw_screen(snakes, food_list, frame_rate, genomes)
        for index, snake in enumerate(snakes):
            if snake.eat(food_list[index].rectangle):
                snake.score += food_list[index].value
                food_list[index].new()
                snake.grow()
                genomes[snake.index][1].fitness += 1
            snake.move()
            if not snake.inside() or snake.self_eating():
                snakes.pop(index)
                food_list.pop(index)
                #genome_list[index].fitness -= 0.1
                #genome_list.pop(index)
                nn_list.pop(index)

            elif snake.check_stalling():
                #print(1)
                snakes.pop(index)
                food_list.pop(index)
                #genome_list[index].fitness -= 0.2
                #genome_list.pop(index)
                nn_list.pop(index)

            else:
                snake.update()
                snake.update_food(food_list[index])
                if snake.got_closer:
                    genomes[snake.index][1].fitness += 0.001
                    pass
                else:
                    genomes[snake.index][1].fitness -= 0.001
                    pass
                output = nn_list[index].activate(snake.wall_distance_list + snake.tail_distance_list + snake.food_position_list + snake.food_distance_list + [snake.direction])
                new_direction = int(np.array(output).argmax())
                if (snake.direction + new_direction)%4 == 1:
                    #snakes.pop(index)
                    #food_list.pop(index)
                    #genome_list[index].fitness -= 0.1
                    #genome_list.pop(index)
                    #nn_list.pop(index)
                    pass
                elif snake.direction != new_direction:
                    snake.number_of_turns += 1
                    genomes[snake.index][1].fitness -= 0.01
                    snake.direction = new_direction

        if len(snakes) == 0:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT or event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    quit()
                if event.key == pygame.K_k:
                    snakes = []
                    food_list = []
                    genome_list = []
                    nn_list = []
                if event.key == pygame.K_s:
                    if frame_rate == 20:
                        frame_rate = 1000
                    else:
                        frame_rate = 20


# Load configuration
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config.txt')

# Create population
p = neat.Population(config)
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)

winner = p.run(main, 1000)
with open('winner.pkl', 'wb') as f:
    pickle.dump(winner, f)


pygame.quit()
