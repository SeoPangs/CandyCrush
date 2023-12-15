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


candy_colors = ['blue', 'green', 'orange', 'pink', 'purple', 'red', 'teal', 'yellow']