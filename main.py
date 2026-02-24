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
        self.pointer1 = None
        self.pointer2 = None

        # Makes sure the old score is recorded properly
        self.old_score = self.read_from_file()

        # Menu card
        self.menu_card = None

        # Monolith
        self.monolith = None

        # Sets the default background
        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))

        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()
        self.all_zombies = pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group()

        # Defaults to the game not having ended yet
        self.end = False

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
                    elif (event.key == pygame.K_SPACE) and (not self.menu_card in self.all_sprites) and (self.menu_card.mode == "zombie_shooter") and self.end:
                        self.end = False
                        self.sprite_reset()
                        self.setup_menu()

            # updates the program and refreshes the screen
            self.update()
            self.draw_screen(screen)

            # Locks the logic updates to 60/sec
            time.sleep(1 / 60)

    # Runs updates for all sprite logic and resets on game end
    def update(self):
        self.all_sprites.update()

        if self.end:
            self.end_game_reset()

    # Displays the screen to the user
    def draw_screen(self, screen):
        pygame.display.flip()
        screen.blit(self.background, (0, 0))
        self.all_sprites.draw(screen)

        self.draw_text(screen)

    # Displays all appropriate text at the appropriate time to the user
    def draw_text(self, screen):
        if self.menu_card.mode == "zombie_shooter" and self.menu_card in self.all_sprites:
            # Game name
            text_surface = font.render('Zombie Shooter', True, (0, 255, 0))
            screen.blit(text_surface, (SCREEN_WIDTH/2.3, SCREEN_HEIGHT/10))

            # Game score
            text_surface = font.render(('High Score: ' + str(self.read_from_file())), True, (0,255,0))
            screen.blit(text_surface, (SCREEN_WIDTH/2.3, SCREEN_HEIGHT/1.15))


        elif not self.menu_card in self.all_sprites and self.menu_card.mode == "zombie_shooter" and not self.end:
            # Monolith's health
            text_surface = font.render(('Monolith Health: ' + str(self.monolith.health)), True, (255, 0, 0))
            screen.blit(text_surface, (SCREEN_WIDTH/2.5, 0))

            # Wave number
            text_surface = font.render(('Wave: ' + str(self.monolith.wave)), True, (255, 0, 0))
            screen.blit(text_surface, (SCREEN_WIDTH/2.1, SCREEN_HEIGHT/17))


        elif not self.menu_card in self.all_sprites and self.menu_card.mode == "zombie_shooter" and self.end:
            # Zombie shooter end score
            text_surface = score_font.render(('Score: ' + str(self.monolith.seconds_lifespan)), True, (255, 0, 0))
            screen.blit(text_surface, ((SCREEN_WIDTH / 5), SCREEN_HEIGHT / 3.5))

        elif self.menu_card.mode == "1v1_shooter" and self.menu_card in self.all_sprites:
            # Game name
            text_surface = font.render('1V1', True, (255, 0, 0))
            screen.blit(text_surface, (SCREEN_WIDTH / 1.97, SCREEN_HEIGHT / 10))


    # Sets up the default main menu for the game
    def setup_menu(self):
        # Sets and scales appropriate background
        self.background = pygame.image.load("zombie_menu_background.png")
        self.background = pygame.transform.scale(self.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))


        # Create the menu card
        self.menu_card = MenuCard(SCREEN_WIDTH/1.9, SCREEN_HEIGHT/2, 'green', self)
        self.all_sprites.add(self.menu_card)

        pygame.mouse.set_visible(True) # Makes you able to see your mouse


    # This sets up the start of the default zombie shooter gamemode
    def setup_zombie_shooter(self):
        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))

        # Setup Sprites
        self.player1 = Player(SCREEN_WIDTH/1.9,SCREEN_HEIGHT/2,'red',True, self)
        self.player2 = Player(SCREEN_WIDTH/1.9,SCREEN_HEIGHT/2,'blue',False, self)
        self.pointer1 = Pointer(False)
        self.pointer2 = Pointer(True)
        self.monolith = Monolith(SCREEN_WIDTH/1.9, SCREEN_HEIGHT/2, self)

        self.all_sprites.add(self.player1, self.player2, self.pointer1, self.pointer2, self.monolith)
        self.all_players.add(self.player1, self.player2)

        pygame.mouse.set_visible(False)

    def setup_1v1_shooter(self):
        pass

    def sprite_reset(self):
        self.all_sprites = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()
        self.all_zombies = pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group()

    def end_game_reset(self):
        if self.end:
            self.sprite_reset()

            # Only triggers on the zombie shooter game
            if self.menu_card.mode == "zombie_shooter":
                # Read the contents of the file
                self.old_score = self.read_from_file()

                # Make sure the old score isn't nothing
                self.old_score = int(self.old_score)

                # Write to the file depending on what was previously on it
                if self.old_score <= self.monolith.seconds_lifespan:
                    self.write_to_file(self.monolith.seconds_lifespan)
                    self.old_score = self.monolith.seconds_lifespan
                elif self.old_score > self.monolith.seconds_lifespan:
                    print('No high score!')

                # Change the background
                self.background = pygame.image.load("zombie_menu_background.png")


    # This safely returns whatever is in the file
    def read_from_file(self):
        file = open('zombie_shooter_score.txt', 'r') # Opens the file as read
        read = file.read() # Reads the file

        # Makes sure it is not returning a corrupt value
        if not read.isdigit():
                read = 0
                self.write_to_file(read)

        file.close() # Closes the read file
        return read # returns the file's contents


    # Writes the parameter to file
    def write_to_file(self, write):
        # Opens the file to write and writes to it
        file = open('zombie_shooter_score.txt', 'w')
        file.write(str(write))
        file.close() # Closes the write file





if __name__ == "__main__":
    g=Game()
    g.mainloop()
