import pygame


class Witch(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.game_over = False
        self.flying = False
        for num in range(1, 4):
            img = pygame.image.load(f"images/witch{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if self.flying:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 770:
                self.rect.y += int(self.vel)

        if not self.game_over:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #  handle the animation
            self.counter += 1
            animation_cooldown = 10

            if self.counter > animation_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # tilt the witch
            self.image = pygame.transform.rotate(self.images[self.index], -self.vel)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
