from variables import *


# class DropDown:
#     def __init__(self, color_menu, color_option, x_axis, y_axis, width, height, font, main, options):
#         self.color_menu = color_menu
#         self.color_option = color_option
#         self.font = font
#         self.rect = pygame.Rect(x_axis, y_axis, width, height)
#         self.options = options
#         self.main = main
#         self.draw_menu = False
#         self.menu_active = False
#         self.active_option = -1
#
#     def draw(self, surf):
#         pygame.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
#         msg = self.font.render(self.main, 1, (0, 0, 0))
#         surf.blit(msg, msg.get_rect(center=self.rect.center))
#
#         if self.draw_menu:
#             for i, text in enumerate(self.options):
#                 rect = self.rect.copy()
#                 rect.y += (i + 1) * self.rect.height
#                 pygame.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
#                 msg = self.font.render(text, 1, (0, 0, 0))
#                 surf.blit(msg, msg.get_rect(center=rect.center))
#
#     def update(self, event_list):
#         mouse_pos = pygame.mouse.get_pos()
#         self.menu_active = self.rect.collidepoint(mouse_pos)
#
#         self.active_option = -1
#         for i in range(len(self.options)):
#             rect = self.rect.copy()
#             rect.y += (i + 1) * self.rect.height
#             if rect.collidepoint(mouse_pos):
#                 self.active_option = i
#                 break
#
#         if not self.menu_active and self.active_option == -1:
#             self.draw_menu = False
#
#         for event in event_list:
#             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 if self.menu_active:
#                     self.draw_menu = not self.draw_menu
#                 elif self.draw_menu and self.active_option >= 0:
#                     self.draw_menu = False
#                     return self.active_option
#         return -1


class RadioButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, font, text):
        super().__init__()
        text_surf = font.render(text, True, (0, 0, 0))
        self.button_image = pygame.Surface((w, h))
        self.button_image.fill((96, 96, 96))
        self.button_image.blit(text_surf, text_surf.get_rect(center=(w // 2, h // 2)))
        self.hover_image = pygame.Surface((w, h))
        self.hover_image.fill((96, 96, 96))
        self.hover_image.blit(text_surf, text_surf.get_rect(center=(w // 2, h // 2)))
        pygame.draw.rect(self.hover_image, (96, 196, 96), self.hover_image.get_rect(), 3)
        self.clicked_image = pygame.Surface((w, h))
        self.clicked_image.fill((96, 196, 96))
        self.clicked_image.blit(text_surf, text_surf.get_rect(center=(w // 2, h // 2)))
        self.image = self.button_image
        self.rect = pygame.Rect(x, y, w, h)
        self.clicked = False
        self.buttons = None

    def setRadioButtons(self, buttons):
        self.buttons = buttons

    def update(self, event_list):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover and event.button == 1:
                    for rb in self.buttons:
                        rb.clicked = False
                    self.clicked = True

        self.image = self.button_image
        if self.clicked:
            self.image = self.clicked_image
        elif hover:
            self.image = self.hover_image

# pygame.init()
# clock = pygame.time.Clock()
# screen = pygame.display.set_mode((640, 480))
#
# COLOR_INACTIVE = (100, 80, 255)
# COLOR_ACTIVE = (100, 200, 255)
# COLOR_LIST_INACTIVE = (255, 100, 100)
# COLOR_LIST_ACTIVE = (255, 150, 150)
#
# list1 = DropDown(
#     [COLOR_INACTIVE, COLOR_ACTIVE],
#     [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
#     50, 50, 200, 50,
#     pygame.font.Font(None, 30),
#     "Select Mode", ["Calibration", "Test"])
#
# run = True
# while run:
#     clock.tick(30)
#
#     event_list = pygame.event.get()
#     for event in event_list:
#         if event.type == pygame.QUIT:
#             run = False
#
#     selected_option = list1.update(event_list)
#     if selected_option >= 0:
#         list1.main = list1.options[selected_option]
#
#     list1.draw(screen)
#     pygame.display.flip()
#
# pygame.quit()
# exit()
