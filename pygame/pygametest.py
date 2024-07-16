import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trash Dodge")

# 배경 이미지 로드
background_image = pygame.image.load('trash_malib2.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 시작 화면 이미지 로드
start_image1 = pygame.image.load('1.png')
start_image1 = pygame.transform.scale(start_image1, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_image2 = pygame.image.load('2.png')
start_image2 = pygame.transform.scale(start_image2, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_image3 = pygame.image.load('3.png')
start_image3 = pygame.transform.scale(start_image3, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 종료 화면 이미지 로드
end_image = pygame.image.load('4.png')
end_image = pygame.transform.scale(end_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('ele.png')  # 외부 이미지 로드
        self.image = pygame.transform.scale(self.image, (100, 100))  # 이미지 크기 조정
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 100
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.rect.x += self.speed


class TrashSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = random.randint(5, 10)

        # 속도에 따른 이미지 로드
        if self.speed == 5 or self.speed == 6:
            self.image = pygame.image.load('slow.png')
        elif self.speed == 7 or self.speed == 8:
            self.image = pygame.image.load('medium3.png')
        else:
            self.image = pygame.image.load('fast.png')

        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += self.speed
        global score
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            score += 1


player = PlayerSprite()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

trash_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()
running = True
lives = 3
score = 0

font = pygame.font.Font(None, 36)

last_trash_spawn_time = pygame.time.get_ticks()
initial_trash_spawn_interval = 1000


def show_final_score():
    screen.blit(end_image, (0, 0))
    final_score_font = pygame.font.Font(None, 100)  # 최종 점수 글씨 크기를 72로 설정
    final_score_text = final_score_font.render(f"{score}", True, (255, 255, 255))
    screen.blit(final_score_text, (
        SCREEN_WIDTH // 2 - final_score_text.get_width() // 2 - 100, SCREEN_HEIGHT // 2 - final_score_text.get_height() // 2 - 298))
    pygame.display.flip()
    pygame.time.wait(3000)  # 3초 동안 최종 점수 표시


def show_start_images():
    images = [start_image1, start_image2, start_image3]
    current_image = 0

    while current_image < len(images):
        screen.blit(images[current_image], (0, 0))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    current_image += 1
                    waiting = False


show_start_images()

start_time = pygame.time.get_ticks()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()
    time_elapsed = (current_time - start_time) / 1000  # 경과 시간(초)

    current_interval = initial_trash_spawn_interval / (2 ** (time_elapsed / 10))

    if current_time - last_trash_spawn_time > current_interval:
        new_trash = TrashSprite()
        trash_sprites.add(new_trash)
        all_sprites.add(new_trash)
        last_trash_spawn_time = current_time

    hits = pygame.sprite.spritecollide(player, trash_sprites, True)
    for hit in hits:
        lives -= 1
        if lives == 0:
            show_final_score()
            running = False

    all_sprites.update()

    # 배경 이미지 그리기
    screen.blit(background_image, (0, 0))

    all_sprites.draw(screen)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    lives_text = font.render(f"Lifes: {lives}", True, (255, 0, 0))
    screen.blit(lives_text, (10, 40))

    pygame.display.flip()

pygame.quit()
