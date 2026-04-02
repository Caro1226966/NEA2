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

        # Multiple players
        self.single_player = False

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
        self.all_walls = pygame.sprite.Group()
        self.all_materials = pygame.sprite.Group()

        # Defaults to the game not having ended yet
        self.end = False
        self.winner = False

        # Menu setup
        self.setup_menu()

# The game's main loop that keeps it alive
    def mainloop(self):
        while self.running:
            # Check for quit
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # Quit
                        self.running = False

                    # Checks for the space on the results screen
                    elif (event.key == pygame.K_SPACE) and (not self.menu_card in self.all_sprites) and (self.menu_card.mode == "zombie_shooter" or self.menu_card.mode == '1V1') and self.end:
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
        self.do_game_drops()
        self.check_for_joystick()

        # Resets the game when it ends
        if self.end:
            self.end_game_reset()

    # Displays the screen to the user
    def draw_screen(self, screen):
        pygame.display.flip()
        screen.blit(self.background, (0, 0))
        self.all_sprites.draw(screen) # Draws the sprites
        self.draw_text(screen) # Draws the text

    # Displays all appropriate text at the appropriate time to the user
    def draw_text(self, screen):
        # Menu Screen ================================================================================
        # Zombie gamemode
        if self.menu_card.mode == "zombie_shooter" and self.menu_card in self.all_sprites:
            # zombie gamemode name
            text_surface = font.render('Zombie Shooter', True, (0, 255, 0))
            screen.blit(text_surface, (SCREEN_WIDTH/2.3, SCREEN_HEIGHT/10))

            # zombie gamemode high score
            text_surface = font.render(('High Score: ' + str(self.read_from_file())), True, (0,255,0))
            screen.blit(text_surface, (SCREEN_WIDTH/2.3, SCREEN_HEIGHT/1.15))

        # 1V1 Shooter Gamemode
        elif self.menu_card.mode == '1V1' and self.menu_card in self.all_sprites:
            # zombie gamemode name
            text_surface = font.render('1V1 Shooter', True, (255, 0, 0))
            screen.blit(text_surface, (SCREEN_WIDTH / 2.2, SCREEN_HEIGHT / 10))

            if self.single_player:
                text_surface = score_font.render('Connect Controller', True, (0, 0, 0))
                screen.blit(text_surface, ((SCREEN_WIDTH/30), SCREEN_HEIGHT / 3.5))

        # Zombie Shooter UI ============================================================================
        elif not self.menu_card in self.all_sprites and self.menu_card.mode == "zombie_shooter" and not self.end:
            # Monolith's health
            text_surface = font.render(('Monolith Health: ' + str(self.monolith.health)), True, (255, 0, 0))
            screen.blit(text_surface, (SCREEN_WIDTH/2.5, 0))

            # Wave number
            text_surface = font.render(('Wave: ' + str(self.monolith.wave)), True, (255, 0, 0))
            screen.blit(text_surface, (SCREEN_WIDTH/2.1, SCREEN_HEIGHT/17))

            # Player1's material count
            text_surface = font.render(('Materials: ' + str(self.player1.wall_materials)), True, (245, 195, 78))
            screen.blit(text_surface, (SCREEN_WIDTH / 30,0))

            # Player2's material count
            if not self.single_player:
                text_surface = font.render(('Materials: ' + str(self.player2.wall_materials)), True, (78, 101, 245))
                screen.blit(text_surface, (SCREEN_WIDTH / 1.3,0))


        # Zombie shooter end score =======================================================================
        elif not self.menu_card in self.all_sprites and self.menu_card.mode == "zombie_shooter" and self.end:
            text_surface = score_font.render(('Score: ' + str(self.monolith.seconds_lifespan)), True, (255, 0, 0))
            screen.blit(text_surface, ((SCREEN_WIDTH / 5), SCREEN_HEIGHT / 3.5))

        # 1v1 Shooter UI =================================================================================
        # Player1's material count
        elif not self.menu_card in self.all_sprites and self.menu_card.mode == "1V1" and not self.end:
            text_surface = font.render(('Materials: ' + str(self.player1.wall_materials)), True, (245, 195, 78))
            screen.blit(text_surface, (SCREEN_WIDTH / 30, 0))

            # Player2's material count
            if not self.single_player:
                text_surface = font.render(('Materials: ' + str(self.player2.wall_materials)), True, (78, 101, 245))
                screen.blit(text_surface, (SCREEN_WIDTH / 1.3, 0))

            # Player1's health
            text_surface = font.render(('Health: ' + str(self.player1.health)), True, (245, 195, 78))
            screen.blit(text_surface, (SCREEN_WIDTH / 4, 0))

            # Player2's health
            text_surface = font.render(('Health: ' + str(self.player2.health)), True, (78, 101, 245))
            screen.blit(text_surface, (SCREEN_WIDTH / 1.7, 0))

        # 1V1 shooter end score =======================================================================
        elif not self.menu_card in self.all_sprites and self.menu_card.mode == "1V1" and self.end:
            text_surface = score_font.render(('Winner: ' + str(self.winner)), True, (255, 0, 0))
            screen.blit(text_surface, ((SCREEN_WIDTH / 8), SCREEN_HEIGHT / 3.5))

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
        # Sets and scales the in game background
        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))

        # Setup Sprites
        self.player1 = Player(SCREEN_WIDTH/1.9,SCREEN_HEIGHT/2,'red',True, self)
        self.pointer1 = Pointer(True, SCREEN_WIDTH/1.9,SCREEN_HEIGHT/2)

        # Player2 Spawn
        if not self.single_player:
            self.player2 = Player(SCREEN_WIDTH/1.9,SCREEN_HEIGHT/2,'blue',False, self)
            self.pointer2 = Pointer(False, SCREEN_WIDTH/1.9, SCREEN_HEIGHT/2)
            self.all_sprites.add(self.pointer2, self.player2)

        # Monolith spawn
        self.monolith = Monolith(SCREEN_WIDTH/1.9, SCREEN_HEIGHT/2, self)

        # Adds all the objects to the sprite groups
        self.all_sprites.add(self.player1, self.pointer1, self.monolith)
        self.all_players.add(self.player1)

        pygame.mouse.set_visible(False) # Makes you unable to see the mouse so the custom cursors look better

    # Sets up the game screen for the 1v1 shooter
    def setup_1v1_shooter(self):
        # Sets and scales the in game background
        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))

        # Setup Sprites
        self.player1 = Player(SCREEN_WIDTH / 15, SCREEN_HEIGHT / 2, 'red', True, self)
        self.player2 = Player(SCREEN_WIDTH / 1.1, SCREEN_HEIGHT / 2, 'blue', False, self)
        self.pointer1 = Pointer(True, SCREEN_WIDTH/15, SCREEN_HEIGHT/2)
        self.pointer2 = Pointer(False, SCREEN_WIDTH/1.1, SCREEN_HEIGHT/2)

        # Adds all the objects to the sprite groups
        self.all_sprites.add(self.player1, self.player2, self.pointer1, self.pointer2)
        self.all_players.add(self.player1, self.player2)

        pygame.mouse.set_visible(False) # Makes you unable to see the mouse so the custom cursors look better


    # Controls the material drops across both gamemodes
    def do_game_drops(self):
        # Make sure you are in game
        if not self.menu_card in self.all_sprites:
            # Spawn the wall if a probability is met
            if random.randint(0,WALL_MATERIAL_SPAWN_PROB) == 5:
                wall_material = WallMaterial(random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT), self)
                self.all_sprites.add(wall_material)
                self.all_materials.add(wall_material)

    # Clear all the sprite groups
    def sprite_reset(self):
        self.all_sprites = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()
        self.all_zombies = pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group()
        self.all_walls = pygame.sprite.Group()
        self.all_materials = pygame.sprite.Group()

    # Reset the game back to the menu when the game ends
    def end_game_reset(self):
        if self.end:

            # Resets the sprites
            self.sprite_reset()

            # Only triggers on the zombie shooter game
            if self.menu_card.mode == "zombie_shooter":
                self.old_score = self.read_from_file() # Read the contents of the file
                self.old_score = int(self.old_score) # Make sure the old score isn't nothing

                # Write to the file depending on what was previously on it
                if self.old_score <= self.monolith.seconds_lifespan:
                    self.write_to_file(self.monolith.seconds_lifespan)
                    self.old_score = self.monolith.seconds_lifespan

                elif self.old_score > self.monolith.seconds_lifespan:
                    pass
                    # print('No high score!')

                # Change the background to the menu background
                self.background = pygame.image.load("zombie_menu_background.png")

            # Only triggers on the 1v1 shooter game
            elif self.menu_card.mode == '1V1':
                pass # Put the background change here


    # Checks if a joystick has been connected
    def check_for_joystick(self):
        if pygame.joystick.get_count() < 1:
            self.single_player = True
        else:
            self.single_player = False

    # This safely returns whatever is in the file
    def read_from_file(self):
        file = open('zombie_shooter_score.txt', 'r') # Opens the file as read
        read = file.read() # Reads the file

        # Makes sure it is not returning a corrupt or incorrect value
        if not read.isdigit():
                read = 0 # If it is incorrect change it to 0 so it doesn't crash or cause errors
                self.write_to_file(read)

        file.close() # Closes the read file
        return read # returns the file's contents


    # Writes the parameter to file
    def write_to_file(self, write):
        # Opens the file to write and writes to it
        file = open('zombie_shooter_score.txt', 'w')
        file.write(str(write))
        file.close() # Closes the write file

# The thing that makes it run
if __name__ == "__main__":
    g=Game()
    g.mainloop()
