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

grid_border_color = (225,200,175)

bg_color = (255, 225, 200)

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

running = True
while running:
	clock.tick(60)

	# draw background color
	WINDOW.fill(bg_color)

	for cell in cell_list:
		if pygame.time.get_ticks() - live_timer > cell_highlight_duration:
			live_timer = pygame.time.get_ticks()

			if current_cell_count + 1 >= len(cell_list):
				current_cell_count = 0
			else:
				current_cell_count += 1
		else:
			pygame.draw.rect(WINDOW, (255,0,0,), cell_list[current_cell_count])

	# draw each individual cell
	for each_cell in cell_list:
		# draw borders
		pygame.draw.rect(WINDOW, grid_border_color, each_cell, 1, 0, 1)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	pygame.display.update()