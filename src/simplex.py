# -*- coding: utf-8 -*-


class Simplex:

    def __init__(self, tableau):
        self.tableau = tableau
        self.answer = None

    def run(self):
        self.__second_phase()

        self.tableau.show(answer=self.answer)

    def __second_phase(self):

        if self.tableau.goes_to_minus_inf():
            self.answer = "Não há solução, pois z tende a infinito negativo"
            return

        while not self.tableau.is_solution():
            i, j = self.tableau.get_pivot()
            self.tableau.change_base(i, j)

            if self.tableau.goes_to_minus_inf():
                self.answer = "Não há solução, pois z tende a infinito negativo"
                return

        tmp = ""
        if self.tableau.is_degenerate():
            tmp = " e degenerada"

        if self.tableau.has_multiple_solutions():
            self.answer = "Solução múltipla" + tmp
        else:
            self.answer = "Solução única" + tmp
