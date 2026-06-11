import pygame.sprite

from config import *

# Monolith's class sprite
class Monolith(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super(Monolith, self).__init__()

        # Sprite parameters
        self.image = MONOLITH_IMAGE
        self.image = pygame.transform.scale(self.image, (MONOLITH_WIDTH, MONOLITH_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Fills the colour if the images failed to load
        if IMAGE_LOADING_FAILED:
            self.image.fill((156, 156, 156))

        self.game = game # Lets it access the game class

        # This is the monolith's health
        self.health = 1000

        # All the time difficulty parameters
        self.tick_lifespan = 0
        self.seconds_lifespan = 0

        # Wave settings
        self.wave = 0
        self.wave_duration = 10
        self.wave_cooldown = 10
        self.wave_difficulty = 2

        # The default cooldown for the zombie spawns
        self.zombie_cooldown = 30

    # calls all the sprite's methods that need updating
    def update(self):
        self.collision()
        self.spawn_zombies()
        self.waves_controller()

        # Ticks to seconds
        self.tick_lifespan += 1
        if self.tick_lifespan >= 60:
            self.tick_lifespan = 0
            self.seconds_lifespan += 1

    def collision(self):
        # The zombie collisions
        zombie_collisions = pygame.sprite.spritecollide(self, self.game.all_zombies, False)
        for zombie in zombie_collisions:
            zombie.at_target = True

            # Checks that the zombie can attack
            if zombie.attack_cooldown <=0:
                zombie.attack_cooldown = 60
                self.health -= zombie.damage
            else:
                zombie.attack_cooldown -= 1

            # Checks if the monolith is dead
            if self.health <= 0:
                self.health = 0
                self.game.end = True

        wall_collisions = pygame.sprite.spritecollide(self,self.game.all_walls,True)
        for wall in wall_collisions:
            if wall.is_player1:
                self.game.player1.wall_materials += 2
            else:
                self.game.player2.wall_materials += 2

    # The method to spawn the zombies in the map
    def spawn_zombies(self):
        # Makes a zombie spawn cooldown that eventually gets faster
        if self.zombie_cooldown <= 0:
            self.zombie_cooldown = DEFAULT_ZOMBIE_COOLDOWN * (10/(self.wave_difficulty/3))
            # print(self.zombie_cooldown)

            # Calculate Static zombie spawning value
            zombie_amount = 1

            if zombie_amount > 0: # Makes sure it doesn't error out when no zombies are selected
                zombie_amount = random.randint(1,zombie_amount)
                # Calculate parameters and spawn the zombies
                for i in range(0, zombie_amount):
                    # Calculate the location of the reinforcements being spawned
                    location_x = random.randint(0, SCREEN_WIDTH)
                    location_y = random.randint(0, SCREEN_HEIGHT)

                    # Calculate health
                    health = random.randint(1, 200)
                    damage = random.randint(1, 50)

                    # Creates the zombie and adds it to the sprite groups
                    zombie = Zombie(location_x, location_y, health, damage, False, self.game)
                    self.game.all_sprites.add(zombie)
                    self.game.all_zombies.add(zombie)
        else:
            self.zombie_cooldown -= 0.1 # takes 0.1 from the cooldown if it doesn't spawn a zombie
            #print(self.zombie_cooldown)

    # Controls the zombie spawning and makes it spawn in waves
    def waves_controller(self):
        # Checks if the wave is on cooldown (no zombies spawn)
        if self.seconds_lifespan >= self.wave_duration and self.wave_cooldown > 0:
            self.wave_cooldown -= 1/60
            self.zombie_cooldown = 1 # Makes the zombies not spawn by never letting the timer run out

        # Runs once the wave cooldown is over
        elif self.wave_cooldown <= 0:
            # Resets all values and increases the difficulty
            self.wave_duration += 22
            self.wave_cooldown = 10
            self.wave += 1
            self.wave_difficulty += 5


# The zombie logic
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, health, damage,reinforcement, game):
        super(Zombie, self).__init__()

        # Sprite parameters
        self.image = pygame.surface.Surface((ZOMBIE_WIDTH, ZOMBIE_HEIGHT))
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0))
        self.rect.center = (x, y)

        # To access the game
        self.game = game

        # extra zombie properties
        self.health = health
        self.movement_speed = BASE_MOVEMENT_SPEED * (50/self.health)
        if self.movement_speed >= BASE_MOVEMENT_SPEED * 2:
            self.movement_speed = BASE_MOVEMENT_SPEED * 2
        self.damage = damage
        self.reinforcement = reinforcement
        self.attack_cooldown = 60
        self.at_target  = False

        # Target location's x and y
        self.target_x = self.game.monolith.rect.x + MONOLITH_WIDTH/2
        self.target_y = self.game.monolith.rect.y + MONOLITH_HEIGHT/2

        # Spawns reinforcements
        self.spawn_reinforcements()

    def update(self):
        if not self.at_target:
            self.move()
        self.collision()


# The logic to spawn zombie reinforcements
    def spawn_reinforcements(self):
        if not self.reinforcement:
            # Calculate amount of reinforcements being spawned
            reinforcement_amount = ((random.uniform(0,0.06) / (10/(self.game.monolith.wave_difficulty/3)))* 100)/2
            # print('Reinforcement: ',reinforcement_amount)
            # print('Wave: ',self.game.monolith.wave)
            reinforcement_amount = round(reinforcement_amount,0)
            # print('Rounded amount: ', reinforcement_amount)
            reinforcement_amount = int(reinforcement_amount)

            # Caps the amount of reinforcements that are able to spawn at 10
            if reinforcement_amount > 10:
                reinforcement_amount = 10

            # Spawns the amount of reinforcements that need spawning
            for i in range(0,reinforcement_amount):
                # Calculate the location of the reinforcements being spawned
                location_x =random.randint(self.rect.x - 100,self.rect.x + 100)
                location_y =random.randint(self.rect.y - 100,self.rect.y + 100)

                # Calculate health
                health = random.randint(1,200)
                damage = random.randint(1,50)

                # Spawns the reinforcement zombie
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

    def collision(self):
        bullet_collisions = pygame.sprite.spritecollide(self, self.game.all_bullets, True)
        for bullet in bullet_collisions:
            self.health -= BULLET_DAMAGE

            if self.health <= 0:
                self.game.all_sprites.remove(self)
                self.game.all_zombies.remove(self)


# Pointer class
class Pointer(pygame.sprite.Sprite):
    def __init__(self, is_player_1, x, y, game):
        super(Pointer, self).__init__()

        # Check for player 1
        self.is_player_1 = is_player_1

        # Apply correct icon
        if self.is_player_1:
            self.image = PLAYER_2_POINTER_IMAGE
            if IMAGE_LOADING_FAILED:
                self.image.fill((255,137,0))         # Fills the colour if the images failed to load
        else:
            self.image = PLAYER_1_POINTER_IMAGE
            if IMAGE_LOADING_FAILED:
                self.image.fill((0, 145, 255))         # Fills the colour if the images failed to load

        self.image = pygame.transform.scale(self.image, (POINTER_WIDTH, POINTER_HEIGHT))

        # Sort out parameters
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Trigger initialisation
        if pygame.joystick.get_count() < 1:
            print('please connect a joystick')
            self.trigger = None
        else:
            self.trigger = pygame.joystick.Joystick(0)
            self.trigger.init()

        self.game = game # Lets the object access the main game class

    def update(self):
        self.move()
        self.clipping()

    def move(self):
        # Move player 1's pointer
        if  self.is_player_1:
            self.rect.x,self.rect.y = pygame.mouse.get_pos()
            self.rect.x -= POINTER_WIDTH / 2
            self.rect.y -= POINTER_HEIGHT / 2

        # Move player 2's pointer
        else:
            # Make sure there is an appropriate value if there is not the controller connected
            if self.trigger is not None:
                # Get joystick values
                rs_y = self.trigger.get_axis(2)
                rs_x = self.trigger.get_axis(3)
            else:
                rs_y = 0
                rs_x = 0

            # Check inputs and move pointer appropriately
            if rs_x < -0.3:
                self.rect.y -= POINTER_SENSITIVITY
            if rs_y < -0.3:
                self.rect.x -= POINTER_SENSITIVITY

            if rs_x > 0.3:
                self.rect.y += POINTER_SENSITIVITY
            if rs_y > 0.3:
                self.rect.x += POINTER_SENSITIVITY

    # This handles the screen clipping and borders for the player
    def clipping(self):
        # Right and left screen border
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x >= SCREEN_WIDTH - POINTER_WIDTH:
            self.rect.x = SCREEN_WIDTH - POINTER_WIDTH
        # Top and bottom screen border
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_HEIGHT -POINTER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - POINTER_HEIGHT


class MenuCard(pygame.sprite.Sprite):
    def __init__(self, x, y, colour, game):
        super(MenuCard, self).__init__()

        # Menu card sprite parameters
        self.image = pygame.surface.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.colour = colour
        self.image = ZOMBIE_SHOOTER_MENU_CARD
        self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        # Fills the colour if the images failed to load
        if IMAGE_LOADING_FAILED:
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
            self.game.background = ZOMBIE_SHOOTER_BACKGROUND
            self.game.background = pygame.transform.scale(self.game.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))

            # Fills the colour if the images failed to load
            if IMAGE_LOADING_FAILED:
                self.game.background.fill((112,112,112))

            self.background_changed = True


        # Changes the background to the 1v1 background
        elif self.mode == '1V1' and not self.background_changed:
            self.game.background = GRASSY_BACKGROUND
            self.game.background = pygame.transform.scale(self.game.background, (BG_IMAGE_SIZE[0], BG_IMAGE_SIZE[1]))

            # Fills the colour if the images failed to load
            if IMAGE_LOADING_FAILED:
                self.game.background.fill((112,112,112))

            self.background_changed = True


# Checks for a certain key press and changes/selects the gamemode based on that
    def change_mode(self):
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        # Lets the user scroll through the gamemodes using a, d,  'space', 'left arrow' and 'right arrow'
        if (key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_a] or key[pygame.K_d]) and self.scroll_cooldown <= 0:

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
                self.image = ZOMBIE_SHOOTER_MENU_CARD
                self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
                # Fills the colour if the images failed to load
                if IMAGE_LOADING_FAILED:
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
            self.game.sprite_reset()
            self.game.setup_zombie_shooter()
        elif self.mode == '1V1' and not self.game.single_player:
            self.game.sprite_reset()
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
        if pygame.joystick.get_count() < 1:
            print('please connect a joystick')
            self.trigger = None
        else:
            self.trigger = pygame.joystick.Joystick(0)
            self.trigger.init()

        # Shoot
        self.shoot_cooldown = BULLET_COOLDOWN

        # Materials
        self.wall_materials = 6
        self.build_cooldown = 10

        # Player's health
        self.health = 500

    # Update class
    def update(self):
        self.movement()
        self.clipping()
        self.shooting()
        self.building()
        self.collision()

    # Player Movement
    def movement(self):
        key = pygame.key.get_pressed() # Gets the current pressed key

        # Makes sure nothing happens if there is no controller connected
        # Gets the controller input if a controller is connected
        if self.trigger is not None:
            ls_y = self.trigger.get_axis(1)
            ls_x = self.trigger.get_axis(0)
        else:
            ls_y = 0
            ls_x = 0

        # Handles the player's movement checks and makes sure the triggers and buttons correlate to the correct movement
        if (self.is_player1 and key[pygame.K_w]) or (not self.is_player1 and ls_y < -0.3):
            self.rect.y -= PLAYER_SPEED
        if (self.is_player1 and key[pygame.K_a]) or (not self.is_player1 and ls_x < -0.3):
            self.rect.x -= PLAYER_SPEED
        if (self.is_player1 and key[pygame.K_s]) or (not self.is_player1 and ls_y > 0.3):
            self.rect.y += PLAYER_SPEED
        if (self.is_player1 and key[pygame.K_d]) or (not self.is_player1 and ls_x > 0.3):
            self.rect.x += PLAYER_SPEED

    # Handles the player's shooting
    def shooting(self):
        mouse = pygame.mouse.get_pressed()
        if self.trigger is not None:
            rt = self.trigger.get_axis(5)
        else:
            rt = 0

        # Handles the shooting for player 1
        if mouse[0] and self.is_player1 and self.shoot_cooldown <= 0:
            # Creates player 1's bullet and adds it to all sprites
            bullet = Bullet(self.rect.centerx, self.rect.centery, True, self.game)
            self.game.all_sprites.add(bullet)
            self.game.all_bullets.add(bullet)

            # Resets the shooting cooldown
            self.shoot_cooldown = BULLET_COOLDOWN

        # Handles the shooting for player 2
        elif rt >=0.5 and not self.is_player1 and self.shoot_cooldown <= 0:
            # Creates player 2's bullet and adds it to all sprites
            bullet = Bullet(self.rect.centerx, self.rect.centery, False, self.game)
            self.game.all_sprites.add(bullet)
            self.game.all_bullets.add(bullet)

            # Resets the shooting cooldown
            self.shoot_cooldown = BULLET_COOLDOWN

            # reduces the cooldown
        else:
            self.shoot_cooldown -= 1

# Lets the player build on right trigger or left click
    def building(self):
        mouse = pygame.mouse.get_pressed()
        if self.trigger is not None:
            lt = self.trigger.get_axis(4)
            a_pressed = self.trigger.get_button(0) # Gets the A button pressed state
        else:
            lt = 0
            a_pressed = False

        # Player 1 building and walls snapping to grid
        if mouse[2]and self.is_player1 and self.wall_materials >= 2:
            self.wall_materials -= 2
            center_x = (self.game.pointer1.rect.centerx// GRID_SIZE)
            center_y = (self.game.pointer1.rect.centery// GRID_SIZE)

            center_x = (center_x * GRID_SIZE) + WALL_WIDTH/2
            center_y =  (center_y * GRID_SIZE) + WALL_HEIGHT/2

            wall = Wall(center_x, center_y, True,False, self.game)
            self.game.all_sprites.add(wall)
            self.game.all_walls.add(wall)

            self.build_cooldown = 10

        # Player2 building and walls snapping to grid
        elif lt >= 0.3 and not self.is_player1 and self.wall_materials >= 2:
            self.wall_materials -= 2

            center_x = (self.game.pointer2.rect.centerx // GRID_SIZE)
            center_y = (self.game.pointer2.rect.centery // GRID_SIZE)

            center_x = (center_x * GRID_SIZE) + WALL_WIDTH/2
            center_y =  (center_y * GRID_SIZE) + WALL_HEIGHT/2

            wall = Wall(center_x, center_y, False,False, self.game)
            self.game.all_sprites.add(wall)
            self.game.all_walls.add(wall)

            self.build_cooldown = 10

        self.build_cooldown -= 1

        # Player 1 breaking walls
        if mouse[1] and self.is_player1:
            center_x = (self.game.pointer1.rect.centerx // GRID_SIZE)
            center_y = (self.game.pointer1.rect.centery // GRID_SIZE)

            center_x = (center_x * GRID_SIZE) + WALL_WIDTH / 2
            center_y = (center_y * GRID_SIZE) + WALL_HEIGHT / 2

            wall = Wall(center_x, center_y, True, True, self.game)
            self.game.all_breakers.add(wall)

        # Player 2 breaking walls
        elif a_pressed and not self.is_player1:
            center_x = (self.game.pointer1.rect.centerx // GRID_SIZE)
            center_y = (self.game.pointer1.rect.centery // GRID_SIZE)

            center_x = (center_x * GRID_SIZE) + WALL_WIDTH / 2
            center_y = (center_y * GRID_SIZE) + WALL_HEIGHT / 2

            wall = Wall(center_x, center_y, False, True, self.game)
            self.game.all_breakers.add(wall)


    # Player collisions
    def collision(self):
        # Checks if the player has collided with the wall material
        collided_wall_materials = pygame.sprite.spritecollide(self, self.game.all_materials, True)
        for wall_material in collided_wall_materials:
            # Gives the player a random amount of materials from 1-3
            self.wall_materials += random.randint(1,3)

        # Checks if the player has collided with a bullet
        collided_bullets = pygame.sprite.spritecollide(self,self.game.all_bullets, False)
        for bullet in collided_bullets:
            # Makes sure it is the right gamemode and the player is
            if self.game.menu_card.mode == '1V1':
                if (self.is_player1 and not bullet.is_player1) or (not self.is_player1 and bullet.is_player1):
                    self.health -= BULLET_DAMAGE

                    self.game.all_sprites.remove(bullet)
                    self.game.all_bullets.remove(bullet)

        # Determines the winner
        if self.health <=0:
            self.health = 0
            self.game.end = True
            if self.is_player1:
                self.game.winner = 'Player2'
            else:
                self.game.winner = 'Player1'


# This handles the screen clipping and borders for the player
    def clipping(self):

        # Right and left screen border
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x >= SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLAYER_WIDTH

        # Top and bottom screen border
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT


# This  is the bullet class. it controls the bullet's movement and trajectory
class Bullet(pygame.sprite.Sprite):
    def __init__(self, starting_x, starting_y, player1, game):
        super(Bullet, self).__init__()

        # Sprite perameters
        self.image = pygame.surface.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill((64, 64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = starting_x, starting_y
        self.is_player1 = player1
        self.game = game

        # makes sure it is going to the right pointer
        if self.is_player1:
            self.ending_x,self.ending_y = self.game.pointer1.rect.center
        else:
            self.ending_x,self.ending_y = self.game.pointer2.rect.center


        # Calculates the angle (in radians) for the bullet to travel along
        x_difference = self.ending_x - starting_x
        y_difference = self.ending_y - starting_y
        angle = math.atan2(y_difference, x_difference)

        # Calculate the change in x and change in y that we need to do every step
        self.move_x = math.cos(angle) * BULLET_VELOCITY
        self.move_y = math.sin(angle) * BULLET_VELOCITY

        self.lifespan = BULLET_LIFESPAN

    def update(self):
        self.move()

    def move(self):
        self.rect.x += self.move_x
        self.rect.y += self.move_y

class Wall(pygame.sprite.Sprite):
    def __init__(self, starting_x, starting_y, is_player1,breaker, game):
        super(Wall, self).__init__()

        self.image = WALL_IMAGE
        self.image = pygame.transform.scale(self.image, (WALL_WIDTH, WALL_HEIGHT))
        # Fills the colour if the images failed to load
        if IMAGE_LOADING_FAILED:
            self.image.fill((148, 99, 0))
        self.rect = self.image.get_rect()
        self.rect.center = starting_x, starting_y
        self.breaker = breaker

        # the wall's health
        self.health = 3

        self.game = game
        self.is_player1 = is_player1


# Walls update class
    def update(self):
        self.collisions()

        self.game.all_breakers = pygame.sprite.Group()

# Checks for collisions
    def collisions(self):

        # Collisions with zombies
        zombie_collisions = pygame.sprite.spritecollide(self,self.game.all_zombies, False)
        for zombie in zombie_collisions:
            zombie.at_target = True

            # Checks that the zombie can attack
            if zombie.attack_cooldown <=0:
                zombie.attack_cooldown = 60
                self.health -= 1
            else:
                zombie.attack_cooldown -= 1

            # destroys wall if health is gone
            if self.health <= 0:
                # Lets the zombie(s) move again
                for zombie_need_moving in zombie_collisions:
                    zombie_need_moving.at_target = False

        # Collisions with bullets
        bullet_collisions = pygame.sprite.spritecollide(self,self.game.all_bullets, False)
        for bullet in bullet_collisions:
            if self.game.menu_card.mode == '1V1':
                if bullet.is_player1 is not self.is_player1:
                    self.health -= 1
                    self.game.all_sprites.remove(bullet)
                    self.game.all_bullets.remove(bullet)

        wall_collisions = pygame.sprite.spritecollide(self,self.game.all_walls, False)
        for wall in wall_collisions:
            if wall != self:
                if wall.is_player1:
                    self.game.player1.wall_materials += 2
                else:
                    self.game.player2.wall_materials += 2
                self.game.all_sprites.remove(wall)
                self.game.all_walls.remove(wall)

        breaker_collisions = pygame.sprite.spritecollide(self,self.game.all_breakers, False)
        for breaker in breaker_collisions:
            if not self.breaker:
                if breaker.is_player1:
                    self.game.player1.wall_materials += 1
                else:
                    self.game.player2.wall_materials += 1
                self.game.all_sprites.remove(self)
                self.game.all_walls.remove(self)

        # destroys wall if health is gone
        if self.health <= 0:
            self.game.all_sprites.remove(self)
            self.game.all_walls.remove(self)


class WallMaterial(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super(WallMaterial, self).__init__()

        self.image = pygame.surface.Surface((WALL_ITEM_WIDTH, WALL_ITEM_HEIGHT))
        self.image.fill((71, 40, 1))
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.game = game
