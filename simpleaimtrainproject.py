# aimproject.py
import pygame
import random
import math
import sys

# Settings
WIDTH, HEIGHT = 800, 600
FPS = 60
SESSION_TIME = 30            
TARGET_RADIUS = 30           
SPAWN_PADDING = 50          
# end settingss

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("aim_traner_s")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 56)

# random spawn 
def random_target_pos():
    x = random.randint(SPAWN_PADDING + TARGET_RADIUS, WIDTH - SPAWN_PADDING - TARGET_RADIUS)
    y = random.randint(SPAWN_PADDING + TARGET_RADIUS, HEIGHT - SPAWN_PADDING - TARGET_RADIUS)
    return x, y

# checking for mx my is in cx cy in r
def is_hit(mx, my, cx, cy, r):
    return (mx - cx)**2 + (my - cy)**2 <= r**2

def draw_text(surf, text, x, y, font, color=(255,255,255)):
    img = font.render(text, True, color)
    surf.blit(img, (x, y))

def main():
    # stat
    hits = 0
    shots = 0
    start_ticks = pygame.time.get_ticks()
    running = True
    game_over = False

    #first target
    target_x, target_y = random_target_pos()

    # target moving
    move_target = False
    target_speed = [0, 0]  # [vx, vy]

    while running:
        dt = clock.tick(FPS) / 1000.0  # delta time in seconds
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000.0
        time_left = max(0, SESSION_TIME - elapsed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    # restart
                    hits = 0
                    shots = 0
                    start_ticks = pygame.time.get_ticks()
                    game_over = False
                    target_x, target_y = random_target_pos()
                if event.key == pygame.K_m:
                    move_target = not move_target
                    if move_target:
                        # random speed
                        target_speed = [random.choice([-150, -100, 100, 150]), random.choice([-120, -80, 80, 120])]

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:  # left click
                    mx, my = event.pos
                    shots += 1
                    if is_hit(mx, my, target_x, target_y, TARGET_RADIUS):
                        hits += 1
                        # spawn other target after target
                        target_x, target_y = random_target_pos()
                        if move_target:
                            # (remember to write after coding)
                            target_speed = [random.choice([-150, -100, 100, 150]), random.choice([-120, -80, 80, 120])]
                    else:
                        
                        pass

        # moving taregt function
        if move_target and not game_over:
            target_x += target_speed[0] * dt
            target_y += target_speed[1] * dt
            # padding
            if target_x - TARGET_RADIUS < 0 + SPAWN_PADDING or target_x + TARGET_RADIUS > WIDTH - SPAWN_PADDING:
                target_speed[0] *= -1
                target_x = max(SPAWN_PADDING + TARGET_RADIUS, min(WIDTH - SPAWN_PADDING - TARGET_RADIUS, target_x))
            if target_y - TARGET_RADIUS < 0 + SPAWN_PADDING or target_y + TARGET_RADIUS > HEIGHT - SPAWN_PADDING:
                target_speed[1] *= -1
                target_y = max(SPAWN_PADDING + TARGET_RADIUS, min(HEIGHT - SPAWN_PADDING - TARGET_RADIUS, target_y))

        # end session token
        if time_left <= 0 and not game_over:
            game_over = True

        
        screen.fill((30, 30, 40))  

        # target
        if not game_over:
            pygame.draw.circle(screen, (200, 50, 50), (int(target_x), int(target_y)), TARGET_RADIUS)
            # target
            pygame.draw.line(screen, (255,255,255), (int(target_x)-10, int(target_y)), (int(target_x)+10, int(target_y)), 2)
            pygame.draw.line(screen, (255,255,255), (int(target_x), int(target_y)-10), (int(target_x), int(target_y)+10), 2)

        # HUD
        accuracy = (hits / shots * 100) if shots > 0 else 0.0
        draw_text(screen, f"Time: {time_left:.1f}s", 10, 10, font)
        draw_text(screen, f"hits: {hits}", 10, 40, font)
        draw_text(screen, f"shoots: {shots}", 10, 70, font)
        draw_text(screen, f"aim: {accuracy:.1f}%", 10, 100, font)
        draw_text(screen, "tap M for moving objects", 10, HEIGHT - 30, font)

        if game_over:
            # ciemne tło do podsumowania
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0,0,0,180))
            screen.blit(s, (0,0))

            draw_text(screen, "Congrats you've got", WIDTH//2 - 120, HEIGHT//2 - 100, big_font)
            draw_text(screen, f"hits: {hits}", WIDTH//2 - 120, HEIGHT//2 - 30, font)
            draw_text(screen, f"shoots: {shots}", WIDTH//2 - 120, HEIGHT//2, font)
            draw_text(screen, f"aim: {accuracy:.1f}%", WIDTH//2 - 120, HEIGHT//2 + 30, font)
            draw_text(screen, "tap R to restart", WIDTH//2 - 160, HEIGHT//2 + 80, font)
            draw_text(screen, "Made by Crabus", WIDTH//2 - 180, HEIGHT//2 + 50, font)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
