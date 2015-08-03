#!/usr/lib/python3.3
#coding: utf-8

""" Exercício proposto em repositório Innvent
https://github.com/innvent/jobs/blob/master/estagio-dev-bh.md """


import os
from operacoes import *

class Menu:
    def __init__(self):
        self.option = ''
        self.users = {}
        self.accounts = {}
        self.options = ('u: criar novo Usuário; \t\t\t' +
                        'c: criar nova Conta;\n' +
                        'd: realizar um depósito; \t\t' +
                        'r: realizar uma Retirada;\n' +
                        't: realizar uma Transferência \t\t' +
                        'l: listar Lançamentos\n' +
                        's: ver um Saldo \t\t \n\n' +
                        'q: sair')

    def header(self, str):
        os.system('cls' if os.name == 'nt' else 'clear')
        if len(str) < 80:
            spaces = int((80 - len(str))/2)
        print('*'*80)
        print(' '*spaces + str)
        print('*'*80+'\n\n')

    def inicio(self):
        self.header('Programa de finanças pessoais!')
        print(self.options)

    def listausuarios(self):
        for user in self.users:
            print(user)

    def selecionausuario(self):
        self.listausuarios()

        usuario = input('Insira o nome do usuario ou "I" para Inicio: ')

        if usuario == "I":
            self.option = ''
            return False

        if usuario not in self.users:
            print('Insira o nome do usuario ou "I" para retornar ao Inicio: ')
            self.selecionausuario()
        else:
            return self.users[usuario]

    def listacontas(self):
        for account in self.accounts.values():
            print(account.user.name + '.' + account.name)

    def selecionaconta(self):
        self.listacontas()
        conta = input('Insira o nome da conta ou "I" para Inicio: ')

        if conta == "I":
            self.option = ''
            return False

        if conta not in self.accounts:
            print('Por favor, escolha uma conta listada:')
            self.selecionaconta()
        else:
            return self.accounts[conta]

    def criarusuario(self):
        self.header('Criar novo usuário')
        nome = input('Insira o nome do usuário: ')
        self.users[nome] = Usuario(nome)

    def criarconta(self):
        self.header('Criar nova conta')
        name = input('Insira o nome da conta: ')

        print('Usuários existentes:')
        user = self.selecionausuario()

        if user:
            self.accounts[user.name+'.'+name] = Conta(user, name)
            message = ('Conta "{0}" criada para' +
                       ' usuário "{1}"').format(name, user.name)
            print(message+'\n\n')

            input('pressione qualquer tecla para voltar ao menu')

    def realizardeposito(self):
        self.header('Realizar um depósito')
        print('Contas existentes')

        conta = self.selecionaconta()
        if conta:
            valor = Decimal(input('Insira o valor do depósito: '))
            categoria = input('Insira o nome da Categoria: ')
            subcategoria = input('Insira o nome da Subcategoria: ')
            conta.depositar(valor, categoria, subcategoria)

            input('pressione qualquer tecla para voltar ao menu')

    def realizarretirada(self):
        self.header('Realizar uma retirada')
        print('Contas existentes')
        conta = self.selecionaconta()
        if conta:
            valor = Decimal(input('Insira o valor da retirada: '))
            categoria = input('Insira o nome da Categoria: ')
            subcategoria = input('Insira o nome da Subcategoria: ')
            conta.retirar(valor, categoria, subcategoria)

            input('pressione qualquer tecla para voltar ao menu')

    def realizartransferencia(self):
        self.header('Realizar uma Transferência')

        print('Selecione a conta de origem')
        conta_origem = self.selecionaconta()

        if conta_origem:
            valor = Decimal(input('Insira o valor a transferir: '))

            print('Selecione a conta de destino')
            conta_destino = self.selecionaconta()

            if conta_destino:
                conta_origem.transferir(conta_destino, valor)

            input('pressione qualquer tecla para voltar ao menu')

    def selecionalancamentos(self, conta, filtro=None):
        if conta:
            if not filtro:
                for l in conta.lancamentos:
                    tipo = 'Crédito' if l.tipo == 1 else 'Débito'
                    data = '{0}/{1}/{2}'.format(l.data.day, l.data.month,
                                                l.data.year)
                    print(data, '\t', tipo, '\t', l.valor, '\t',
                          l.categoria, '\t', l.subcategoria)
            else:
                for l in conta.filter(**filtro):
                    tipo = 'Crédito' if l.tipo == 1 else 'Débito'
                    data = '{0}/{1}/{2}'.format(l.data.day, l.data.month,
                                                l.data.year)
                    print(data, '\t', tipo, '\t', l.valor, '\t',
                          l.categoria, '\t', l.subcategoria)

    def listalancamentos(self):
        self.header('Lista lancamentos')
        print('Por favor, selecione uma conta')
        conta = self.selecionaconta()
        self.selecionalancamentos(conta)

        opt = input('Pressione "F" para filtrar outra tecla qualquer para' +
                    ' voltar: ')

        if opt == 'F':
            filtro = input('Insira C para categoria, T para Tipo ou' +
                           ' P para periodo: ')
            if filtro == 'C':
                cat = input('Insira o nome da Categoria: ')
                self.selecionalancamentos(conta, {'filterByCategory': cat})
                input('pressione qualquer tecla para voltar ao menu')

            elif filtro == 'T':
                tipo = input('Insira "-1" para Débito ou "1" para Crédito: ')
                self.selecionalancamentos(conta, {'filterByType': int(tipo)})
                input('pressione qualquer tecla para voltar ao menu')

            elif filtro == 'P':
                inicial = input('Insira a data inicial (AAAA-MM-DD): ')
                final = input('Insira a data final (AAAA-MM-DD): ')
                self.selecionalancamentos(conta,
                                          {'filterByPeriod': [inicial, final]})
                input('pressione qualquer tecla para voltar ao menu')

    def exibesaldo(self):
        self.header('Lista lancamentos')
        conta = self.selecionaconta()
        if conta:
            print('"{0}" tem R$ {1} de saldo'.format(conta.name, conta.saldo))
            input('pressione qualquer tecla para voltar ao menu')

    def run(self):
        while self.option != 'q':

            if self.option == 'u':
                self.criarusuario()
                self.inicio()
                self.option = input('Por favor selecione uma opção: ')

            elif self.option == 'c':
                self.criarconta()
                self.inicio()
                self.option = input('Por favor selecione uma opção: ')

            elif self.option == 'd':
                self.realizardeposito()
                self.inicio()
                self.option = input('Por favor selecione uma opção: ')

            elif self.option == 'r':
                self.realizarretirada()
                self.inicio()
                self.option = input('Por favor selecione uma opção: ')

            elif self.option == 't':
                self.realizartransferencia()
                self.inicio()
                self.option = input('Por favor selecione uma opção: ')

            elif self.option == 'l':
                self.listalancamentos()
                self.inicio()
                self.option = input('Por favor selecione uma opção: ')

            elif self.option == 's':
                self.exibesaldo()
                self.inicio()
                self.option = input('Por favor selecione uma opção: ')

            else:
                self.inicio()
                self.option = input('Por favor selecione uma opção: ')


def main():
    menu = Menu()
    menu.run()

if __name__ == '__main__':
    main()
