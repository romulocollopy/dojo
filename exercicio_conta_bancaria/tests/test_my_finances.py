#coding: utf-8

""" Processo seletivo Innvent
https://github.com/innvent/jobs/blob/master/estagio-dev-bh.md """


from unittest import TestCase
from datetime import date, timedelta

from my_finances import *


class InitTestCase(TestCase):
    def setUp(self):
        self.user = Usuario('Rômulo Collopy', CPF="666.666.666-66")
        self.lancamentos = [Lancamento(1, 7544.25, date.today()-timedelta(15),
                                       'Salário'),
                            Lancamento(-1, 1500, date.today() - timedelta(10),
                                       'Aluguel'),
                            Lancamento(-1, 535.4, date.today() - timedelta(5),
                                       'Compras'),
                            Lancamento(-1, 232.33, date.today(),
                                       'Telefone'),
                            Lancamento(-1, 16.99, date.today() + timedelta(5),
                                       'XVideos'),
                            ]
        self.conta = Conta(self.user, 'Conta Corrente', 820, self.lancamentos)
        self.conta_destino = Conta(self.user, 'Conta Poupança', 100)


class SaldoIsProtectedTestCase(InitTestCase):
    def runTest(self):
        """ Não deve ser possível atribuir um saldo após instaciação """

        try:
            self.conta.saldo = -533
        except:
            pass
        self.assertEqual(self.conta.saldo, 820)


class DepositoTestCase(InitTestCase):
    def runTest(self):
        """ Depósito deve somar ao saldo """

        self.conta.depositar(180)
        self.assertEqual(self.conta.saldo, 1000)


class RetiradaTestCase(InitTestCase):
    def runTest(self):
        """ Retirada deve diminuir do saldo """

        self.conta.retirar(920)
        self.assertEqual(self.conta.saldo, -100)


class TransferenciaTestCase(InitTestCase):
    def runTest(self):
        """ Transferência deve diminuir o valor da conta que chama o método e
        adicionar na conta pasada nos argumentos """

        self.conta.transferir(self.conta_destino, 100)
        self.assertEqual(self.conta.saldo, 720)
        self.assertEqual(self.conta_destino.saldo, 200)


class LancamentoTestCase(InitTestCase):
    def runTest(self):
        """ Um lancamento deve ser adicionado a cada operação """

        self.conta.depositar(180)
        self.conta.retirar(180)
        self.conta.transferir(self.conta_destino, 100)

        self.assertEqual(len(self.conta.lancamentos), 8)


class DateFilterTestCase(InitTestCase):
    def runTest(self):
        """ Filtro pela data de hoje deve retornar apenas um lancamento """

        self.assertEqual(len(self.conta.filter(filterByPeriod=[date.today(),date.today()])), 1)

class ClassFilterTestCase(InitTestCase):
    def runTest(self):
        """ Filtro pela categoria \'Xvideos\' deve retornar apenas um lancamento """

        self.assertEqual(len(self.conta.filter(filterByCategory='XVideos')), 1)

class TipoFilterTestCase(InitTestCase):
    def runTest(self):
        """ Filtro pelo tipo deve retornar o número de operações do tipo """

        self.assertEqual(len(self.conta.filter(filterByType=1)), 1)
        self.assertEqual(len(self.conta.filter(filterByType=-1)), 4)
