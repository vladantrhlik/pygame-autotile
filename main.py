import pygame as pg
import math

pg.init()
screen = pg.display.set_mode([640, 640])
running = True

class Tile:
	def __init__(self, x, y, mask, image):
		self.mask = mask
		self.image = image

	def draw(self, screen, x, y, mask=False):
		screen.blit(self.image, (x,y))
		
		if mask:
			surf = pg.Surface((self.image.get_width(), self.image.get_height()))
			surf.set_alpha(100)
			
			size = self.image.get_width()/3

			for ypos,row in enumerate(self.mask):
				for xpos, m in enumerate(row):
					if m == 1:
						pg.draw.rect(surf, (255,0,0), (xpos * size, ypos * size, size, size))
			screen.blit(surf, (x,y))


class AutoTile:

	def __init__(self, tileset, tileSize):
		f = open("mask.txt").readlines()
		'''
		tile_mask = list(map(lambda x: list(map(lambda x: int(x), list(x.replace("\n", "")))), f[:5]))
		masks = list(map(lambda x: list(map(lambda x: int(x), list(x.replace("\n", "").replace(" ", "")))), f[6:]))
		'''
		tile_mask = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0]]
		masks = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0]]

		self.tileset = pg.image.load(tileset)
		self.tileSize = tileSize

		#self.directions =  [[[x,y] for x in range(-1,2,1)] for y in range(-1,2,1)]
		self.directions = [
			[[	[-1,0], [-1,-1], [0,-1]	], [[0,-1]], [	[0,-1], [1,-1], [1,0]	]],
			[[[-1,0]], [], [[1,0]]],
			[[	[-1,0],[-1,1],[0,1]	], [[0,1]], [	[1,0],[1,1],[0,1]	]]
		]

		self.tiles = []
		for y,row in enumerate(tile_mask):
			for x, tile in enumerate(row):
				if tile == 1:
					m = []
					for i in range(3):
						m.append(masks[y*3+i][x*3:x*3+3])

					surf = pg.Surface((self.tileSize, self.tileSize))
					surf.blit( self.tileset, (0, 0), (x * self.tileSize, y * self.tileSize, self.tileSize, self.tileSize) )

					self.tiles.append(Tile(x,y,m,surf))

	def getTile(self, mask):
		for t in self.tiles:
			if mask == t.mask:
				return t
		return None
	
	def renderMap(self, screen, map):
		for y,row in enumerate(map):
			for x, tile in enumerate(row):
				if tile == 1:
					mask = [[0,0,0],
							[0,1,0],
							[0,0,0]]
					for my in range(3):
						for mx in range(3):
							allDirections = self.directions[my][mx]
							valid = True
							for d in allDirections:
								if 0<=x+d[0]<len(map[0]) and 0<=y+d[1]<len(map):
									try:
										if map[y + d[1]][x + d[0]] == 0:
											valid = False
									except:
										valid = False
								else:
									valid = False

							if valid: mask[my][mx] = 1
					try:
						t = self.getTile(mask)
						t.draw(screen, x*self.tileSize, y*self.tileSize)
					except:
						t = self.tiles[11]
						t.draw(screen, x*self.tileSize, y*self.tileSize)


map = [[0 for x in range(10)] for y in range(10)]

autotile = AutoTile("tilemap.png", 16)

while running:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
	
	pos = pg.mouse.get_pos()
	x = math.floor(pos[0]/64)
	y = math.floor(pos[1]/64)

	color = [255,255,255]

	if pg.mouse.get_pressed()[0] == 1:
		map[y][x] = 1
	elif pg.mouse.get_pressed()[2] == 1:
		map[y][x] = 0
		color = [255,0,0]

	screen.fill((40,40,40))

	surf = pg.Surface((160,160))
	autotile.renderMap(surf, map)
	screen.blit(pg.transform.scale(surf, (640,640)), (0,0))

	cursor = pg.Surface((64,64), pg.SRCALPHA, 32)
	cursor.fill(color + [100])

	screen.blit(cursor, (x*64,y*64))

	pg.display.flip()

pg.quit()