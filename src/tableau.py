# -*- coding: utf-8 -*-

class Tableau:
    def __init__(self, file_name):
        self.tableau = None
        self.I = None
        self.J = None
        self.A = None
        self.option = None
        self.tableau_n = 0

        self.__load_tableau_from_file(file_name)

    def show(self, out=None, inn=None, answer=None, custom=None):
        if answer is not None:
            tableau_info = "Tableau Final: " + answer
            final_space = "\n\n"
        elif custom is not None:
            tableau_info = "Tableau {}: ".format(self.tableau_n) + custom
            self.tableau_n += 1
            final_space = ""
        else:
            tableau_info = "Tableau {}: Vai entrar x{} e sair x{}".format(
                self.tableau_n, inn, self.I[out - 1]
            )
            self.tableau_n += 1
            final_space = ""

        print("\n\n" + tableau_info + "\n" + self.__str__() + final_space)

    def __str__(self):
        header = ['z'] + ['x' + str(i) for i in self.I]
        sets = "I: " + str(self.I) + "     J: " + str(self.J)
        if self.option == 1:
            z = 'z* = ' + '{0:.3f}'.format(self.tableau[1 - 1][0])
        else:
            z = 'z* = ' + '{0:.3f}'.format(self.tableau[1 - 1][0]*-1)

        solution = [0.0] * (len(self.tableau[0]) - 1)
        for i in range(0, len(self.I)):
            solution[self.I[i] - 1] = self.tableau[i + 1][0]

        tmp = [['', 'b'] + ['x' + str(x) for x in range(1, len(self.tableau[0]))]]
        tmp += [[header[i]] + ['{0:.3f}'.format(x) for x in self.tableau[i]] for i in range(0, len(self.tableau))]

        shift = max([len(e) for row in tmp for e in row])

        separator = '+' + '+'.join(['~' * shift for _ in range(0, len(self.tableau[0]) + 1)]) + '+'

        return (
            separator
            + "\n"
            + ''.join(
                ['|' + '|'.join('{0:>{shift}}'.format(x, shift=shift) for x in row) + '|\n' for row in tmp]
            )
            + separator
            + "\n"
            + sets
            + "\n"
            + z
            + '\nx* = ('
            + ', '.join(['{0:.3f}'.format(s) for s in solution])
            + ')'
        )

    def __load_tableau_from_file(self, file_name):
        not_in_format_msg = "O arquivo não está no formato correto ou o PPL não está na forma padrão."

        with open(file_name, 'r') as file:
            self.option = int(file.readline().replace('\n', ''))

            if self.option not in {1, 2}:
                raise ValueError(not_in_format_msg)

            rows, cols = map(int, file.readline().replace('\n', '').split())
            m = rows - 1

            self.tableau = [list(map(float, file.readline().replace('\n', '').split())) for _ in range(0, m + 1)]

            # ld na primeira coluna
            for i in range(0, rows):
                self.tableau[i] = [self.tableau[i][-1]] + self.tableau[i][0:-1]

            # lista em ordem das variáveis básicas
            self.I = []
            for j in range(0, cols):
                n_zeros = 0
                n_ones = 0

                jj = j
                for i in range(1 - 1, rows):
                    if self.tableau[i][j] == 1.0:
                        n_ones += 1
                        ii = i
                    elif self.tableau[i][j] == 0.0:
                        n_zeros += 1
                    else:
                        break

                if n_ones == 1 and n_zeros == m:
                    self.I.append((ii, jj))

            if len(self.I) != m:
                raise ValueError(not_in_format_msg)

            self.I = list(zip(*self.I))[1]
            self.I = list(self.I)  # Converta self.I para uma lista aqui
            self.J = [j for j in range(1, cols) if j not in self.I]  # exceto 1 porque é LD

            # Invert the sign of the coefficients in the objective function for minimize
            #if self.option == 1:
            self.tableau[0] = [-x for x in self.tableau[0]]  # invertindo o sinal

        self.I = list(self.I)  # Converta self.I para uma lista aqui

    def change_base(self, i, j):
        div = self.tableau[i][j]
        self.tableau[i] = list(map(lambda x: x / div, self.tableau[i]))

        tmp_range = [x for x in range(0, len(self.tableau)) if x != i]
        
        for ii in tmp_range:
            b = -self.tableau[ii][j]
            tmp = list(map(lambda x: x * b, self.tableau[i]))
            self.tableau[ii] = list(map(lambda a: sum(a), zip(tmp, self.tableau[ii])))
        
        self.__adjust_JI(i, j)

    def __adjust_JI(self, i, j):
        tmp = self.I[i - 1]
        self.I[i - 1] = j
        self.J.remove(j)
        self.J.append(tmp)
        self.J.sort()


    def get_pivot(self):
        j = max(map(lambda j: (j, self.tableau[0][j]), self.J), key=lambda x: x[1])[0]
        l = [i for i in range(1, len(self.tableau)) if self.tableau[i][j] > 0.0]
        l = [(self.tableau[i][0] / self.tableau[i][j], i) for i in l]
        i = min(l, key=lambda div: div[0])[1]
        self.show(i, j)
        return i, j

    def is_degenerate(self):
        for row in self.tableau[1:]:  # 1: só roda na opção 1
            if row[0] == 0.0:
                return True
        return False

    def has_multiple_solutions(self):
        return max([self.tableau[0][j] for j in self.J]) == 0.0

    def is_M_empty(self):
        return self.tableau[0][0] != 0.0

    def is_solution(self):
        return max([self.tableau[0][j] for j in self.J]) <= 0.0

    def goes_to_minus_inf(self):
        for j in self.J:
            inf = True
            if self.tableau[0][j] > 0.0:  # apenas se for candidata a entrar na base!
                for row in self.tableau[1:]:  # só verificado na opção 1 (segunda fase)
                    if row[j] > 0.0:
                        inf = False
                        break
                if inf:  # -infinito
                    return True
        return False
