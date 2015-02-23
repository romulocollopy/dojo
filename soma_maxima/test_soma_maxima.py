# coding: utf-8

import unittest

from unittest import TestCase

from soma_maxima import SomaMaxima

"""

TestCase para problema da soma máxima

Dado um conjunto de números, descobrir o subconjunto em que a soma dos
elementos são de máxima soma.

Exemplo: dado o conjunto de elementos [2, -4, 6, 8, -10, 100, -6, 5]

O subconjunto de soma máxima é: [6, 8, -10, 100]

Assim, o programa deve retornar a posição do primeiro e do último elemento
da subcadeia. Neste exemplo, as posições 2 e 5, considerando a primeira
posição com índice 0.

"""

class TestSomaMaxima(TestCase):

    def test_sequencia_de_positivos_retorna_primeiro_e_ultimo(self):
        seq = SomaMaxima([1, 1, 1, 1, 1])
        seq2 = SomaMaxima([1, 1, 1, 1, 1, 1, 1])
        self.assertEqual((0, 4), seq())
        self.assertEqual((0, 6), seq2())

    def test_zero_e_includo_na_lista_de_SomaMaxima(self):
        seq = SomaMaxima([0, 1, 1, 1, 0])
        self.assertEqual((0,4), seq())

    def test_negativo_no_inicio_e_descartado(self):
        seq = SomaMaxima([-3, 1, 1, 1, 1])
        self.assertEqual((1,4), seq())

    def test_negativo_no_final_e_descartado(self):
        seq = SomaMaxima([1, 1, 1, 1, -3])
        self.assertEqual((0, 3), seq())

    def test_negativo_no_inicio_e_final_sao_descartados(self):
        seq = SomaMaxima([-3, 1, 1, 1, -3])
        self.assertEqual((1, 3), seq())

    def test_sequencia_de_negativos_no_inicio_e_final_sao_descartados(self):
        seq = SomaMaxima([-3, -3, -3, 1, 1, 1, 1, -3, -3])
        self.assertEqual((3, 6), seq())

    def test_negativo_grande_exclui_positivo_do_inicio(self):
        seq = SomaMaxima([1, -3, 1, 1, 1])
        self.assertEqual((2,4), seq())

    def test_negativo_grande_exclui_positivo_do_fim(self):
        seq = SomaMaxima([1, 1, 1, -3, 1])
        self.assertEqual((0,2), seq())

    def test_negativo_grande_exclui_fim_depois_de_descartar(self):
        seq = SomaMaxima([-1, -1, 1, 1, 1, -3, 1, -1, -1, -1])
        self.assertEqual((2,4), seq())

    def test_negativo_grande_exclui_inicio_depois_de_descartar(self):
        seq = SomaMaxima([-1, -1, 1, -3, 1, 1, 1, -1, -1, -1])
        self.assertEqual((4,6), seq())

    def test_negativo_menor_nao_exclui_inicio_depois_de_descartar(self):
        seq = SomaMaxima([1, 1, 1, -3, 1, 1, 1, -1, -1, -1])
        self.assertEqual((0,6), seq())

    def test_sequencia_negativa_grande_exclui_inicio(self):
        seq = SomaMaxima([1, 1, -3, -3, 1, 1, 1])
        self.assertEqual((4,6), seq())

    def test_sequencia_negativa_grande_exclui_fim(self):
        seq = SomaMaxima([1, 1, 1, -3, -3, 1, 1])
        self.assertEqual((0,2), seq())


    def test_com_sequencia_proposta(self):
        seq = SomaMaxima([2, -4, 6, 8, -10, 100, -6, 5])
        self.assertEqual((2, 5), seq())

unittest.main()
