import pygame
import random


class SnakePart:
    def __init__(self, cordinate=(140, 140), specials=False):
        self.coordinates = cordinate
        self.specials = specials

    def update_coordinates(self, cordinate):
        if type(cordinate) == tuple:
            if len(cordinate) == 2:
                self.coordinates = cordinate
        else:
            raise ValueError('coordinate is invalid')

    def get_y(self):
        return self.coordinates[1]

    def get_x(self):
        return self.coordinates[0]

    def get_coordinates(self):
        return self.coordinates

    def copy(self):
        return SnakePart(self.coordinates, self.specials)


class Food(SnakePart):
    def generate(self, lst=None):
        if lst is None:
            lst = []
        while self.coordinates in lst:
            self.coordinates = random.randrange(0, 700, 35), random.randrange(0, 700, 35)


class App:

    def __init__(self):
        self.running = False
        self.running2 = True
        self.clock = None
        self.rendered = False
        self.moving = 'r'
        self.snake = []
        self.food = None
        self.lengthen = False
        self.screen = None

    def run(self):
        self.init()
        running = True
        self.update()
        self.render()
        str = pygame.image.load('start.png')
        self.screen.blit(str, (100, 250))
        pygame.display.update()

        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = quit()
                if e.type == pygame.KEYDOWN:
                    if e.key != pygame.K_a and e.key != pygame.K_w and e.key != pygame.K_s and e.key != pygame.K_d and e.key != pygame.K_LEFT and e.key != pygame.K_UP and e.key != pygame.K_DOWN and e.key != pygame.K_RIGHT:
                        running = False
        while self.running:
            self.update()
            self.collisions()
            self.render()
            self.clock.tick(3)
        self.cleanUp()
        pygame.time.delay(1000)

        while self.running2:
            self.ending_screen()

    def init(self):
        self.screen = pygame.display.set_mode((700, 700))
        pygame.display.set_caption("nimo's snake")
        pygame.mixer.init()

        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play()

        for i in range(5):
            if i == 4:
                self.snake.append(SnakePart((350, i * 35), True))
            else:
                self.snake.append(SnakePart((350, i * 35)))

        self.snake.reverse()

        self.food = Food()
        self.food.generate()

        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.events()
        chngX = 0
        chngY = 0

        if self.moving == 'r' :
            chngY = 35
        elif self.moving == 'l' :
            chngY = -35
        elif self.moving == 'd':
            chngX = 35
        else:
            chngX = -35

        self.snake.insert(0, self.snake[0].copy())
        self.snake[0].update_coordinates((self.snake[0].get_x() + chngX, self.snake[0].get_y() + chngY))
        self.snake[1].specials = False
        self.snake[0].specials = True
        if not self.lengthen:
            self.snake.pop(len(self.snake) - 1)
        self.lengthen = False

    def collisions(self):
        hd = self.snake[0].get_coordinates()
        if hd[0] < 0 or hd[0] > 700:
            self.running = False
        if hd[1] < 0 or hd[1] > 700:
            self.running = False

        copy = self.map_to_coordinates()

        if hd == self.food.get_coordinates():
            pygame.mixer.Sound('eat.mp3').play()
            self.lengthen = True
            self.food.generate(copy)

        copy.pop(0)
        if hd in copy:
            self.running = False

    def map_to_coordinates(self):
        return list(map(lambda x: x.get_coordinates(), self.snake.copy()))

    def cleanUp(self):
        self.screen.fill((245, 251, 250))
        self.init()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if self.rendered:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.moving != 'r':
                            self.rendered = False
                            self.moving = 'l'

                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.moving != 'l':
                            self.rendered = False
                            self.moving = 'r'

                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.moving != 'd':
                            self.rendered = False
                            self.moving = 'u'

                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if self.moving != 'u':
                            self.rendered = False
                            self.moving = 'd'

    def render(self):
        head = pygame.image.load('head.png')
        body = pygame.image.load('body.png')
        apple = pygame.image.load('fishera.png')
        wall = pygame.transform.scale(pygame.image.load('background.jpg'), (700, 750))

        self.screen.blit(wall, (0, 0))

        hd = None
        for i in self.snake:
            if not i.specials:
                self.screen.blit(body, (i.get_y(), i.get_x()))
            else:
                hd = i

        self.screen.blit(head, (hd.get_y(), hd.get_x()))
        self.screen.blit(apple, (self.food.get_y(), self.food.get_x()))

        pygame.display.update()
        self.rendered = True

    def ending_screen(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(pygame.transform.scale(pygame.image.load('end.png'), (700, 350)), (0, 175))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running2 = False
            if event.type == pygame.KEYDOWN:
                self.running2 = False


if __name__ == "__main__":
    app = App()
    app.run()