import pygame

pygame.init()

WINDOW_X, WINDOW_Y = 500, 500

WINDOW = pygame.display.set_mode((WINDOW_X, WINDOW_Y))

pygame.display.set_caption("Sidewinder")

clock = pygame.time.Clock()

# amount of pixels wide in a cell
cell_width = 20

x_axis = 25
y_axis = 25

cell_size = 1

bg_color = (255, 225, 200)

grid_border_color = (225,200,175)

cell_list = []

for y_cell in range(y_axis):
	for x_cell in range(x_axis):
		individual_cell = pygame.Rect( (cell_width * x_cell * cell_size), (cell_width * y_cell * cell_size), cell_width * cell_size, cell_width * cell_size)
		print(individual_cell.x / cell_width, individual_cell.y / cell_width)
		cell_list.append(individual_cell)

cell_x, cell_y = 0, 0

# set fixed cell coordinates
for each_cell in cell_list:
	# dividing by cell width to get correct x and y of cells and not pixels
	each_cell_x = int(each_cell.x / cell_width)
	each_cell_y = int(each_cell.y / cell_width)

live_timer = pygame.time.get_ticks()
current_cell_count = 0
cell_highlight_duration = 5

target_cell_x, target_cell_y = 200, 200

player_cell = pygame.Rect(target_cell_x, target_cell_y, cell_width, cell_width)

bad_rectangle = pygame.Rect(10 * cell_width, 20 * cell_width, cell_width, cell_width)

moving_right = True
moving_down = False
moving_left = False
moving_up = False

running = True
while running:
	clock.tick(15)

	# draw background color
	WINDOW.fill(bg_color)
	player_cell.x = target_cell_x
	player_cell.y = target_cell_y

	pygame.draw.rect(WINDOW, (0, 255, 0), player_cell)

	# draw each individual cell
	for each_cell in cell_list:
		# draw borders
		pygame.draw.rect(WINDOW, grid_border_color, each_cell, 1, 0, 1)

	if moving_right:
		if target_cell_x + cell_width >= WINDOW_X:
			target_cell_x = 0
		else:
			target_cell_x += cell_width


	elif moving_down:
		if target_cell_y + cell_width >= WINDOW_Y:
			target_cell_y = 0
		else:
			target_cell_y += cell_width


	elif moving_left:
		if target_cell_x - cell_width < 0:
			target_cell_x = WINDOW_X
		else:
			target_cell_x -= cell_width


	elif moving_up:
		if target_cell_y + cell_width < 0:
			target_cell_y = WINDOW_Y
		else:
			target_cell_y -= cell_width

	pygame.draw.rect(WINDOW, (255,120,0), bad_rectangle)

	if player_cell.colliderect(bad_rectangle):
		print("Game over !")

	keys_pressed = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				print("Right")
				if moving_down or moving_up:
					moving_right = True
					moving_down= False
					moving_left = False
					moving_up = False
				
			if event.key == pygame.K_DOWN:
				print("Down")
				if moving_left or moving_right:
					moving_down = True
					moving_right= False
					moving_left = False
					moving_up = False
				
			if event.key == pygame.K_LEFT:
				print("Left")
				if moving_up or moving_down:
					moving_left = True
					moving_right= False
					moving_down = False
					moving_up = False
				
			if event.key == pygame.K_UP:
				print("Up")
				if moving_left or moving_right:
					moving_up = True
					moving_right= False
					moving_down = False
					moving_left = False
					
	pygame.display.update()