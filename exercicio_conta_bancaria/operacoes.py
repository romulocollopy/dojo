#coding: utf-8

from datetime import date
from decimal import Decimal

""" Operações para transações bancárias"""

class Conta:
    """ Classe Conta Bancária """

    def __init__(self, user, name, saldo=0, lancamentos=[]):
        assert isinstance(user, Usuario), ('Argumento 1, \"Usuário\" deve' +
                                            'ser do tipo Usuario')
        self.user = user

        assert isinstance(name, str), ('Argumento 2, \"nome\" deve ser uma' +
                                       'string')

        try:
            self.__saldo = Decimal(saldo)
        except ValueError:
            print('Argumento 3, \"saldo\", deve ser um número Real')

        self.name = name
        self.__lancamentos = [l for l in lancamentos
                              if isinstance(l, Lancamento)]

    @property
    def saldo(self):
        """ propriedade protegida """
        return self.__saldo

    def retirar(self, value, categoria='Padrão', subcategoria=None):
        """ realiza um saque na conta"""

        value = value if value > 0 else 0
        self.__saldo -= value
        self.__lancamentos.append(Lancamento(-1, value, date.today(),
                                  categoria, subcategoria))

        if value > self.__saldo:
            message = 'Atenção, sua conta está negativa em R$ {0}'.format(
                abs(self.__saldo))
        else:
            message = 'Saldo atual da conta {0}.{1} é de R$ {2}'
            message = message.format(self.user.name, self.name, self.__saldo)

        print(message)

    def depositar(self, value, categoria='Padrão', subcategoria=None):
        """ realiza um depósito na conta"""

        value = value if value > 0 else 0
        self.__saldo += value
        self.__lancamentos.append(Lancamento(1, value, date.today(), categoria,
                                  subcategoria))

        message = 'Saldo atual da conta {0}.{1} é de R$ {2}'
        message = message.format(self.user.name, self.name, self.__saldo)

        print(message)

    def transferir(self, conta, value, categoria='Padrão', subcategoria=None):
        """ Transfere valor de da conta que chama o método para a conta no
        argumento """

        assert isinstance(conta, Conta), ('Argumento 1, \"conta\" deve ser' +
                                          ' do tipo Conta')
        self.retirar(value,'Transferência')
        conta.depositar(value,'Transferência')

        message = ('Transferência no valor de R$ {0} realizada' +
                   ' de "{1}.{2}" para "{3}.{4}"')

        message = message.format(value, self.user.name, self.name,
                                 conta.user.name, conta.name)

        print(message)

    @property
    def lancamentos(self,):
        """ Atributo lancamentos é protegido """
        return self.__lancamentos

    def filter(self, filterByCategory=False, filterByPeriod=False,
               filterByType=False):

        lancamentos = self.__lancamentos

        def lancamento_date(lancamento):
            return lancamento.data

        if filterByCategory:
            lancamentos = [i for i in lancamentos
                           if i.categoria == filterByCategory]

        if filterByType:
            lancamentos = [i for i in lancamentos
                           if i.tipo == filterByType]

        if filterByPeriod:
            if not isinstance(filterByPeriod[0], date):

                initial_date = [int(i) for i in filterByPeriod[0].split('-')]
                initial_date = date(*initial_date)

                final_date = [int(i) for i in filterByPeriod[1].split('-')]
                final_date = date(*final_date)

            else:
                initial_date = filterByPeriod[0]
                final_date = filterByPeriod[1]

            lancamentos = [i for i in lancamentos
                           if i.data >= initial_date
                           and i.data <= final_date]

        return sorted(lancamentos, key=lancamento_date)


class Usuario:
    """ Classe Usuário """
    def __init__(self, name, **kwargs):
        self.name = name


class Lancamento:
    def __init__(self, tipo, valor, data, categoria, subcategoria=None):

        assert tipo == 1 or tipo == -1, ('Argumento 1, \"tipo\", deve receber' +
                                         ' 1 para receita ou 0 para despesa')
        self.tipo = tipo

        try:
            self.valor = Decimal(valor)
        except ValueError:
            print('Argumento 2, \"valor\", deve ser um número Real')

        if isinstance(data, date):
            self.data = data
        elif isinstance(data, str):
            try:
                data = [int(i) for i in data.split('-')]
                self.data = date(*data)
            except ValueError:
                print('Argumento 3, \"data\", deve receber um objeto'+
                      'datetime.date ou string no formato AAAA-MM-DD')

        assert isinstance(categoria, str), \
            'Argumento 4, \"categoria\", deve receber um nome.'

        self.categoria = categoria
        self.subcategoria = subcategoria
