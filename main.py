import pygame
from globals import SCREEN_WIDTH, SCREEN_HEIGHT, light_brown
from ui.grid import Grid
from ui.components import Button, DropDown

pygame.init()
FPS = 60
CLOCK = pygame.time.Clock()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PF-Visualization")
GRID = Grid()
hs = SCREEN_WIDTH // 2
vsb = Button(hs, 0, hs, 30, "Visualize")
drop_down = DropDown(0, 0, hs, 30, "Algorithm", ["A*"])


def redraw_win():
    win.fill(light_brown)
    vsb.draw(win)
    GRID.draw(win)
    drop_down.draw(win)
    pygame.display.flip()


def main():
    RUN = True
    st = False
    tg = False
    while RUN:
        CLOCK.tick(FPS)
        events = pygame.event.get()
        selected = drop_down.update(events)
        if selected >= 0:
            drop_down.selected_idx = selected
            drop_down.main = drop_down.options[selected]
        for event in events:
            if event.type == pygame.QUIT:
                RUN = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                vsb.button(GRID, event.pos, drop_down.selected_idx)
                if st and not GRID.grid[GRID.start[0]][GRID.start[1]].is_wall:
                    st = False
                elif tg and not GRID.grid[GRID.target[0]][GRID.target[1]].is_wall:
                    tg = False
            elif True not in [st, tg]:
                try:
                    mp = pygame.mouse.get_pressed()
                    r, c = GRID.get_row_col_clicked(event.pos)
                    if mp[0] and (r, c) not in [GRID.start, GRID.target]:
                        GRID.grid[r][c].make_wall()
                    elif mp[2]:
                        GRID.grid[r][c].make_wall(True)
                except AttributeError:
                    pass

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            st = not tg
        elif keys[pygame.K_t]:
            tg = not st
        r, c = GRID.get_row_col_clicked(pygame.mouse.get_pos())
        if st:
            GRID.start = (r, c)
        elif tg:
            GRID.target = (r, c)
        redraw_win()
    pygame.quit()


if __name__ == "__main__":
    main()
