import pygame

window = pygame.display.set_mode((512, 512))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()