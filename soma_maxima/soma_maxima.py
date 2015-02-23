# coding: utf-8


class SomaMaxima:
    def __init__(self, seq):
        self.primeiro = 0
        self.ultimo = len(seq) -1
        self.seq = seq

    def __call__(self):
        self.retira_negativos_inicio()
        self.retira_negativos_fim()
        self.retira_negativo_grande()
        self.reduce_lists()
        return self.primeiro, self.ultimo

    def retira_negativo_grande(self):
        """ se um negativo anular um lado da sequencia, ele é retirado """

        try:
            val, pos = self.encontra_negativo_maior()
        except TypeError:
            return None

        fatia_inicio, fatia_fim = self.divide_sequencia(pos)
        soma_inicio = sum(fatia_inicio)
        soma_fim = sum(fatia_fim)

        if soma_inicio == soma_fim and soma_inicio + val >= 0:
            return None

        if soma_inicio < soma_fim:
            self.seq = fatia_fim
            self.primeiro += pos+1
        else:
            self.seq = fatia_inicio
            self.ultimo -= pos-1

    def reduce_lists(self):
        sum_dict = {}
        listas = []
        for i, j in enumerate(self.seq):
            for k in range(len(self.seq)):
                listas += self.seq[i:k]
                sum_dict[sum(listas)] = (listas, i, i+len(listas)-1)

        maximo = max(list(sum_dict.keys()))
        self.primeiro = sum_dict[maximo][1]
        self.ultimo = sum_dict[maximo][2]
        print (sum_dict[maximo])




    def divide_sequencia(self, pos):
        fatia_inicio = self.seq[:pos]
        fatia_fim = self.seq[pos+1:]
        return fatia_inicio, fatia_fim

    def encontra_negativo_maior(self):
        negativos = self.encontra_negativos()
        min_candidate = 0
        unique = True
        pos_seq = None

        for val, pos in negativos:
            if val < min_candidate:
                min_candidate = val
                unique = True
                pos_seq = pos
            elif val == min_candidate:
                unique = False

        if unique and pos_seq:
            return min_candidate, pos_seq

    def encontra_negativos(self):
        return [(val, pos) for pos, val in enumerate(self.seq) if val < 0 ]

    def retira_negativos_inicio(self):
        pos = self.conta_negativos_em_sequencia(self.seq)
        self.primeiro += pos
        self.seq = self.seq[pos:]

    def retira_negativos_fim(self):
        pos = self.conta_negativos_em_sequencia(self.seq[::-1])
        if pos:
            self.seq = self.seq[:-pos]
        self.ultimo -= pos

    def conta_negativos_em_sequencia(self, seq):
        count = 0
        for i in seq:
            if i < 0:
                count += 1
            else:
                break

        return count
