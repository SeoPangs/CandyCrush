"""
4개의 보드를 부모로 사용 후 적합도를 검사해 2개의 보드를 부모삼아 새로운 보드를 생성, 총 4개의 자식을 생성
적합도는 뭉쳐서 그려진 캔디 그룹의 수가 낮을수록 (움직임이 유효한 캔디가 많을수록) 높음.
"""

import pygame
from pygame.locals import *
import random

#AutoMode가 활성화되면 마우스 입력이 활성화 되지 않는다.
bAutoMode = False

pygame.init()

# 게임 창 세팅
width = 400
height = 400
scoreboard_height = 25
window_size = (width, height + scoreboard_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Match Three for The Manual')
pygame.display.set_icon(pygame.image.load("swirl_blue.png"))

# 7종류의 캔디
candy_colors = ['blue', 'green', 'orange', 'pink', 'purple', 'red', 'teal', 'yellow']

# 그려질 캔디의 크기
candy_width = 40
candy_height = 40
candy_size = (candy_width, candy_height)

#실제 게임에서 쓰일 보드
board = []

class Candy:
    
    def __init__(self, row_num, col_num, color):
        
        # 캔디 위치 저장
        self.row_num = row_num
        self.col_num = col_num
        
        self.color = candy_colors[color] #보드에 적혀있는대로 캔디에 색깔 할당
        image_name = f'swirl_{self.color}.png'
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.smoothscale(self.image, candy_size)
        self.rect = self.image.get_rect()
        self.rect.left = col_num * candy_width
        self.rect.top = row_num * candy_height
        
    # 화면에 캔디 출력
    def draw(self):
        screen.blit(self.image, self.rect)
        
    # 캔디 위치 변경
    def snap(self):
        self.snap_row()
        self.snap_col()
        
    def snap_row(self):
        self.rect.top = self.row_num * candy_height
        
    def snap_col(self):
        self.rect.left = self.col_num * candy_width
        
def draw():
    
    # 배경 그리기
    pygame.draw.rect(screen, (173, 216, 230), (0, 0, width, height + scoreboard_height))
    
    # 사탕 그리기
    for row in board:
        for candy in row:
            candy.draw()
    
    # UI
    font = pygame.font.SysFont('monoface', 18)
    score_text = font.render(f'Score: {score}', 1, (0, 0, 0))
    score_text_rect = score_text.get_rect(center=(width / 4, height + scoreboard_height / 2))
    screen.blit(score_text, score_text_rect)
    
    moves_text = font.render(f'Moves: {moves}', 1, (0, 0, 0))
    moves_text_rect = moves_text.get_rect(center=(width * 3 / 4, height + scoreboard_height / 2))
    screen.blit(moves_text, moves_text_rect)
    
# 캔디끼리 위치 변경
def swap(candy1, candy2):
    
    temp_row = candy1.row_num
    temp_col = candy1.col_num
    
    candy1.row_num = candy2.row_num
    candy1.col_num = candy2.col_num
    
    candy2.row_num = temp_row
    candy2.col_num = temp_col
    
    # 보드에서 캔디 위치 업데이트
    board[candy1.row_num][candy1.col_num] = candy1
    board[candy2.row_num][candy2.col_num] = candy2
    
    # 실제로 위치 변경
    candy1.snap()
    candy2.snap()
    
# 3개 이상의 캔디로 뭉친 그룹 찾기
def find_matches(board, candy, matches, direction):

    matches.add(candy)
    
    # 위 체크
    if direction == "up" and candy.row_num > 0:
        neighbor = board[candy.row_num - 1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(board, neighbor, matches, direction))
            
    # 아래 체크
    if direction == "down" and candy.row_num < height / candy_height - 1:
        neighbor = board[candy.row_num + 1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(board, neighbor, matches, direction))
            
    # 왼쪽 체크
    if direction == "left"  and candy.col_num > 0:
        neighbor = board[candy.row_num][candy.col_num - 1]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(board, neighbor, matches, direction))
            
    # 오른쪽 체크
    if direction == "right" and candy.col_num < width / candy_width - 1:
        neighbor = board[candy.row_num][candy.col_num + 1]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(board, neighbor, matches, direction))
            
    return matches
    
# 캔디 그룹이 3개이상이면 그 그룹을, 아니면 빈 세트를 반환
def match_three(board, candy, direction):
    
    matches = find_matches(board, candy, set(), direction)
    if len(matches) >= 3:
        return matches
    else:
        return set()



boards = []
# boards: 보드 4개로 이루어진 삼중배열   
# board[x][n][m]: (n, m)번째 있는 x번째 Candy Board의 값.

#총 4개의 보드를 생성할 것임
for i in range(4):
    
    # 이차원 리스트를 저장할 리스트 삽입
    boards.append([])
    
    for row_num in range(height // candy_height):
        
        # 이차원 리스트 삽입
        boards[i].append([])
        
        for col_num in range(width // candy_width):
            
            # 랜덤하게 이차원 리스트 값채우기
            candy = Candy(row_num, col_num, random.randint(0, 7))
            boards[i][row_num].append(candy)


'''print("Parent1-------------Parent2-------------Parent3-------------Parent4-------------")
for i in range(10):
    for k in range(4):
        for j in range(10):
            print(boards[k][i][j].color[0], end = " ")
        print(" ", end = "")
    print("\n", end = "")'''

#유전자 알고리즘 보드 생성 함

#변이
def Mutation(board):
    for row in board:
        for candy in row:
            if(random.randint(1, 100) == 1):
                candy.color = candy_colors[random.randint(0, 7)]
                image_name = f'swirl_{candy.color}.png'
                candy.image = pygame.image.load(image_name)
                candy.image = pygame.transform.smoothscale(candy.image, candy_size)
                print("m", candy.row_num, candy.col_num)
    
    '''print("\nchild--------")

    for i in range(10):
        for j in range(10):
            print(board[i][j].color[0], end = " ")
        print("")'''
    return board

#교차
def crossover(parent):
    row = random.randint(0, 10)
    col = random.randint(0, 10)
    '''print("row: ", row, "col: ", col)'''
    child = [[] for i in range(10)]

    '''for i in range(10):
        for j in range(10):
            print(parent[0][i][j].color[0], end = " ")
        print("")
    print("")
    for i in range(10):
        for j in range(10):
            print(parent[1][i][j].color[0], end = " ")
        print("")'''
    
    for i in range(row):
        for j in range(col):
            child[i].append(parent[0][i][j])
        for j in range(10 - col):
            child[i].append(parent[1][i][j + col])
            
    for i in range(10 - row):
        for j in range(col):
            child[i + row].append(parent[1][i + row][j])
        for j in range(10 - col):
            child[i + row].append(parent[0][i + row][j + col])
        
    '''print("\nchild--------")

    for i in range(10):
        for j in range(10):
            print(child[i][j].color[0], end = " ")
        print("")'''
        
    return Mutation(child)
           
#룰렛 휠
def wheel(boards, fitness):
    sum = 0
    parent = []
    for i in fitness:
        sum += i
    '''print("sum: ", sum)'''
    for i in range(2):
        rand = random.randint(1, sum)
        '''print("rand: ", rand)'''
        for j in range(4):
            if(rand <= fitness[j]):
                '''print(j+1)'''
                parent.append(boards[j])
                break
            else:
                rand -= fitness[j]
    '''print("")'''
    return crossover(parent)
    

#보드의 적합도 검사
def selection(board):
    unfitness = 0
    for row in board:
        for candy in row:
            tmp = match_three(board, candy, "up")
            if(len(tmp) >= 3):
                unfitness += len(tmp)
            tmp = match_three(board, candy, "down")
            if(len(tmp) >= 3):
                unfitness += len(tmp)
            tmp = match_three(board, candy, "left")
            if(len(tmp) >= 3):
                unfitness += len(tmp)
            tmp = match_three(board, candy, "right")
            if(len(tmp) >= 3):
                unfitness += len(tmp)
    return unfitness

#유전자 알고리즘으로 보드 생성
while True:
    gene = 0
    '''print("\n\ngeneration: ", gene)'''
    selected_board = 4
    fit = []
    '''print("Fitness: ", end = "")'''
    
    for i in range(4):
        fit.append(100 - selection(boards[i]))

    print(fit)

    for i in range(4):
        if(fit[i] == 100):
            selected_board = i

    if(selected_board < 4):
        board = boards[selected_board]
        break

    for board in boards:
        board = wheel(boards, fit)
    gene += 1

# 플레이어가 움직일 캔디
clicked_candy = None

# 플레이어가 바꿀 위치에 있는 캔디
swapped_candy = None

# 클릭 좌표
click_x = None
click_y = None

# 점수랑 움직임 수
score = 0
moves = 0

# 게임 루프 값 지정
clock = pygame.time.Clock()
running = True


#게임 루프가 여기서 이뤄집니다.
while running:
    
    # 캔디 그룹
    matches = set()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if not bAutoMode:    
            
            # 클릭 캔디 없음 and 마우스 클릭
            if clicked_candy is None and event.type == MOUSEBUTTONDOWN:
                
                # 클릭한 캔디 찾기
                for row in board:
                    for candy in row:
                        if candy.rect.collidepoint(event.pos):
                            
                            clicked_candy = candy
                            
                            # 클릭한 캔디 위치 저
                            click_x = event.pos[0]
                            click_y = event.pos[1]
                            
            # 캔디 클릭함 and 마우스 드래그
            if clicked_candy is not None and event.type == MOUSEMOTION:
                
                # 드래그 방향 계산
                distance_x = abs(click_x - event.pos[0])
                distance_y = abs(click_y - event.pos[1])
                
                # 바꿀 캔디 업데이트
                if swapped_candy is not None:
                    swapped_candy.snap()
                    
                # 방향 판단
                if distance_x > distance_y and click_x > event.pos[0]:
                    direction = 'left'
                elif distance_x > distance_y and click_x < event.pos[0]:
                    direction = 'right'
                elif distance_y > distance_x and click_y > event.pos[1]:
                    direction = 'up'
                else:
                    direction = 'down'
                    
                # 좌우냐 상하냐 판단해 캔디 이동
                if direction in ['left', 'right']:
                    clicked_candy.snap_row()
                else:
                    clicked_candy.snap_col()
                    
                #왼쪽으로 이동
                if direction == 'left' and clicked_candy.col_num > 0:
                    
                    swapped_candy = board[clicked_candy.row_num][clicked_candy.col_num - 1]
                    
                    clicked_candy.rect.left = clicked_candy.col_num * candy_width - distance_x
                    swapped_candy.rect.left = swapped_candy.col_num * candy_width + distance_x
                    
                    if clicked_candy.rect.left <= swapped_candy.col_num * candy_width + candy_width / 4:
                        swap(clicked_candy, swapped_candy)
                        matches.update(match_three(board, clicked_candy, direction))
                        matches.update(match_three(board, swapped_candy, direction))
                        moves += 1
                        clicked_candy = None
                        swapped_candy = None
                        
                #오른쪽으로 이동
                if direction == 'right' and clicked_candy.col_num < width / candy_width - 1:
                    
                    swapped_candy = board[clicked_candy.row_num][clicked_candy.col_num + 1]
                    
                    clicked_candy.rect.left = clicked_candy.col_num * candy_width + distance_x
                    swapped_candy.rect.left = swapped_candy.col_num * candy_width - distance_x
                    
                    if clicked_candy.rect.left >= swapped_candy.col_num * candy_width - candy_width / 4:
                        swap(clicked_candy, swapped_candy)
                        matches.update(match_three(board, clicked_candy, direction))
                        matches.update(match_three(board, swapped_candy, direction))
                        moves += 1
                        clicked_candy = None
                        swapped_candy = None
                        
                # 위로 이동
                if direction == 'up' and clicked_candy.row_num > 0:
                    
                    swapped_candy = board[clicked_candy.row_num - 1][clicked_candy.col_num]
                    
                    clicked_candy.rect.top = clicked_candy.row_num * candy_height - distance_y
                    swapped_candy.rect.top = swapped_candy.row_num * candy_height + distance_y
                    
                    if clicked_candy.rect.top <= swapped_candy.row_num * candy_height + candy_height / 4:
                        swap(clicked_candy, swapped_candy)
                        matches.update(match_three(board, clicked_candy, direction))
                        matches.update(match_three(board, swapped_candy, direction))
                        moves += 1
                        clicked_candy = None
                        swapped_candy = None
                        
                #아래로 이동
                if direction == 'down' and clicked_candy.row_num < height / candy_height - 1:
                    
                    swapped_candy = board[clicked_candy.row_num + 1][clicked_candy.col_num]
                    
                    clicked_candy.rect.top = clicked_candy.row_num * candy_height + distance_y
                    swapped_candy.rect.top = swapped_candy.row_num * candy_height - distance_y
                    
                    if clicked_candy.rect.top >= swapped_candy.row_num * candy_height - candy_height / 4:
                        swap(clicked_candy, swapped_candy)
                        matches.update(match_three(board, clicked_candy, direction))
                        matches.update(match_three(board, swapped_candy, direction))
                        moves += 1
                        clicked_candy = None
                        swapped_candy = None
                        
                        
                    
        # 마우스 뗌
        if clicked_candy is not None and event.type == MOUSEBUTTONUP:
            
            #캔디들 원래 위치로 이동
            clicked_candy.snap()
            clicked_candy = None
            if swapped_candy is not None:
                swapped_candy.snap()
                swapped_candy = None
            
    draw()
    pygame.display.update()

    #초기 맵 생성 후 그룹 확인(유전자 알고리즘으로 보드만든 뒤엔 삭제 예정)
    matches = set()
    for row in board:
        for candy in row:
            matches.update(match_three(board, candy, "up"))
            matches.update(match_three(board, candy, "down"))
            matches.update(match_three(board, candy, "left"))
            matches.update(match_three(board, candy, "right"))

    # 캔디 그룹이 3개인지 판단
    if len(matches) >= 3:
        
        # 점수 추가
        score += len(matches)
        
        # 캔디 삭제
        while len(matches) > 0:
            
            clock.tick(100)
            
            # 사이즈 감소
            for candy in matches:
                new_width = candy.image.get_width() - 1
                new_height = candy.image.get_height() - 1
                new_size = (new_width, new_height)
                candy.image = pygame.transform.smoothscale(candy.image, new_size)
                candy.rect.left = candy.col_num * candy_width + (candy_width - new_width) / 2
                candy.rect.top = candy.row_num * candy_height + (candy_height - new_height) / 2
                
            # 캔디 삭제
            for row_num in range(len(board)):
                for col_num in range(len(board[row_num])):
                    candy = board[row_num][col_num]
                    if candy.image.get_width() <= 0 or candy.image.get_height() <= 0:
                        matches.remove(candy)
                        
                        #새 캔디 생성
                        board[row_num][col_num] = Candy(row_num, col_num, random.randint(0, 7))
                        
            #보드 업데이트
            draw()
            pygame.display.update()

            #새로 생성된 캔디가 그룹을 이루는지 확인
            for candy in matches :
                matches.update(match_three(board, candy, "up"))
                matches.update(match_three(board, candy, "down"))
                matches.update(match_three(board, candy, "left"))
                matches.update(match_three(board, candy, "right"))
            
            
pygame.quit()
