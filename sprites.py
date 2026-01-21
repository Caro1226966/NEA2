import pygame

from config import *

pygame.joystick.init()

class Monolith(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super(Monolith, self).__init__()

        self.image = pygame.image.load('monolith.png')
        self.image = pygame.transform.scale(self.image, (MONOLITH_WIDTH, MONOLITH_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.game = game

        # This is the monolith's health
        self.health = 1000

        # All the time difficulty parameters
        self.tick_lifespan = 0
        self.seconds_lifespan = 0
        self.wave = 0

        # The default cooldown for the zombie spawns
        self.zombie_cooldown = 30

    def update(self):
        self.collision()
        self.spawn_zombies()


        self.tick_lifespan += 1

        if self.tick_lifespan >= 60:
            self.tick_lifespan = 0
            self.seconds_lifespan += 1

    def collision(self):
        # The zombie collisions
        zombie_collision = pygame.sprite.spritecollide(self, self.game.all_zombies, False)
        for zombie in zombie_collision:

            # Checks that the zombie can attack
            if zombie.attack_cooldown <=0:
                zombie.attack_cooldown = 60
                self.health -= zombie.damage
            else:
                zombie.attack_cooldown -= 1

            # Checks if the monolith is dead
            if self.health <= 0:
                self.game.end = True

    # The method to spawn the zombies in the map
    def spawn_zombies(self):
        # Makes a zombie spawn cooldown that eventually gets faster
        if self.zombie_cooldown <= 0:
            self.zombie_cooldown = DEFAULT_ZOMBIE_COOLDOWN * (10/self.seconds_lifespan)

            # Calculate amount of reinforcements being spawned
            zombie_amount = round((ZOMBIE_SPAWN_PROBABILITY * self.game.monolith.tick_lifespan), 0) + 1
            zombie_amount = int(zombie_amount)

            for i in range(0, zombie_amount):
                # Calculate the location of the reinforcements being spawned
                location_x = random.randint(0, SCREEN_WIDTH)
                location_y = random.randint(0, SCREEN_HEIGHT)

                # Calculate health
                health = random.randint(1, 200)
                damage = random.randint(1, 50)

                zombie = Zombie(location_x, location_y, health, damage, False, self.game)
                self.game.all_sprites.add(zombie)
                self.game.all_zombies.add(zombie)
        else:
            self.zombie_cooldown -= 0.1
            print(self.zombie_cooldown)




# The zombie logic
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, health, damage,reinforcement, game):
        super(Zombie, self).__init__()

        # Sprite parameters
        self.image = pygame.surface.Surface((ZOMBIE_WIDTH, ZOMBIE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # To access the game
        self.game = game

        # extra zombie properties
        self.health = health
        self.movement_speed = BASE_MOVEMENT_SPEED * (50/self.health)
        self.damage = damage
        self.reinforcement = reinforcement
        self.attack_cooldown = 60


        # Target location's x and y
        self.target_x = self.game.monolith.rect.x + MONOLITH_WIDTH/2
        self.target_y = self.game.monolith.rect.y + MONOLITH_HEIGHT/2

        # Spawns reinforcements
        self.spawn_reinforcements()

    def update(self):
        self.move()


# The logic to spawn zombie reinforcements
    def spawn_reinforcements(self):
        if not self.reinforcement:
            # Calculate amount of reinforcements being spawned
            reinforcement_amount = round((REINFORCEMENT_PROBABILITY * self.game.monolith.seconds_lifespan), 0)
            reinforcement_amount = int(reinforcement_amount)


            for i in range(0,reinforcement_amount):
                # Calculate the location of the reinforcements being spawned
                location_x =random.randint(self.rect.x - 100,self.rect.x + 100)
                location_y =random.randint(self.rect.y - 100,self.rect.y + 100)

                # Calculate health
                health = random.randint(1,200)
                damage = random.randint(1,50)

                zombie = Zombie(location_x, location_y, health, damage, True, self.game)
                self.game.all_sprites.add(zombie)
                self.game.all_zombies.add(zombie)

    # The function for the zombie's movement logic
    def move(self):
        # The method that makes the sprite move to the desire location using vectors
        movement_vector = pygame.math.Vector2(self.target_x - self.rect.x, self.target_y - self.rect.y)

        # In a try incase the normalisation or movement fail (e.g. it is on the target and can't move anywhere else)
        try:
            # Normalises the vector
            movement_vector.normalize()
            # Re-scales the vector
            movement_vector.scale_to_length(self.movement_speed)
            # Moves the sprite
            self.rect.move_ip(movement_vector)
            # print('Vector: ', movement_vector)
        except:
            pass




class MenuCard(pygame.sprite.Sprite):
    def __init__(self, x, y, colour, game):
        super(MenuCard, self).__init__()

        # Menu card sprite parameters
        self.image = pygame.surface.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.colour = colour
        self.image.fill(self.colour)

        # To call upon the game when needed
        self.game = game

        # Sets a default mode
        self.mode = 'zombie_shooter'

        # Stops the card from bugging out when trying to change modes
        self.scroll_cooldown = 0

        # Stops the background constantly being changed and resized every frame when it doesn't need to
        self.background_changed = False

    def update(self):
        self.change_mode()
        self.update_background()

    # Updates the background based on what the card is
    def update_background(self):
        # Changes the background to the zombie shooter background
        if self.mode == 'zombie_shooter' and not self.background_changed:
            self.game.background = pygame.image.load("zombie_menu_background.png")
            self.game.background = pygame.transform.scale(self.game.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))
            self.background_changed = True


        # Changes the background to the 1v1 background
        elif self.mode == '1V1' and not self.background_changed:
            self.game.background = pygame.image.load("background.png")
            self.game.background = pygame.transform.scale(self.game.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))
            self.background_changed = True


# Checks for a certain key press and changes/selects the gamemode based on that
    def change_mode(self):
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        # Lets the user scroll through the gamemodes using a, d,  'space', 'left arrow' and 'right arrow'
        if (key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_a] or key[pygame.K_d] or key[pygame.K_SPACE]) and self.scroll_cooldown <= 0:

            # Resets the cooldown
            self.scroll_cooldown = 15

            # If it is the zombie shooter change it to the 1v1
            if self.mode == 'zombie_shooter':
                self.mode = '1V1'
                self.colour = 'red'
                self.image.fill(self.colour)

            # If it is the 1v1, change it to the zombie shooter
            elif self.mode == '1V1':
                self.mode = 'zombie_shooter'
                self.colour = 'green'
                self.image.fill(self.colour)
            self.background_changed = False

        # Lets the user select the gamemode
        elif mouse[0] or mouse[1]:
            self.on_click()

        # Adds 1 to the scrolling cooldown
        else:
            self.scroll_cooldown -= 1

    def on_click(self):
        if self.mode == 'zombie_shooter':
            self.game.reset()
            self.game.setup_zombie_shooter()
        elif self.mode == '1V1':
            self.game.reset()
            self.game.setup_1v1_shooter()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, colour, player1, game):
        super(Player, self).__init__()

        # player sprite parameters
        self.image = pygame.surface.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.image.fill(colour)

        # To access the game
        self.game = game

        # Player Definer
        self.is_player1 = player1

        # Trigger initialisation
        self.trigger = pygame.joystick.Joystick(0)
        self.trigger.init()



    def update(self):
        self.movement()

    def movement(self):
        key = pygame.key.get_pressed()
        ls_y = self.trigger.get_axis(1)
        ls_x = self.trigger.get_axis(0)

        if (self.is_player1 and key[pygame.K_w]) or (not self.is_player1 and ls_y < -0.3):
            self.rect.y -= PLAYER_SPEED
        if (self.is_player1 and key[pygame.K_a]) or (not self.is_player1 and ls_x < -0.3):
            self.rect.x -= PLAYER_SPEED

        if (self.is_player1 and key[pygame.K_s]) or (not self.is_player1 and ls_y > 0.3):
            self.rect.y += PLAYER_SPEED
        if (self.is_player1 and key[pygame.K_d]) or (not self.is_player1 and ls_x > 0.3):
            self.rect.x += PLAYER_SPEED

        self.clipping()

    def clipping(self):
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x >= SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLAYER_WIDTH

        if self.rect.y < 0:
            self.rect.y = 0

        elif self.rect.y > SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT



