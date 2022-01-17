import pygame
from sys import exit
from random import randint, choice
## from pygame.locals import *

# PLAYER CREATION

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_espera_1 = pygame.image.load('graphics/player/player_espera_3.png').convert_alpha()
		player_espera_2 = pygame.image.load('graphics/player/player_espera_2.png').convert_alpha()
		self.player_espera = [player_espera_1,player_espera_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/salto.png').convert_alpha()

		self.image = self.player_espera[self.player_index]
		self.rect = self.image.get_rect(midbottom = (400,200))
		self.gravity = 0

		# self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		# self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and self.rect.bottom >= 250:
			self.gravity = -20
			# self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 335:
			self.rect.bottom = 335

	def animation_state(self):
		if self.rect.bottom < 300: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_espera):self.player_index = 0
			self.image = self.player_espera[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

# CLOUD CREATION

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			nube_1 = pygame.image.load('graphics/nube/nube1.png').convert_alpha()
			nube_2 = pygame.image.load('graphics/nube/nube2.png').convert_alpha()
			self.frames = [nube_1,nube_2]
			y_pos = 150
		else:
			snail_1 = pygame.image.load('graphics/nube/nube1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/nube/nube1.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos  = 100

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

#SCORE CREATION

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Chuches: {current_time}',False,(64,64,64))
	score_rect = score_surf.get_rect(center = (120,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True


pygame.init()
screen = pygame.display.set_mode((800,400))
##DISPLAYSURF = pygame.display.set_mode((800,400), RESIZABLE)
pygame.display.set_caption('LA RANA COME LETRAS')
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/ITCKRIST.TTF", 50)
game_active = False
start_time = 0
score = 0
# bg_music = pygame.mixer.Sound('audio/music.wav')
# bg_music.play(loops = -1)
user_text = ""
input_rect =pygame.Rect(0,0,200,50)
color_input = pygame.Color("lightskyblue3")

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro screen
player_stand = pygame.image.load('graphics/player/player_espera_3.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Come Letras',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

text_surface = test_font.render(user_text, True, (255,255,255))

game_message = test_font.render('Aprieta espacio',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer  
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				user_text = user_text[:-1]
			user_text += event.unicode 

		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:
		screen.blit(sky_surface,(0,0))
		player.draw(screen)
		screen.blit(ground_surface,(0,300))
		score = display_score()
		
		
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		screen.fill((94,129,162))
		screen.blit(player_stand,player_stand_rect)

		screen.blit(text_surface, (0,0))
		pygame.draw.rect(screen, color_input, input_rect,2)

		score_message = test_font.render(f'Los chuches: {score}',False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)