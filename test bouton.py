import pygame
import pygame_gui

pygame.init()

# Initialisation de Pygame GUI
pygame.init()

# Paramètres pour la fenêtre principale
window_size = (800, 600)
background_color = (255, 255, 255)

# Création de la fenêtre principale
pygame.display.set_caption('Pygame GUI Button Style')
window_surface = pygame.display.set_mode(window_size)
window_surface.fill(background_color)

# Création du gestionnaire d'interface utilisateur
ui_manager = pygame_gui.UIManager(window_size)

# Définition du style du bouton
button_style = {
    "normal_bg": pygame.Color('dodgerblue'),
    "hovered_bg": pygame.Color('deepskyblue'),
    "disabled_bg": pygame.Color('gray'),
    "border_color": pygame.Color('black'),
    "text_color": pygame.Color('white'),
    "font": pygame.font.Font(None, 36),
}

# Création du bouton avec le style défini
button_rect = pygame.Rect(100, 100, 200, 50)
button = pygame_gui.elements.UIButton(
    relative_rect=button_rect,
    text='Custom Button',
    manager=ui_manager,
    object_id=pygame_gui.core.ObjectID('custom_button', 'button'),
    container=None,
    starting_height=1,
    layer_starting_height=1,
    layer_thickness=1,
    anchors={'left': 'left',
             'right': 'right',
             'top': 'top',
             'bottom': 'bottom'})

# Application principale
running = True
clock = pygame.time.Clock()

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button:
                    print('Custom button pressed!')

        ui_manager.process_events(event)

    ui_manager.update(time_delta)
    window_surface.fill(background_color)

    ui_manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
