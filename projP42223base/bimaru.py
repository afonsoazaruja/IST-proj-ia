# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 127:
# 103606 Henrique Silva
# 103624 Afonso Azaruja

import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

BOARD_SIZE = 10

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, grid, row, col):
        self.board = grid
        self.row = row
        self.col = col
        self.free_row = [BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.free_col = [BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.boats = [1, 2, 3, 4]
        self.unknown_coord = []
        self.coord = []

    def set_value(self, row: int, col: int, val):
        """Insere peça no board e atualiza os espaços livres e o número de peças
        que cabem em cada linha e coluna."""
        if 0 <= row <= 9 and 0 <= col <= 9:
            if self.get_value(row, col) == None:

                self.free_row[row] -= 1
                self.free_col[col] -= 1
                
                if val.lower() != 'w':
                    self.row[row] -= 1
                    self.col[col] -= 1
                    self.coord.append((row, col))
                    self.coord.sort(key=lambda c: (c[0], c[1]))
                
                    if val == 'u':
                        self.unknown_coord.append((row, col))
                
                self.board[row][col] = val
            
            elif self.get_value(row, col).islower():
                self.board[row][col] = val
        
        return self

    def calculate_state(self, hints):
        """Calcula o estado inicial do board."""
        for hint in hints:
            r = int(hint[0])
            c = int(hint[1])
            v = hint[2]

            self.set_value(r, c, v)

        for hint in hints:
            r = int(hint[0])
            c = int(hint[1])
            v = hint[2]
 
            if v.lower() == 'c':
               self.circle_case(r, c)
               self.boats[3] -= 1
            if v.lower() == 't':
                self.top_case(r, c)
            if v.lower() == 'r':
                self.right_case(r, c)
            if v.lower() == 'b':
                self.bottom_case(r, c)
            if v.lower() == 'l':
                self.left_case(r, c)
            if v.lower() == 'm':
                self.middle_case(r, c)
            
        while(True):
            state = self.free_row[:]            
            self.fill_water()
            self.fill_missing()
            if state == self.free_row:
                break

        return self

    def fill_missing(self):
        """No caso em que os espaços livres numa linha (coluna) é igual ao
        número de peças de barcos que faltam nessa linha (coluna), essa linha
        (coluna) é preenchida com peças de barcos."""
        for i in range(BOARD_SIZE):
            if self.row[i] != 0 and self.free_row[i] == self.row[i]:
                for col in range(BOARD_SIZE):
                    if self.get_value(i, col) == None:
                        self.set_value(i, col, 'u')
            if self.col[i] != 0 and self.free_col[i] == self.col[i]:
                for row in range(BOARD_SIZE):
                    if self.get_value(row, i) == None:
                        self.set_value(row, i, 'u')

        return self

    def circle_case(self, r: int, c: int):
        
        self.set_value(r-1, c-1, 'w')
        self.set_value(r-1, c, 'w')
        self.set_value(r-1, c+1, 'w')
        self.set_value(r, c+1, 'w')
        self.set_value(r+1, c+1, 'w')
        self.set_value(r+1, c, 'w')
        self.set_value(r+1, c-1, 'w')
        self.set_value(r, c-1, 'w')

        return self

    def top_case(self, r: int, c: int):
        
        self.set_value(r-1, c-1, 'w')
        self.set_value(r-1, c, 'w')
        self.set_value(r-1, c+1, 'w')
        self.set_value(r, c+1, 'w')
        self.set_value(r+1, c+1, 'w')
        self.set_value(r+1, c-1, 'w')
        self.set_value(r, c-1, 'w')
        self.set_value(r+2, c-1, 'w')
        self.set_value(r+2, c+1, 'w')
        self.set_value(r+1, c, 'u')

        return self

    def right_case(self, r: int, c: int):
        
        self.set_value(r-1, c-1, 'w')
        self.set_value(r-1, c, 'w')
        self.set_value(r-1, c+1, 'w')
        self.set_value(r, c+1, 'w')
        self.set_value(r+1, c+1, 'w')
        self.set_value(r+1, c, 'w')
        self.set_value(r+1, c-1, 'w')
        self.set_value(r+1, c-2, 'w')
        self.set_value(r-1, c-2, 'w')
        self.set_value(r, c-1, 'u')

        return self
    
    def bottom_case(self, r: int, c: int):

        self.set_value(r-2, c-1, 'w')
        self.set_value(r-2, c+1, 'w')
        self.set_value(r-1, c+1, 'w')
        self.set_value(r, c+1, 'w')
        self.set_value(r+1, c+1, 'w')
        self.set_value(r+1, c, 'w')
        self.set_value(r+1, c-1, 'w')
        self.set_value(r, c-1, 'w')
        self.set_value(r-1, c-1, 'w')
        self.set_value(r-1, c, 'u')

        return self
    
    def left_case(self, r: int, c: int):
        
        self.set_value(r-1, c-1, 'w')
        self.set_value(r-1, c, 'w')
        self.set_value(r-1, c+1, 'w')
        self.set_value(r, c-1, 'w')
        self.set_value(r+1, c+1, 'w')
        self.set_value(r+1, c, 'w')
        self.set_value(r+1, c-1, 'w')
        self.set_value(r+1, c+2, 'w')
        self.set_value(r-1, c+2, 'w')
        self.set_value(r, c+1, 'u')

        return self

    def middle_case(self, r: int, c: int):

        self.set_value(r - 1, c - 1, 'w')
        self.set_value(r - 1, c + 1, 'w')
        self.set_value(r + 1, c + 1, 'w')
        self.set_value(r + 1, c - 1, 'w')

        return self

    def process_unknown(self):
        pass
        #for coord in self.unknown_coord:


    def print_board(self):
        """Faz print do board no terminal."""
        print("(ROW) Peças:", self.row, " Livres:", self.free_row, '\n')
        print("(COL) Peças:", self.col, " Livres:", self.free_col, '\n')
        print("(COR)", len(self.coord), self.coord, '\n')
        print("(UKN)", len(self.unknown_coord), self.unknown_coord, '\n')
        for i in range(10):
            for j in range(10):
                if(self.get_value(i, j) == None):
                    sys.stdout.write('?')
                else:
                    if self.get_value(i,j) == 'w':
                        sys.stdout.write('.')
                    else:
                        sys.stdout.write(self.board[i][j])
            sys.stdout.write('\n')

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row <= 9 and 0 <= col <= 9:
            return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row-1, col), self.get_value(row+1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col-1), self.get_value(row, col+1))
    
    def adjacent_diagonal_values(self, row: int, col: int) -> (str, str, str, str):
        """Devolve os valores que se encontram nas diagonais, começando pelo,
        canto superior esquerdo, seguindo os ponteiros do relógio."""
        return (
            self.get_value(row-1, col-1), 
            self.get_value(row-1, col+1),
            self.get_value(row+1, col+1),
            self.get_value(row+1, col-1))
    
    def adjacent_values(self, row: int, col: int) -> (str, str, str, str, str, str, str, str):
        """Devolve os valores à volta da coordenada"""
        return (
            self.get_value(row-1, col-1),
            self.get_value(row-1, col), 
            self.get_value(row-1, col+1),
            self.get_value(row, col+1),
            self.get_value(row+1, col+1),
            self.get_value(row+1, col),
            self.get_value(row+1, col-1),
            self.get_value(row, col-1) 
        )
    
    def fill_water(self):
        i = 0
        for j in self.row:
            if j == 0:
                self.fill_row(i)
            i += 1

        i = 0
        for j in self.col:
            if j == 0:
                self.fill_col(i)
            i += 1

        return self

    def fill_row(self, row: int):
        """Preenche as linhas que já estão completas com água"""
        for i in range(BOARD_SIZE):
            if self.get_value(row, i) == None:
                self.set_value(row, i, 'w')
        return self

    def fill_col(self, col: int):
        """Preenche as colunas que já estão completas com água"""
        for i in range(BOARD_SIZE):
            if self.get_value(i, col) == None:
                self.set_value(i, col, 'w')
        return self

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
                
        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        row = list(map(int, sys.stdin.readline().split()[1:]))
        col = list(map(int, sys.stdin.readline().split()[1:]))
        num = int(sys.stdin.readline())
        hints = []
        grid = np.full((BOARD_SIZE, BOARD_SIZE), None, dtype=object)
        for _ in range(num):
            hints.append(tuple(sys.stdin.readline().split()[1:]))
        return Board(grid, row, col).calculate_state(hints)

    # TODO: outros metodos da classe

class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = BimaruState(board)
        super().__init__(state)
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        # TODO
        partir do estado passado como argumento."""
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    bimaru = Bimaru(board)
    Board.print_board(board)
