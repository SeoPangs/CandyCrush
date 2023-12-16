# 게임을 시작하면 생성될 맵에 대한 알고리즘
# 처음 만들 맵에 대한 내용이다.
#   시작할 때부터 이미 같은 색이 3개가 모여있는 경우가 있다.
#   처음에 이런 상황을 배제하기 위해 레벨제네레이터를 유전자함수를 통해 제작한다.

# 만들어야할것

# 적합도함수
#    = 100 * Match가 되는 블록의 수 / 전체 블록의 수
#   시작할 때부터 이미 3개가 모여있는 블록의 수다.

#변이
#교차
#선택함수

#그래서 적합도가 100인 모델을 만들어서 그 중 일부를 사용할 수 있게 한다.

#레벨 자체는 N의 크기라고 가정한다.
#반환은 일단 N의 크기를 가진 사이즈라고 하자


"""
    두번째
        유전자 함수 구성

        유전자 구성
    		(a, b)의 노드를 (방향)으로.
        적합도 평가
        선택
        교차
        돌연변이
"""

import pygame
from pygame.locals import *
import random
import numpy as np

#AutoMode가 활성화되면 마우스 입력이 활성화 되지 않는다.
bAutoMode = True

pygame.init()

# create the game window
width = 400
height = 400
scoreboard_height = 25
window_size = (width, height + scoreboard_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Match Three with Artificial Intelligence')
pygame.display.set_icon(pygame.image.load("swirl_blue.png"))

# list of candy colors
candy_colors = ['blue', 'green', 'orange', 'pink', 'purple', 'red', 'teal', 'yellow']

# candy size
candy_width = 40
candy_height = 40
candy_size = (candy_width, candy_height)

class Candy:
    
    def __init__(self, row_num, col_num):
        
        # set the candy's position on the board
        self.row_num = row_num
        self.col_num = col_num
        
        #여기 부분에서 유전자 모델을 심어놔야 할 것 같은데 말이야.
        self.match = set()
        # assign a random image
        self.color = random.choice(candy_colors)
        image_name = f'swirl_{self.color}.png'
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.smoothscale(self.image, candy_size)
        self.rect = self.image.get_rect()
        self.rect.left = col_num * candy_width
        self.rect.top = row_num * candy_height
        
    # draw the image on the screen
    def draw(self):
        screen.blit(self.image, self.rect)
        
    # snap the candy to its position on the board
    def snap(self):
        self.snap_row()
        self.snap_col()
        
    def snap_row(self):
        self.rect.top = self.row_num * candy_height
        
    def snap_col(self):
        self.rect.left = self.col_num * candy_width
        
# create the board of candies
board = []
# board: List, Candy로 이루어진 이중배열   
# board[n][n]: n번째 있는 Candy의 값.

for row_num in range(height // candy_height):
    
    # add a new row to the board
    board.append([])
    
    for col_num in range(width // candy_width):
        
        # create the candy and add it to the board
        candy = Candy(row_num, col_num)
        board[row_num].append(candy)
        
def draw():
    
    # draw the background
    pygame.draw.rect(screen, (173, 216, 230), (0, 0, width, height + scoreboard_height))
    
    # draw the candies
    for row in board:
        for candy in row:
            candy.draw()
    
    # display the score and moves
    font = pygame.font.SysFont('monoface', 18)
    score_text = font.render(f'Score: {score}', 1, (0, 0, 0))
    score_text_rect = score_text.get_rect(center=(width / 4, height + scoreboard_height / 2))
    screen.blit(score_text, score_text_rect)
    
    moves_text = font.render(f'Moves: {moves}', 1, (0, 0, 0))
    moves_text_rect = moves_text.get_rect(center=(width * 3 / 4, height + scoreboard_height / 2))
    screen.blit(moves_text, moves_text_rect)
    
# swap the positions of two candies
def swap(candy1, candy2):
    
    temp_row = candy1.row_num
    temp_col = candy1.col_num
    
    candy1.row_num = candy2.row_num
    candy1.col_num = candy2.col_num
    
    candy2.row_num = temp_row
    candy2.col_num = temp_col
    
    # update the candies on the board list
    board[candy1.row_num][candy1.col_num] = candy1
    board[candy2.row_num][candy2.col_num] = candy2
    
    # snap them into their board positions
    candy1.snap()
    candy2.snap()
    
# find neighboring candies that match the candy's color
def find_matches(candy, matches):
    
    # add the candy to the set
    matches.add(candy)
    
    # check the candy above if it's the same color
    if candy.row_num > 0:
        neighbor = board[candy.row_num - 1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches))
            
    # check the candy below if it's the same color
    if candy.row_num < height / candy_height - 1:
        neighbor = board[candy.row_num + 1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches))
            
    # check the candy to the left if it's the same color
    if candy.col_num > 0:
        neighbor = board[candy.row_num][candy.col_num - 1]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches))
            
    # check the candy to the right if it's the same color
    if candy.col_num < width / candy_width - 1:
        neighbor = board[candy.row_num][candy.col_num + 1]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches))
            
    return matches
    
# return a set of at least 3 matching candies or an empty set
def match_three(candy):
    
    matches = find_matches(candy, set())
    if len(matches) >= 3:
        return matches
    else:
        return set()
        


def get_random_neighbor(candy):
    neighbors = []

    # 위
    if candy.row_num > 0:
        neighbors.append(board[candy.row_num - 1][candy.col_num])

    # 아래
    if candy.row_num < height // candy_height - 1:
        neighbors.append(board[candy.row_num + 1][candy.col_num])

    # 왼쪽
    if candy.col_num > 0:
        neighbors.append(board[candy.row_num][candy.col_num - 1])

    # 오른쪽
    if candy.col_num < width // candy_width - 1:
        neighbors.append(board[candy.row_num][candy.col_num + 1])

    return random.choice(neighbors) if neighbors else None

# 추가된 함수: 인공지능이 랜덤으로 주변 캔디를 스왑하는 함수
def swap_by_ai():
    global moves
    candy = random.choice([candy for row in board for candy in row])

    # 주변의 캔디를 무작위로 선택
    neighbor_candy = get_random_neighbor(candy)

    if neighbor_candy:
        # 스왑 수행
        swap(candy, neighbor_candy)
        matches.update(match_three(candy))
        matches.update(match_three(neighbor_candy))
        moves += 1



# 추가된 코드: 타이머 설정을 위한 변수
swap_timer = pygame.USEREVENT + 1
pygame.time.set_timer(swap_timer, 1000)  # 1초(1000ms)마다 타이머 이벤트 발생
  
# candy that the user clicked on
clicked_candy = None

# the adjacent candy that will be swapped with the clicked candy
swapped_candy = None

# coordinates of the point where the user clicked on
click_x = None
click_y = None

# game variables
score = 0
moves = 0

# game loop
clock = pygame.time.Clock()
running = True


#게임 루프가 여기서 이뤄집니다.
while running:
    
    # set of matching candies
    matches = set()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == swap_timer:
            swap_by_ai()

        if not bAutoMode:
            # detect mouse click
            if clicked_candy is None and event.type == MOUSEBUTTONDOWN:
                
                # get the candy that was clicked on
                for row in board:
                    for candy in row:
                        if candy.rect.collidepoint(event.pos):
                            
                            clicked_candy = candy
                            
                            # save the coordinates of the point where the user clicked
                            click_x = event.pos[0]
                            click_y = event.pos[1]
                            
            # detect mouse motion
            if clicked_candy is not None and event.type == MOUSEMOTION:
                
                # calculate the distance between the point the user clicked on
                # and the current location of the mouse cursor
                distance_x = abs(click_x - event.pos[0])
                distance_y = abs(click_y - event.pos[1])
                
                # reset the position of the swapped candy if direction of mouse motion changed
                if swapped_candy is not None:
                    swapped_candy.snap()
                    
                # determine the direction of the neighboring candy to swap with
                if distance_x > distance_y and click_x > event.pos[0]:
                    direction = 'left'
                elif distance_x > distance_y and click_x < event.pos[0]:
                    direction = 'right'
                elif distance_y > distance_x and click_y > event.pos[1]:
                    direction = 'up'
                else:
                    direction = 'down'
                    
                # if moving left/right, snap the clicked candy to its row position
                # otherwise, snap it to its col position
                if direction in ['left', 'right']:
                    clicked_candy.snap_row()
                else:
                    clicked_candy.snap_col()
                    
                # if moving the clicked candy to the left,
                # make sureit's not on the first col
                if direction == 'left' and clicked_candy.col_num > 0:
                    
                    # get the candy to the left
                    swapped_candy = board[clicked_candy.row_num][clicked_candy.col_num - 1]
                    
                    # move the two candies
                    clicked_candy.rect.left = clicked_candy.col_num * candy_width - distance_x
                    swapped_candy.rect.left = swapped_candy.col_num * candy_width + distance_x
                    
                    # snap them into their new positions on the board
                    if clicked_candy.rect.left <= swapped_candy.col_num * candy_width + candy_width / 4:
                        swap(clicked_candy, swapped_candy)
                        matches.update(match_three(clicked_candy))
                        matches.update(match_three(swapped_candy))
                        moves += 1
                        clicked_candy = None
                        swapped_candy = None
                        #테스트 부분입니다.
                        print("왼쪽으로 Swap 성공")
                        
                # if moving the clicked candy to the right,
                # make sure it's not on the last col
                if direction == 'right' and clicked_candy.col_num < width / candy_width - 1:
                    
                    # get the candy to the right
                    swapped_candy = board[clicked_candy.row_num][clicked_candy.col_num + 1]
                    
                    # move the two candies
                    clicked_candy.rect.left = clicked_candy.col_num * candy_width + distance_x
                    swapped_candy.rect.left = swapped_candy.col_num * candy_width - distance_x
                    
                    # snap them into their new positions on the board
                    if clicked_candy.rect.left >= swapped_candy.col_num * candy_width - candy_width / 4:
                        swap(clicked_candy, swapped_candy)
                        matches.update(match_three(clicked_candy))
                        matches.update(match_three(swapped_candy))
                        moves += 1
                        clicked_candy = None
                        swapped_candy = None
                        #테스트 부분입니다.
                        print("오른쪽으로 Swap 성공")
                        
                # if moving the clicked candy up,
                # make sure it's not on the first row
                if direction == 'up' and clicked_candy.row_num > 0:
                    
                    # get the candy above
                    swapped_candy = board[clicked_candy.row_num - 1][clicked_candy.col_num]
                    
                    # move the two candies
                    clicked_candy.rect.top = clicked_candy.row_num * candy_height - distance_y
                    swapped_candy.rect.top = swapped_candy.row_num * candy_height + distance_y
                    
                    # snap them into their new positions on the board
                    if clicked_candy.rect.top <= swapped_candy.row_num * candy_height + candy_height / 4:
                        swap(clicked_candy, swapped_candy)
                        matches.update(match_three(clicked_candy))
                        matches.update(match_three(swapped_candy))
                        moves += 1
                        clicked_candy = None
                        swapped_candy = None
                        #테스트 부분입니다.
                        print("위쪽으로 Swap 성공")
                        
                # if moving the clicked candy down,
                # make sure it's not on the last row
                if direction == 'down' and clicked_candy.row_num < height / candy_height - 1:
                    # get the candy below
                    swapped_candy = board[clicked_candy.row_num + 1][clicked_candy.col_num]
                    
                    # move the two candies
                    clicked_candy.rect.top = clicked_candy.row_num * candy_height + distance_y
                    swapped_candy.rect.top = swapped_candy.row_num * candy_height - distance_y
                    
                    # snap them into their new positions on the board
                    if clicked_candy.rect.top >= swapped_candy.row_num * candy_height - candy_height / 4:
                        swap(clicked_candy, swapped_candy)
                        matches.update(match_three(clicked_candy))
                        matches.update(match_three(swapped_candy))
                        moves += 1
                        clicked_candy = None
                        swapped_candy = None
                        #테스트 부분입니다.
                        print("아래쪽으로 Swap 성공")
                        
                            
                        
            # detect mouse release
            if clicked_candy is not None and event.type == MOUSEBUTTONUP:
                
                # snap the candies back to their original positions on the grid
                clicked_candy.snap()
                clicked_candy = None
                if swapped_candy is not None:
                    swapped_candy.snap()
                    swapped_candy = None
            
    draw()
    pygame.display.update()

    matches = set()
    for row in board:
        for candy in row:
            matches.update(match_three(candy))

    # check if there's at least 3 matching candies
    if len(matches) >= 3:
        
        # add to score
        score += len(matches)
        
        # animate the matching candies shrinking
        while len(matches) > 0:
            
            clock.tick(100)
            
            # decrease width and height by 1
            for candy in matches:
                new_width = candy.image.get_width() - 1
                new_height = candy.image.get_height() - 1
                new_size = (new_width, new_height)
                candy.image = pygame.transform.smoothscale(candy.image, new_size)
                candy.rect.left = candy.col_num * candy_width + (candy_width - new_width) / 2
                candy.rect.top = candy.row_num * candy_height + (candy_height - new_height) / 2
                
            # check if the candies have shrunk to zero size
            for row_num in range(len(board)):
                for col_num in range(len(board[row_num])):
                    candy = board[row_num][col_num]
                    if candy.image.get_width() <= 0 or candy.image.get_height() <= 0:
                        matches.remove(candy)
                        
                        # generate a new candy
                        board[row_num][col_num] = Candy(row_num, col_num)
                        
            draw()
            pygame.display.update()
            for candy in matches :
                matches.update(match_three(candy))
            
            
pygame.quit()