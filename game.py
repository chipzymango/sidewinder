import pygame

pygame.init()

WINDOW_X, WINDOW_Y = 500, 500

WINDOW = pygame.display.set_mode((WINDOW_X, WINDOW_Y))

pygame.display.set_caption("Snake game")

clock = pygame.time.Clock()

x_axis = 25
y_axis = 25

cell_size = 1

grid_border_color = (200,200,200)

bg_color = (250, 225, 200)

cell_list = []

for x_cell in range(x_axis):
	for y_cell in range(y_axis):
		individual_cell = pygame.Rect( (20 * x_cell * cell_size), (20 * y_cell * cell_size), 20 * cell_size, 20 * cell_size)
		print(individual_cell.x, individual_cell.y)
		cell_list.append(individual_cell)

running = True
while running:
	clock.tick(10)

	WINDOW.fill(bg_color)

	for each_cell in cell_list:
		pygame.draw.rect(WINDOW, grid_border_color, each_cell, 1, 0, 1)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

			pygame.draw.rect(WINDOW, (255,0,0), each_cell)

	pygame.display.update()