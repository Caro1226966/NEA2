from config import *
from sprites import *

# Initializes pygame
pygame.init()

class Game:
    def __init__(self):

        # Sets the game running
        self.running = True

        # Players
        self.player1 = None
        self.player2 = None

        # Menu card
        self.menu_card = None

        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))

        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()
        self.all_zombies = pygame.sprite.Group()

        # Menu setup
        self.setup_menu()


    def mainloop(self):
        # Game loop
        while self.running:
            # Check for quit
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # updates the program and refreshes the screen
            self.update()
            self.draw_screen(screen)

            # Locks the logic updates to 60/sec
            time.sleep(1 / 60)

    def update(self):
        self.all_sprites.update()

    def draw_screen(self, screen):
        pygame.display.flip()
        screen.blit(self.background, (0, 0))
        self.all_sprites.draw(screen)

        self.draw_text(screen)


    def draw_text(self, screen):

        if self.menu_card.mode == "zombie_shooter":
            text_surface = font.render('Zombie Shooter', True, (0, 255, 0))
            screen.blit(text_surface, (SCREEN_WIDTH/2.3, SCREEN_HEIGHT/10))
        else:
            text_surface = font.render('1V1', True, (255, 0, 0))
            screen.blit(text_surface, (SCREEN_WIDTH / 1.97, SCREEN_HEIGHT / 10))

    def setup_menu(self):
        self.background = pygame.image.load("zombie_menu_background.png")
        self.background = pygame.transform.scale(self.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))


        # Create the menu card
        self.menu_card = MenuCard(SCREEN_WIDTH/1.9, SCREEN_HEIGHT/2, 'green', self)
        self.all_sprites.add(self.menu_card)

    def setup_zombie_shooter(self):
        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))


        self.player1 = Player(SCREEN_WIDTH/1.9,SCREEN_HEIGHT/2,'red',True, self)
        self.player2 = Player(SCREEN_WIDTH/2.1,SCREEN_HEIGHT/2,'blue',False, self)

        self.all_sprites.add(self.player1, self.player2)
        self.all_players.add(self.player1, self.player2)

    def setup_1v1_shooter(self):
        pass

    def reset(self):
        self.all_sprites = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()
        self.all_zombies = pygame.sprite.Group()



if __name__ == "__main__":
    g=Game()
    g.mainloop()
