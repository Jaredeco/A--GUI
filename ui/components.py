import pygame
from globals import white, black, brown, light_brown, green, red, FONT
from pygame.gfxdraw import filled_circle
from algorithms import AStar


class Node:
    def __init__(self, x, y, pos, size_x, size_y):
        self.x = x
        self.y = y
        self.pos = pos
        self.size_x = size_x
        self.size_y = size_y
        self.is_wall = False
        self.parent = None
        self.g = self.h = self.f = 0

    def __eq__(self, other):
        return self.pos == other.pos

    def draw(self, win, grid, ip):
        color = green if ip else brown
        if self.is_wall:
            pygame.draw.rect(win, white, (self.x, self.y, self.size_x, self.size_y))
        else:
            pygame.draw.rect(win, color, (self.x, self.y, self.size_x, self.size_y), 1)
        radius = 8
        if self.pos == grid.start:
            filled_circle(win, self.x + int(radius * 1.5), self.y + int(radius * 1.5), radius, green)
        elif self.pos == grid.target:
            filled_circle(win, self.x + int(radius * 1.5), self.y + int(radius * 1.5), radius, red)

    def make_wall(self, right=False):
        if self.is_wall and right:
            self.is_wall = False
        elif not self.is_wall and not right:
            self.is_wall = True


class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.text = FONT.render(text, True, black)

    def draw(self, win):
        mpos = pygame.mouse.get_pos()
        active = self.rect.collidepoint(*mpos)
        color = brown
        if active:
            color = light_brown
        pygame.draw.rect(win, color, self.rect)
        pygame.draw.rect(win, black, self.rect, 3)
        win.blit(self.text, self.text.get_rect(center=self.rect.center))

    def button(self, grid, pos, selected):
        x, y = pos
        if self.rect.collidepoint(x, y) and selected is not None:
            if selected == 0:
                AStar.a_star(grid)


class DropDown:
    def __init__(self, x, y, width, height, main, options):
        self.color_menu = [brown, light_brown]
        self.color_option = [brown, light_brown]
        self.rect = pygame.Rect(x, y, width, height)
        self.main = main
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.selected_idx = None
        self.active_option = -1

    def draw(self, win):
        pygame.draw.rect(win, self.color_menu[self.menu_active], self.rect, 0)
        msg = FONT.render(self.main, 1, black)
        win.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.options):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(win, self.color_option[1 if i == self.active_option else 0], rect, 0)
                msg = FONT.render(text, 1, black)
                win.blit(msg, msg.get_rect(center=rect.center))

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(*mpos)

        self.active_option = -1
        for i in range(len(self.options)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.draw_menu = False
                    return self.active_option
        return -1

