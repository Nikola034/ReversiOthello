#Autor: Nikola Bandulaja SV74/2022
#Projekat je radjen u periodu od 13.05.2023. do 24.05.2023.
import copy
import random
import time
from tkinter import messagebox
import pygame

pygame.init()

class Field(object):

    def __init__(self, value, valid):
        self._value = value
        self._valid = valid

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value

    def isValid(self):
            return self._valid == True

    def setValid(self, valid):
        self._valid = valid



def crtajTablu():
    for row in range(8):
        for column in range(8):
            rect = pygame.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

def osveziDiskove(board):
    for row in range(8):
        for column in range(8):
            if board[row][column].getValue() == 1:
                pygame.draw.circle(screen, WHITE,
                                   (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 5)
            elif board[row][column].getValue() == -1:
                pygame.draw.circle(screen, BLACK,
                                   (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 5)
            elif board[row][column].getValue() == 0 and board[row][column].isValid():
                pygame.draw.circle(screen, BLACK,
                                   (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 5, width=3)
            elif board[row][column].getValue() == 0 and not board[row][column].isValid():
                pygame.draw.circle(screen, GREEN,
                                   (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 5, width=3)


    pygame.display.flip()

def nadjiValidnePozicije(board, igrac):

    dobra = losa = 0
    if igrac == 1:
        dobra = -1
        losa = 1
    else:
        dobra = 1
        losa = -1

    #za svako polje ide u svim pravcima, ako negde naidje na trazenu boju, validno je
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j].getValue() == 0:
                # gore
                x = i - 1
                while x >= 0:
                    if board[x][j].getValue() == 0:
                        break
                    elif board[x][j].getValue() == losa:
                        x -= 1
                    elif board[x][j].getValue() == dobra:
                        if x < i - 1:
                            board[i][j] = Field(0, True)
                        break
                # dole
                x = i + 1
                while x <= 7:
                    if board[x][j].getValue() == 0:
                        break
                    elif board[x][j].getValue() == losa:
                        x += 1
                    elif board[x][j].getValue() == dobra:
                        if x > i + 1:
                            board[i][j] = Field(0, True)
                        break
                # levo
                x = j - 1
                while x >= 0:
                    if board[i][x].getValue() == 0:
                        break
                    elif board[i][x].getValue() == losa:
                        x -= 1
                    elif board[i][x].getValue() == dobra:
                        if x < j - 1:
                            board[i][j] = Field(0, True)
                        break
                # desno
                x = j + 1
                while x <= 7:
                    if board[i][x].getValue() == 0:
                        break
                    elif board[i][x].getValue() == losa:
                        x += 1
                    elif board[i][x].getValue() == dobra:
                        if x > j + 1:
                            board[i][j] = Field(0, True)
                        break
                # dijagonala levo gore
                x = i - 1
                y = j - 1
                while x >= 0 and y >= 0:
                    if board[x][y].getValue() == 0:
                        break
                    elif board[x][y].getValue() == losa:
                        x -= 1
                        y -= 1
                    elif board[x][y].getValue() == dobra:
                        if x < i - 1 and y < j - 1:
                            board[i][j] = Field(0, True)
                        break
                # dijagonala levo dole
                x = i + 1
                y = j - 1
                while x <= 7 and y >= 0:
                    if board[x][y].getValue() == 0:
                        break
                    elif board[x][y].getValue() == losa:
                        x += 1
                        y -= 1
                    elif board[x][y].getValue() == dobra:
                        if x > i + 1 and y < j - 1:
                            board[i][j] = Field(0, True)
                        break
                # dijagonala desno gore
                x = i - 1
                y = j + 1
                while x >= 0 and y <= 7:
                    if board[x][y].getValue() == 0:
                        break
                    elif board[x][y].getValue() == losa:
                        x -= 1
                        y += 1
                    elif board[x][y].getValue() == dobra:
                        if x < i - 1 and y > j + 1:
                            board[i][j] = Field(0, True)
                        break
                # dijagonala desno dole
                x = i + 1
                y = j + 1
                while x <= 7 and y <= 7:
                    if board[x][y].getValue() == 0:
                        break
                    elif board[x][y].getValue() == losa:
                        x += 1
                        y += 1
                    elif board[x][y].getValue() == dobra:
                        if x > i + 1 and y > j + 1:
                            board[i][j] = Field(0, True)
                        break

    return board

def ponistiValidnostPozicija(board):
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            board[i][j] = Field(board[i][j].getValue(), False)

    return board

def odigrajPotez(position, row, column, igrac):

    dobra = losa = 0
    if igrac == 1:
        dobra = -1
        losa = 1
    else:
        dobra = 1
        losa = -1

    if position[row][column].isValid():
        position[row][column] = Field(dobra, True)

    # gore
    if row > 0:
        x = row - 1
        while position[x][column].getValue() == losa and x > 0:
            x -= 1
        if position[x][column].getValue() == dobra and x > -1:
            y = row - 1
            while y > x:
                position[y][column] = Field(dobra, True)
                y -= 1
    # dole
    if row < 7:
        x = row + 1
        while position[x][column].getValue() == losa and x < 7:
            x += 1
        if position[x][column].getValue() == dobra and x < 8:
            y = row + 1
            while y < x:
                position[y][column] = Field(dobra, True)
                y += 1
    # levo
    if column > 0:
        x = column - 1
        while position[row][x].getValue() == losa and x > 0:
            x -= 1
        if position[row][x].getValue() == dobra and x > -1:
            y = column - 1
            while y > x:
                position[row][y] = Field(dobra, True)
                y -= 1
    # desno
    if column < 7:
        x = column + 1
        while position[row][x].getValue() == losa and x < 7:
            x += 1
        if position[row][x].getValue() == dobra and x < 8:
            y = column + 1
            while y < x:
                position[row][y] = Field(dobra, True)
                y += 1
    # dijagonala levo gore
    if row > 0 and column > 0:
        x = row - 1
        y = column - 1
        while position[x][y].getValue() == losa and x > 0 and y > 0:
            x -= 1
            y -= 1
        if position[x][y].getValue() == dobra and x > -1 and y > -1:
            z = row - 1
            u = column - 1
            while z > x and u > y:
                position[z][u] = Field(dobra, True)
                z -= 1
                u -= 1
    # dijagonala levo dole
    if row < 7 and column > 0:
        x = row + 1
        y = column - 1
        while position[x][y].getValue() == losa and x < 7 and y > 0:
            x += 1
            y -= 1
        if position[x][y].getValue() == dobra and x < 8 and y > -1:
            z = row + 1
            u = column - 1
            while z < x and u > y:
                position[z][u] = Field(dobra, True)
                z += 1
                u -= 1
    # dijagonala desno gore
    if row > 0 and column < 7:
        x = row - 1
        y = column + 1
        while position[x][y].getValue() == losa and x > 0 and y < 7:
            x -= 1
            y += 1
        if position[x][y].getValue() == dobra and x > -1  and y < 8:
            z = row - 1
            u = column + 1
            while z > x and u < y:
                position[z][u] = Field(dobra, True)
                z -= 1
                u += 1
    # dijagonala desno dole
    if row < 7 and column < 7:
        x = row + 1
        y = column + 1
        while position[x][y].getValue() == losa and x < 7 and y < 7:
            x += 1
            y += 1
        if position[x][y].getValue() == dobra and x < 8  and y < 8:
            z = row + 1
            u = column + 1
            while z < x and u < y:
                position[z][u] = Field(dobra, True)
                z += 1
                u += 1
    return position

def listaValidnihPozicija(board):
    validnePozicije = []
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j].getValue() == 0 and board[i][j].isValid():
                validnePozicije.append((i, j))

    return validnePozicije

def izracunajPoene(board):
    poeni1 = poeni2 = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j].getValue() == -1:
                poeni1 += 1
            elif board[i][j].getValue() == 1:
                poeni2 += 1
    return (poeni1, poeni2)

#Semafor
def osveziSemafor(board):
    global poeni1
    global poeni2
    poeni = izracunajPoene(board)
    poeni1 = poeni[0]
    poeni2 = poeni[1]
    poeni1_str = "IGRAC1        " + str(poeni1)
    poeni2_str = str(poeni2) + "        IGRAC2"
    result_text1 = font.render(poeni1_str, True, BLACK, GRAY)
    result_rect1 = result_text1.get_rect(center=(screen.get_width() // 2 - 100, 890))
    result_text2 = font.render(poeni2_str, True, WHITE, GRAY)
    result_rect2 = result_text2.get_rect(center=(screen.get_width() // 2 + 100, 890))
    pygame.draw.rect(screen, GRAY, pygame.Rect(0, 840, screen.get_width(), 100))
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, 840, screen.get_width(), 100), 3)
    screen.blit(result_text1, result_rect1)
    screen.blit(result_text2, result_rect2)
    osveziDiskove(board)

def brojValidnihPoteza(board):
    retValue = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j].isValid() and board[i][j].getValue() == 0:
                retValue += 1
    return retValue

broj = 0
global_timer = 0

def minimax(position, depth, alpha, beta, maximizingPlayer, player, currentPosition):
    global broj, global_timer
    brPoteza = brojValidnihPoteza(position)
    if depth == 0 or brPoteza == 0 or time.time() - global_timer > 3:
        return heuristika(position, player), currentPosition
    if maximizingPlayer:
        broj += 1
        maxPos = currentPosition
        maxEval = float('-inf')
        validnePozicije = listaValidnihPozicija(position)
        for pos in validnePozicije:
            position2 = copy.deepcopy(position)
            position2 = odigrajPotez(position2, pos[0], pos[1], player)
            position2 = ponistiValidnostPozicija(position2)
            position2 = nadjiValidnePozicije(position2, -player)
            eval = minimax(position2, depth - 1, alpha, beta, False, -player, (pos[0], pos[1]))
            if eval[0] > maxEval:
                maxEval = eval[0]
                maxPos = pos
            alpha = max(alpha, eval[0])
            if beta <= alpha:
                break
        return maxEval, maxPos
    else:
        broj += 1
        maxPos = currentPosition
        minEval = float('inf')
        validnePozicije = listaValidnihPozicija(position)
        for pos in validnePozicije:
            position2 = copy.deepcopy(position)
            position2 = odigrajPotez(position2, pos[0], pos[1], player)
            position2 = ponistiValidnostPozicija(position2)
            position2 = nadjiValidnePozicije(position2, -player)
            eval = minimax(position2, depth - 1, alpha, beta, True, -player, (pos[0], pos[1]))
            if eval[0] < minEval:
                minEval = eval[0]
                maxPos = pos
            beta = min(beta, eval[0])
            if beta <= alpha:
                break
        return minEval, maxPos

def heuristika(position, player):
    global nadjene_heuristike

    if zobristHash(position) in nadjene_heuristike.keys():
        return nadjene_heuristike[zobristHash(position)]

    opponent = 1 if player == -1 else -1
    coin_parity = 100 * (paritet(position, player) - paritet(position, opponent)) / (paritet(position, player) + paritet(position, opponent))
    mobility = 0
    max_mobility = mobilnost(position, player)
    position = ponistiValidnostPozicija(position)
    boardCopy = nadjiValidnePozicije(position, opponent)
    min_mobility = mobilnost(boardCopy, opponent)
    if (max_mobility + min_mobility) != 0:
        mobility = 100 * (max_mobility - min_mobility) / (max_mobility + min_mobility)

    max_corner = coskovi(position, player)
    min_corner = coskovi(position, opponent)
    corner_occupancy = 0
    if (max_corner + min_corner) != 0:
        corner_occupancy = 100 * (max_corner - min_corner) / (max_corner + min_corner)

    edge_occupancy = 0
    max_edge = ivice(position, player)
    min_edge = ivice(position, opponent)

    if (max_edge + min_edge) != 0:
        edge_occupancy = 100 * (max_edge - min_edge) / (max_edge + min_edge)

    stability = 0
    max_stability_liste = stabilnostListe(position, player)
    min_stability_liste = stabilnostListe(position, opponent)

    max_stability = max_stability_liste[0] - max_stability_liste[2]
    min_stability = min_stability_liste[0] - min_stability_liste[2]

    if (max_stability + min_stability) != 0:
        stability = 100 * (max_stability - min_stability) / (max_stability + min_stability)

    h_total = coin_parity + mobility + 2 * edge_occupancy + 5 * corner_occupancy + 10 * stability

    nadjene_heuristike[zobristHash(position)] = h_total

    return h_total

hash_table1 = [[random.getrandbits(64) for _ in range(8)] for _ in range(8)]
hash_table2 = [[random.getrandbits(64) for _ in range(8)] for _ in range(8)]

def zobristHash(board):
    hash = 0
    table = []
    for i in range(0, len(board)):
        niz = []
        for j in range(0, len(board[i])):
            niz.append(board[i][j].getValue())
        table.append(niz)

    for i in range(0, len(table)):
        for j in range(0, len(table[i])):
            if table[i][j] != 0:
                piece = table[i][j]
                if piece == -1:
                    hash ^= hash_table1[i][j]
                else:
                    hash ^= hash_table2[i][j]

    return hash

def paritet(board, igrac):
    paritet = 0
    boja = -1 if igrac == 1 else 1
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j].getValue() == boja:
                paritet += 1
    return paritet

def mobilnost(board, igrac):
    return brojValidnihPoteza(nadjiValidnePozicije(board, igrac))

def ivice(board, igrac):
    ivice = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if (i == 0 or i == 7 or j == 0 or j == 7) and board[i][j].getValue() == igrac:
                ivice += 1
    return ivice

def stabilnost(board, row, col, igrac):
    if (row == 0 and col == 0) or (row == 0 and col == 7) or \
            (row == 7 and col == 0) or (row == 7 and col == 7):
        return "stable"

    if row == 0 or row == 7 or col == 0 or col == 7:
        return "semi-stable"

    boja = igrac
    protivnik = -1 if boja == 1 else 1

    for i in range(col - 1, -1, -1):
        if board[row][i].getValue() == protivnik:
            return "unstable"
        if board[row][i].getValue() == boja:
            break
    for i in range(col + 1, 8):
        if board[row][i].getValue() == protivnik:
            return "unstable"
        if board[row][i].getValue() == boja:
            break

    for i in range(row - 1, -1, -1):
        if board[i][col].getValue() == protivnik:
            return "unstable"
        if board[i][col].getValue() == boja:
            break
    for i in range(row + 1, 8):
        if board[i][col].getValue() == protivnik:
            return "unstable"
        if board[i][col].getValue() == boja:
            break

    i = row - 1
    j = col - 1
    while i >= 0 and j >= 0:
        if board[i][j].getValue() == protivnik:
            return "unstable"
        if board[i][j].getValue() == boja:
            break
        i -= 1
        j -= 1
    i = row + 1
    j = col + 1
    while i < 8 and j < 8:
        if board[i][j].getValue() == protivnik:
            return "unstable"
        if board[i][j].getValue() == boja:
            break
        i += 1
        j += 1

    i = row - 1
    j = col + 1
    while i >= 0 and j < 8:
        if board[i][j].getValue() == protivnik:
            return "unstable"
        if board[i][j].getValue() == boja:
            break
        i -= 1
        j += 1
    i = row + 1
    j = col - 1
    while i < 8 and j >= 0:
        if board[i][j].getValue() == protivnik:
            return "unstable"
        if board[i][j].getValue() == boja:
            break
        i += 1
        j -= 1

    return "semi-stable"

def stabilnostListe(board, igrac):
    stable = 0
    semi_stable = 0
    unstable = 0
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j].getValue() == -igrac:
                continue
            if stabilnost(board, i, j, igrac) == "stable":
                stable += 1
            elif stabilnost(board, i, j, igrac) == "semi-stable":
                semi_stable += 1
            elif stabilnost(board, i, j, igrac) == "unstable":
                unstable += 1
    return stable, semi_stable, unstable

def coskovi(board, igrac):
    coskovi = 0
    if board[0][0].getValue() == igrac:
        coskovi += 1
    if board[0][7].getValue() == igrac:
        coskovi += 1
    if board[7][0].getValue() == igrac:
        coskovi += 1
    if board[7][7].getValue() == igrac:
        coskovi += 1
    return coskovi

def potezRacunara(board):
    global broj, global_timer
    broj = 0
    alpha = float('-inf')
    beta = float('inf')
    lista = listaValidnihPozicija(board)
    depth = 8
    copy1 = copy.deepcopy(board)
    score = 0
    max = float('-inf')
    maxPos = (0, 0)

    for pos in lista:
        global_timer = time.time()
        score = minimax(copy1, depth - 1, alpha, beta, False, -1, pos)

        if score[0] > max:
            max = score[0]
            maxPos = (score[1][0], score[1][1])

        if time.time() - global_timer > 3:
            break

    return odigrajPotez(board, maxPos[0], maxPos[1], -1)


#Boje
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
GRAY = (128, 128, 128)

#Velicina ekrana i polja
SCREEN_SIZE = (840, 940)
SQUARE_SIZE = SCREEN_SIZE[0] // 8

#Displej
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Reversi/Othello")

#Igraci 1 ili -1
igrac = 1
poeni1 = 2
poeni2 = 2

#Polja
board = [8 * [Field(0, False)] for i in range(0,8)]

crtajTablu()

#Postavljanje pocetne pozicije
board[3][3] = Field(1, False)
board[3][4] = Field(-1, False)
board[4][3] = Field(-1, False)
board[4][4] = Field(1, False)

font = pygame.font.Font(None, 36)

osveziSemafor(board)

board = nadjiValidnePozicije(board, igrac)
osveziDiskove(board)

nadjene_heuristike = {}

#Igra
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            row = pos[1] // SQUARE_SIZE
            column = pos[0] // SQUARE_SIZE

            if row > 7 or column > 7 or not board[row][column].isValid():
                continue
            if igrac == 1:
                if board[row][column].getValue() == 0:
                    board = odigrajPotez(board, row, column, igrac)
                    osveziDiskove(board)
                    igrac = -1

            board = ponistiValidnostPozicija(board)
            board = nadjiValidnePozicije(board, igrac)
            osveziSemafor(board)

            if brojValidnihPoteza(board) == 0:
                if poeni1 > poeni2:
                    messagebox.showinfo('Kraj igre','IGRAC1 je pobedio')
                elif poeni1 < poeni2:
                    messagebox.showinfo('Kraj igre','IGRAC2 je pobedio')
                else:
                    messagebox.showinfo('Kraj igre','NERESENO!')
                running = False

            copyBoard = copy.deepcopy(board)
            start_time = time.time()
            board = potezRacunara(copyBoard)
            elapsed_time = time.time() - start_time
            print(elapsed_time)
            osveziDiskove(board)

            igrac = 1

            board = ponistiValidnostPozicija(board)
            board = nadjiValidnePozicije(board, igrac)
            osveziSemafor(board)
            if brojValidnihPoteza(board) == 0:
                if poeni1 > poeni2:
                    messagebox.showinfo('Kraj igre','IGRAC1 je pobedio')
                elif poeni1 < poeni2:
                    messagebox.showinfo('Kraj igre','IGRAC2 je pobedio')
                else:
                    messagebox.showinfo('Kraj igre','NERESENO!')
                running = False

            osveziDiskove(board)

pygame.quit()