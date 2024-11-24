import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Geometry Dash Caca")

# Chargement des images
background = pygame.image.load('background.png').convert()  # Charger l'image de fond
background = pygame.transform.scale(background, (width, height))  # Redimensionner à 800x600

# Chargement des images du caca
caca_images = [pygame.image.load('caca1.png').convert_alpha(), 
               pygame.image.load('caca2.png').convert_alpha()]

# Chargement des images des obstacles
obstacle_images = [
    pygame.image.load('obstacle_25.png').convert_alpha(), 
    pygame.image.load('obstacle_32.png').convert_alpha(), 
    pygame.image.load('obstacle_40.png').convert_alpha(), 
    pygame.image.load('obstacle_50.png').convert_alpha()
]

# Chargement des images des boutons
start_button = pygame.image.load('start_button.png').convert_alpha()
restart_button = pygame.image.load('restart_button.png').convert_alpha()
quit_button = pygame.image.load('quit_button.png').convert_alpha()
continue_button = pygame.image.load('continue.png').convert_alpha()

# Redimensionnement des boutons
button_scale = (100, 100)  # Taille des boutons (largeur, hauteur)
start_button = pygame.transform.scale(start_button, button_scale)
restart_button = pygame.transform.scale(restart_button, button_scale)
quit_button = pygame.transform.scale(quit_button, button_scale)
continue_button = pygame.transform.scale(continue_button, button_scale)

# Couleurs
green = (0, 255, 0)    # Couleur de fond
black = (0, 0, 0)      # Couleur des obstacles
red = (255, 0, 0)      # Couleur des textes

# Propriétés du caca
caca_size = 32
caca_x = 100
caca_y = height - caca_size
caca_velocity_y = 0
gravity = 0.5
jump_strength = -15
on_ground = True

# Liste des obstacles
obstacles = []
obstacle_width = 50
max_obstacle_height = caca_size * 2  # Max 2 fois la hauteur du caca
min_obstacle_height = 25  # Hauteur minimale pour les obstacles

# Timer pour ajouter des obstacles
obstacle_timer = 0
obstacle_delay = 1500  # Délai pour ajouter des obstacles (1,5 seconde)

# Temps de jeu
game_time = 0
start_time = pygame.time.get_ticks()
duration = 60000  # 1 minute en millisecondes

# Vitesse d'obstacle initiale
obstacle_speed = 5

# Variable de jeu
score = 0
game_over = False
paused = False
game_started = False
game_won = False

# Animation du caca
animation_frame = 0
animation_speed = 500  # Vitesse de l'animation (500 ms pour chaque image)
animation_counter = 0

def draw_text(text, font, color, surface, x, y):
    """Fonction pour dessiner du texte sur l'écran."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def draw_button(image, x, y):
    """Fonction pour dessiner un bouton et retourner son rectangle."""
    button_rect = image.get_rect(center=(x, y))
    screen.blit(image, button_rect)
    return button_rect

def reset_game():
    """Réinitialiser les variables du jeu."""
    global caca_y, caca_velocity_y, on_ground, obstacles, obstacle_timer, score, game_over, game_started, game_time, start_time, game_won
    caca_y = height - caca_size
    caca_velocity_y = 0
    on_ground = True
    obstacles = []
    obstacle_timer = 0
    score = 0
    game_over = False
    game_started = True
    game_won = False
    game_time = 0
    start_time = pygame.time.get_ticks()

# Boucle principale
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Mettre en pause
                paused = not paused
            
            if event.key == pygame.K_r and (game_over or game_won):  # Rejouer
                reset_game()
            
            if event.key == pygame.K_RETURN and not game_started:  # Commencer le jeu
                reset_game()

            # Sauter avec la touche Espace
            if event.key == pygame.K_SPACE and on_ground and game_started:
                caca_velocity_y = jump_strength  # Appliquer la force de saut
                on_ground = False  # Le caca n'est plus sur le sol

        if event.type == pygame.MOUSEBUTTONDOWN:  # Vérifier les clics de souris
            mouse_pos = pygame.mouse.get_pos()  # Obtenir la position de la souris

            # Vérifier le clic sur le bouton "Start"
            if not game_started and draw_button(start_button, width // 2, height // 2).collidepoint(mouse_pos):
                reset_game()

            # Vérifier le clic sur le bouton "Restart"
            if game_over or game_won:
                if draw_button(restart_button, width // 2, height // 2 + 50).collidepoint(mouse_pos):
                    reset_game()

                # Vérifier le clic sur le bouton "Quit"
                if draw_button(quit_button, width // 2, height // 2 + 150).collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

    if not game_over and not paused:
        if game_started:
            # Mouvements du caca
            caca_velocity_y += gravity
            caca_y += caca_velocity_y

            # Vérifier si le caca touche le sol
            if caca_y >= height - caca_size:
                caca_y = height - caca_size
                caca_velocity_y = 0
                on_ground = True

            # Ajouter des obstacles (1 à 4 à chaque intervalle)
            obstacle_timer += clock.get_time()
            if obstacle_timer > obstacle_delay:
                num_obstacles = random.randint(1, 4)  # Générer entre 1 et 4 obstacles
                for _ in range(num_obstacles):
                    obstacle_height = random.randint(min_obstacle_height, max_obstacle_height)  # Hauteur aléatoire
                    obstacle_index = random.randint(0, len(obstacle_images) - 1)  # Index pour sélectionner une image d'obstacle
                    obstacles.append([width, height - obstacle_height, obstacle_width, obstacle_height, obstacle_index])
                obstacle_timer = 0

            # Déplacer les obstacles
            for obstacle in obstacles:
                obstacle[0] -= obstacle_speed  # Déplacement vers la gauche

            # Supprimer les obstacles hors écran
            obstacles = [obstacle for obstacle in obstacles if obstacle[0] > -obstacle_width]

            # Vérifier les collisions
            for obstacle in obstacles:
                if (caca_x + caca_size > obstacle[0] and caca_x < obstacle[0] + obstacle[2] and
                    caca_y + caca_size > obstacle[1] and caca_y < obstacle[1] + obstacle[3]):
                    game_over = True  # Mettre le jeu en mode "Game Over"

            # Mettre à jour la vitesse des obstacles en fonction du temps
            game_time = pygame.time.get_ticks() - start_time
            if game_time < duration:
                obstacle_speed = 5 + (game_time // 10000) * 0.5  # Accélération
                score += 1  # Incrémenter le score

            # Vérifier si le temps est écoulé
            if game_time >= duration:
                game_won = True  # Mettre le jeu en mode "Gagné"
                game_started = False  # Arrêter le jeu

            # Animation du caca
            animation_counter += clock.get_time()
            if animation_counter > animation_speed:
                animation_frame = (animation_frame + 1) % len(caca_images)  # Passer à l'image suivante
                animation_counter = 0

    # Dessiner tout
    screen.blit(background, (0, 0))  # Dessiner le fond

    if not game_started:
        # Afficher l'écran de démarrage avec le bouton de démarrage
        draw_text("Bienvenue dans Geometry Dash Caca!", pygame.font.Font(None, 40), black, screen, width // 2, height // 2 - 100)
        draw_button(start_button, width // 2, height // 2)  # Bouton de démarrage
    elif game_won:
        # Afficher l'écran de victoire
        draw_text("Vous avez gagné!", pygame.font.Font(None, 74), red, screen, width // 2, height // 2 - 40)
        draw_button(restart_button, width // 2, height // 2 + 50)  # Bouton de redémarrage
        draw_button(quit_button, width // 2, height // 2 + 150)  # Bouton de quitter
    elif game_over:
        # Afficher l'écran de game over avec le bouton de redémarrage
        draw_text("Game Over", pygame.font.Font(None, 74), red, screen, width // 2, height // 2 - 40)
        draw_button(restart_button, width // 2, height // 2 + 50)  # Bouton de redémarrage
        draw_button(quit_button, width // 2, height // 2 + 150)  # Bouton de quitter
    else:
        # Afficher le caca en utilisant l'animation
        screen.blit(caca_images[animation_frame], (caca_x, caca_y))
        # Afficher les obstacles
        for obstacle in obstacles:
            obstacle_image = obstacle_images[obstacle[4]]
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

        # Afficher le score
        draw_text(f"Score: {score}", pygame.font.Font(None, 36), (255, 255, 255), screen, width // 2, 30)

        # Afficher le temps restant
        time_remaining = max(0, (duration - game_time) // 1000)
        draw_text(f"Temps restant : {time_remaining}", pygame.font.Font(None, 36), (255, 255, 255), screen, width - 160, 30)

    # Rafraîchir l'écran
    pygame.display.flip()
    clock.tick(60)  # Limiter à 60 FPS
