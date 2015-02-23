# coding: utf-8


class SomaMaxima:
    def __init__(self, seq):
        self.primeiro = 0
        self.ultimo = len(seq) -1
        self.seq = seq

    def __call__(self):
        self.reduce_lists()
        return self.primeiro, self.ultimo

    def reduce_lists(self):
        acumulado = 0
        soma_atual = 0
        primeiro = _primeiro = ultimo = 0 
    
        for i, j in enumerate(self.seq):
            if soma_atual + j >= 0:
                soma_atual += j
            else:
                _primeiro = i + 1
                soma_atual = 0
            
            if soma_atual >= acumulado:
                acumulado = soma_atual
                primeiro = _primeiro
                ultimo = i
        
        self.primeiro = primeiro
        self.ultimo = ultimo