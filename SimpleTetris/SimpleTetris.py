import pygame
import random

pygame.init()

screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
]

shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
]

def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(colors[1:])
        self.rotation = 0

    @property
    def image(self):
        rotated_shape = self.shape
        for _ in range(self.rotation):
            rotated_shape = rotate_shape(rotated_shape)
        return rotated_shape

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4  

class Tetris:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[0] * width for _ in range(height)]
        self.score = 0
        self.game_over = False
        self.current_piece = self.new_piece()

    def new_piece(self):
        return Piece(3, 0, random.choice(shapes))

    def valid_move(self, shape, offset):
        off_x, off_y = offset
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if x + off_x < 0 or x + off_x >= self.width or y + off_y >= self.height:
                        return False
                    if self.board[y + off_y][x + off_x]:
                        return False
        return True

    def clear_lines(self):
        lines = 0
        for i, row in enumerate(self.board):
            if all(row):
                del self.board[i]
                self.board.insert(0, [0 for _ in range(self.width)])
                lines += 1
        self.score += lines ** 2

    def drop(self):
        if not self.game_over:
            self.current_piece.y += 1
            if not self.valid_move(self.current_piece.image, (self.current_piece.x, self.current_piece.y)):
                self.current_piece.y -= 1
                self.freeze()

    def freeze(self):
        for y, row in enumerate(self.current_piece.image):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.current_piece.y][x + self.current_piece.x] = self.current_piece.color
        self.clear_lines()
        self.current_piece = self.new_piece()
        if not self.valid_move(self.current_piece.image, (self.current_piece.x, self.current_piece.y)):
            self.game_over = True

    def move(self, dx):
        if not self.game_over:
            new_x = self.current_piece.x + dx
            if self.valid_move(self.current_piece.image, (new_x, self.current_piece.y)):
                self.current_piece.x = new_x

    def rotate(self):
        if not self.game_over:
            old_rotation = self.current_piece.rotation  
            self.current_piece.rotate()
            if not self.valid_move(self.current_piece.image, (self.current_piece.x, self.current_piece.y)):
                self.current_piece.rotation = old_rotation  

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, pygame.Rect(x * 30, y * 30, 30, 30))
        for y, row in enumerate(self.current_piece.image):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_piece.color, pygame.Rect((self.current_piece.x + x) * 30, (self.current_piece.y + y) * 30, 30, 30))

        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = Tetris(20, 10)
    counter = 0

    while True:
        if game.game_over:
            break

        counter += 1
        if counter % 5 == 0:
            game.drop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move(1)
                elif event.key == pygame.K_DOWN:
                    game.drop()
                elif event.key == pygame.K_UP:
                    game.rotate()

        game.draw(screen)
        clock.tick(10)

    print(f"Norm graesh! Tvii rezultat: {game.score}")

if __name__ == '__main__':
    main()
    pygame.quit()
