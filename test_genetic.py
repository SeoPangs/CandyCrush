import random

def find_matches(candy, matches, board):
    
    # add the candy to the set
    matches.add(candy)
    
    # check the candy above if it's the same color
    if candy.row_num > 0:
        neighbor = board[candy.row_num - 1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches, board))
            
    # check the candy below if it's the same color
    if candy.row_num < 10 - 1:
        neighbor = board[candy.row_num + 1][candy.col_num]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches, board))
            
    # check the candy to the left if it's the same color
    if candy.col_num > 0:
        neighbor = board[candy.row_num][candy.col_num - 1]
        if candy.color == neighbor.color and neighbor not in matches:
            matches.update(find_matches(neighbor, matches, board))
            
    # check the candy to the right if it's the same color
    if candy.col_num < 10 - 1:
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
def mutate(pop):
    pass
def crossover(pop):
    father = select(pop)
    mother = select(pop)
    index = random.randint(1, SIZE - 1)
    child1 = father.genes[:index] + mother.genes[index:] 
    child2 = mother.genes[:index] + father.genes[index:] 
    return (child1, child2)

def print_population(pop):
    i = 0
    for x in pop:
        print("염색체 #", i, "적합도=", x.evaluate())
        i += 1
    print("")


candy_colors = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

class Candy:
    
    def __init__(self, row_num, col_num):
        
        # set the candy's position on the board
        self.row_num = row_num
        self.col_num = col_num
        
        # assign a random image
        self.color = random.choice(candy_colors)

ccc = Chromosome()

for i in ccc.genes:
    print("[", end="")
    for j in i:
        print(j.color, end=", ")
    print("]")

print()

for i in match_board(ccc.genes):
    print("[", end="")
    for j in i:
        print(j, end=", ")
    print("]")


print(ccc.evaluate())

POPULATION_SIZE = 1000
population = []

for i in range(POPULATION_SIZE):
    population.append(Chromosome())

population.sort(key=lambda x: x.evaluate())

count=0
print("세대 번호=", count)
print_population(population)

while population[0].evaluate() > 0:
    new_pop = []

    # 선택과 교차 연산
    for _ in range(POPULATION_SIZE//2):
        c1, c2 = crossover(population);
        new_pop.append(Chromosome(c1));
        new_pop.append(Chromosome(c2));

    # 자식 세대가 부모 세대를 대체한다. 
    # 깊은 복사를 수행한다. 
    population = new_pop.copy();    
    
    # 돌연변이 연산
    for c in population: mutate(c)

    # 출력을 위한 정렬
    population.sort(key=lambda x: x.evaluate())
    print("세대 번호=", count)
    print_population(population)
    count += 1
    if count > 100 : break;

print("최종값")
for i in population[0].genes:
    print("[", end="")
    for j in i:
        print(j.color, end=", ")
    print("]")


