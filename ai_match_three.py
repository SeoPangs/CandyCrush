import pygame
from pygame.locals import *
import random
import numpy as np

#AutoMode가 활성화되면 마우스 입력이 활성화 되지 않는다.
bAutoMode = True

bGeneticLevelGenerate = False

pygame.init()

# create the game window
width = 400
height = 400
scoreboard_height = 25
window_size = (width, height + scoreboard_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Match Three with Artificial Intelligence')
pygame.display.set_icon(pygame.image.load("swirl_blue.png"))

# game variables
score = 0
moves = 0

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
        
        self.match = set()
        # assign a random image
        self.color = random.choice(candy_colors)
        image_name = f'swirl_{self.color}.png'
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.smoothscale(self.image, candy_size)
        self.rect = self.image.get_rect()
        self.rect.left = col_num * candy_width
        self.rect.top = row_num * candy_height
        
    def check(self):
        self.image = pygame.image.load(f'swirl_{self.color}.png')
        self.image = pygame.transform.smoothscale(self.image, candy_size)
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

if not bGeneticLevelGenerate:
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
def find_matches(candy, matches, board):
    
    # add the candy to the set
    matches.add(candy)
    
    # check the candy above if it's the same color
    if candy.row_num > 0:
        neighbor = board[candy.row_num - 1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches, board))
            
    # check the candy below if it's the same color
    if candy.row_num < height / candy_height - 1:
        neighbor = board[candy.row_num + 1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches, board))
            
    # check the candy to the left if it's the same color
    if candy.col_num > 0:
        neighbor = board[candy.row_num][candy.col_num - 1]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches, board))
            
    # check the candy to the right if it's the same color
    if candy.col_num < width / candy_width - 1:
        neighbor = board[candy.row_num][candy.col_num + 1]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches, board))
            
    return matches
    
def match_board(board):
    match_value_list = []
    for row_num in range(len(board)):
        for col_num in range(len(board[row_num])):
            candy = board[row_num][col_num]
            matches = find_matches(candy, set(), board)
            candy.match = len(matches)

    # 각 행에 대해 반복
    for row in board:
        # 각 캔디 주변의 수으 추출해서 저장,
        result_row = [len(find_matches(candy, set(), board)) for candy in row]
        match_value_list.append(result_row)

    return match_value_list

# return a set of at least 3 matching candies or an empty set
def match_three(candy):
    
    matches = find_matches(candy, set(), board)
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

def get_neighbors(candy, board):
    neighbors = []
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
    
    return neighbors

def print_candy(candy):
    print("Candy %d %d %s" %(candy.row_num, candy.col_num, candy.color))

# 추가된 함수: 인공지능이 랜덤으로 주변 캔디를 스왑하는 함수
def swap_by_ai():
    global moves
    temp_board = board.copy()
    candy = random.choice([candy for row in board for candy in row])

    print_candy(candy)
    match_board(board)

    # 주변의 캔디를 무작위로 선택
    neighbor_candies = get_neighbors(candy, board)
    for iCandy in neighbor_candies:
        if iCandy:
        # 스왑 수행
            #iCandy, candy = candy, iCandy
            matches = find_matches(iCandy, set(), board)

            for i in matches:
                print_candy(i)
#여기만 좀 수정하자.
            swap(candy, iCandy)
            matches.update(match_three(candy))
            matches.update(match_three(iCandy))
            moves += 1  

    

SIZE = 10
class Chromosome():
    def __init__(self, g=[]) -> None:
        self.genes = g.copy()
        self.fitness = 0
        if self.genes.__len__()==0:
            for row_num in range(SIZE):
                # add a new row to the board
                self.genes.append([])
                for col_num in range(SIZE):
                    # create the candy and add it to the board
                    candy = Candy(row_num, col_num)
                    self.genes[row_num].append(candy)

    def evaluate(self):
        value = 0
        list = match_board(self.genes)
        for i in list:
            #print(i)
            for j in i:
                if j >= 3:
                    value += 1
        return value

def select(pop):
    max_value  = sum([c.evaluate() for c in population])
    pick    = random.uniform(0, max_value)
    current = 0
    
    # 룰렛휠에서 어떤 조각에 속하는지를 알아내는 루프
    for c in pop:
        current += c.evaluate()
        if current > pick:
            return c

MUTATION_RATE = 0.1
def mutate(chromosome):
    for row_num in range(SIZE):
        for col_num in range(SIZE):
            if random.random() < MUTATION_RATE:
                # 일정 확률로 돌연변이 발생
                chromosome.genes[row_num][col_num].color = random.choice(candy_colors)

def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index1 = random.randint(0, SIZE - 2)
    index2 = random.randint(index1 + 1, SIZE - 1)

    # 부분적 Crossover
    child1 = father.genes[:index1] + mother.genes[index1:index2] + father.genes[index2:]
    child2 = mother.genes[:index1] + father.genes[index1:index2] + mother.genes[index2:]

    return (child1, child2)

def print_population(pop):
    i = 0
    for x in pop:
        print("염색체 #", i, "적합도=", x.evaluate())
        i += 1
    print("")


### 여기부터 유전자 알고리즘
POPULATION_SIZE = 100
population = []

if bGeneticLevelGenerate:
    for i in range(POPULATION_SIZE):
        population.append(Chromosome())

    population.sort(key=lambda x: x.evaluate())

    count=0
    print("세대 번호=", count)
    print_population(population)

    while population[0].evaluate() > 0:
        print("New Generations")
        new_pop = []

        crossover_index = 0
        # 선택과 교차 연산
        for _ in range(POPULATION_SIZE//2):
            crossover_index += 1
            print(crossover_index)
            c1, c2 = crossover(population);
            new_pop.append(Chromosome(c1));
            new_pop.append(Chromosome(c2));

        # 자식 세대가 부모 세대를 대체한다. 
        # 깊은 복사를 수행한다. 
        population = new_pop.copy();    
        
        # 돌연변이 연산
        for c in population: 
            mutate(c)

        # 출력을 위한 정렬
        population.sort(key=lambda x: x.evaluate())
        print("세대 번호=", count)
        print_population(population)
        count += 1
        if count > 100 : 
            break;

    print("최종값")
    for i in population[0].genes:
        print("[", end="")
        for j in i:
            print(j.color, end=", ")
        print("]")

    board = population[0].genes

### 여기까지 유전자 알고리즘

def print_board():
    for i in board:
        print("[", end="")
        for j in i:
            print(j.color, end=", ")
            j.check()
        print("]")

print_board()

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
            if bAutoMode:
                swap_by_ai()

        if not bAutoMode:
            # detect mouse click
            if clicked_candy is None and event.type == MOUSEBUTTONDOWN:
                
                # get the candy that was clicked on
                for row in board:
                    for candy in row:
                        if candy.rect.collidepoint(event.pos):
                            
                            clicked_candy = candy
                            print("Mathces %d %d %s" %(candy.row_num, candy.col_num, candy.color))
                            
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
                        print_board()
                        
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