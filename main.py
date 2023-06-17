from consts import *
from screen import Screen

import pygame


def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    
    screen = Screen(win)
    
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            elif event.type == pygame.KEYDOWN:
                screen.handle_key_down(event)
            
            elif event.type == pygame.KEYUP:
                screen.handle_key_up(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                screen.handle_mouse_down(event)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                screen.handle_mouse_up(event)

        screen.update()
        screen.draw()


if __name__ == "__main__":
    main()