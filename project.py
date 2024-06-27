import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 600
TOOLBAR_HEIGHT = 100
window = pygame.display.set_mode((WIDTH, HEIGHT + TOOLBAR_HEIGHT))
pygame.display.set_caption("Simple Paint with Tools and Colors")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
BRUSH_SIZE = 5
ERASER_SIZE = 10
current_color = BLACK


BRUSH = 'brush'
ERASER = 'eraser'
FILL = 'fill'
EYEDROPPER = 'eyedropper'
current_tool = BRUSH

window.fill(WHITE)

undo_stack = []
redo_stack = []

def save_state():
    undo_stack.append(window.copy())
    if len(undo_stack) > 20:
        undo_stack.pop(0)
    redo_stack.clear()

def undo():
    if undo_stack:
        redo_stack.append(window.copy())
        last_state = undo_stack.pop()
        window.blit(last_state, (0, 0))

def redo():
    if redo_stack:
        undo_stack.append(window.copy())
        next_state = redo_stack.pop()
        window.blit(next_state, (0, 0))

def fill(screen, pos, color):
    target_color = screen.get_at(pos)
    if target_color == color:
        return

    fill_queue = [pos]
    while fill_queue:
        x, y = fill_queue.pop()
        if screen.get_at((x, y)) != target_color:
            continue

        west, east = x, x
        while west > 0 and screen.get_at((west - 1, y)) == target_color:
            west -= 1
        while east < WIDTH - 1 and screen.get_at((east + 1, y)) == target_color:
            east += 1

        for i in range(west, east + 1):
            screen.set_at((i, y), color)
            if y > 0 and screen.get_at((i, y - 1)) == target_color:
                fill_queue.append((i, y - 1))
            if y < HEIGHT - 1 and screen.get_at((i, y + 1)) == target_color:
                fill_queue.append((i, y + 1))

def draw_toolbar():
    toolbar_rect = pygame.Rect(0, HEIGHT, WIDTH, TOOLBAR_HEIGHT)
    pygame.draw.rect(window, GRAY, toolbar_rect)

    brush_button = pygame.Rect(10, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, BLACK, brush_button)
    eraser_button = pygame.Rect(50, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, BLACK, eraser_button)
    fill_button = pygame.Rect(90, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, BLACK, fill_button)
    eyedropper_button = pygame.Rect(130, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, BLACK, eyedropper_button)

    black_button = pygame.Rect(200, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, BLACK, black_button)
    white_button = pygame.Rect(240, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, WHITE, white_button)
    blue_button = pygame.Rect(280, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, BLUE, blue_button)
    green_button = pygame.Rect(320, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, GREEN, green_button)
    red_button = pygame.Rect(360, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, RED, red_button)

    undo_button = pygame.Rect(400, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, BLACK, undo_button)
    redo_button = pygame.Rect(440, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, BLACK, redo_button)
    save_button = pygame.Rect(480, HEIGHT + 10, 30, 30)
    pygame.draw.rect(window, BLACK, save_button)

    return (brush_button, eraser_button, fill_button, eyedropper_button,
            black_button, white_button, blue_button, green_button, red_button,
            undo_button, redo_button, save_button)

def save_image():
    filename = "drawing.jpg"
    sub_surface = window.subsurface((0, 0, WIDTH, HEIGHT))
    pygame.image.save(sub_surface, filename)
    print(f"Image saved as {filename}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] >= HEIGHT:
                if brush_button.collidepoint(event.pos):
                    current_tool = BRUSH
                elif eraser_button.collidepoint(event.pos):
                    current_tool = ERASER
                elif fill_button.collidepoint(event.pos):
                    current_tool = FILL
                elif eyedropper_button.collidepoint(event.pos):
                    current_tool = EYEDROPPER
                elif black_button.collidepoint(event.pos):
                    current_color = BLACK
                elif white_button.collidepoint(event.pos):
                    current_color = WHITE
                elif blue_button.collidepoint(event.pos):
                    current_color = BLUE
                elif green_button.collidepoint(event.pos):
                    current_color = GREEN
                elif red_button.collidepoint(event.pos):
                    current_color = RED
                elif undo_button.collidepoint(event.pos):
                    undo()
                elif redo_button.collidepoint(event.pos):
                    redo()
                elif save_button.collidepoint(event.pos):
                    save_image()
            else:
                save_state()
                if current_tool == FILL:
                    fill(window, event.pos, current_color)
                elif current_tool == EYEDROPPER:
                    current_color = window.get_at(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                if event.pos[1] < HEIGHT:
                    if current_tool == BRUSH:
                        pygame.draw.circle(window, current_color, event.pos, BRUSH_SIZE)
                    elif current_tool == ERASER:
                        pygame.draw.circle(window, WHITE, event.pos, ERASER_SIZE)

    (brush_button, eraser_button, fill_button, eyedropper_button,
     black_button, white_button, blue_button, green_button, red_button,
     undo_button, redo_button, save_button) = draw_toolbar()
    pygame.display.flip()

pygame.quit()
sys.exit()
