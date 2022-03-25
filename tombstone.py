import pygame


class Tombstone(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/tomb.png")
        self.rect = self.image.get_rect()
        self.scroll_speed = 4
        self.gap = 120
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(self.gap)]
        if position == -1:
            self.rect.topleft = [x, y + int(self.gap)]

    def update(self):
        self.rect.x -= self.scroll_speed/2
        if self.rect.right < 0:
            self.kill()
