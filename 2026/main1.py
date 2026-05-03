import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60
RED_DUST = (193, 68, 14)
SKY_COLOR = (45, 20, 20)
PLATFORM_COLOR = (100, 50, 30) 
WHITE = (255, 255, 255)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.8
        self.jump_power = -16
        self.platforms = platforms 

    def update(self):
        # 1. Гравітація
        self.speed_y += self.gravity
        self.rect.y += self.speed_y
        
        # 2. Перевірка зіткнень по вертикалі (Y)
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        if hits:
            # Якщо ми падаємо вниз на платформу
            if self.speed_y > 0:
                self.rect.bottom = hits[0].rect.top
                self.speed_y = 0
            # Якщо ми вдарилися головою об платформу знизу
            elif self.speed_y < 0:
                self.rect.top = hits[0].rect.bottom
                self.speed_y = 0

        # 3. Керування по осі X
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -7
        if keys[pygame.K_RIGHT]:
            self.speed_x = 7
        self.rect.x += self.speed_x

        # Обмеження екрану (підлога та стіни)
        if self.rect.bottom > HEIGHT - 20:
            self.rect.bottom = HEIGHT - 20
            self.speed_y = 0
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH

    def jump(self):
        # Перевіряємо, чи стоїть гравець на чомусь перед стрибком
        self.rect.y += 1 # Тимчасово опускаємо на 1 піксель для перевірки
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 1
        
        if hits or self.rect.bottom >= HEIGHT - 20:
            self.speed_y = self.jump_power

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

p1 = Platform(500, 450, 200, 30)
p2 = Platform(200, 350, 150, 30)
p3 = Platform(450, 250, 100, 30)
p4 = Platform(100, 150, 200, 30)

platforms.add(p1, p2, p3, p4)
all_sprites.add(p1, p2, p3, p4)

player = Player(platforms)
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_UP]:
                player.jump()

    all_sprites.update()

    screen.fill(SKY_COLOR)
    pygame.draw.rect(screen, RED_DUST, (0, HEIGHT - 20, WIDTH, 20))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()