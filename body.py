from asyncio import events
from calendar import day_abbr
from distutils.log import info
from operator import length_hint
from tkinter import Button
import PySimpleGUI as sg
import datetime
import PGSQL
from random import randint


# função:inicio
# ---------------------------------------------------------------------------------------------
def inicio():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Agenda de Lembretes')],
        [sg.Button('Sair'), sg.Button('Creditos'), sg.Button('Entrar')]
    ]
    window = sg.Window('Agenda de Lembretes', layout, size=(
        500, 100), element_justification='center')
    while True:
        button, values = window.read()
        if button == 'Sair' or button == sg.WINDOW_CLOSED:
            break
        if button == 'Entrar':
            window.close()
            mainpage()
        if button == 'Creditos':
            window.close()
            creditos()

# ---------------------------------------------------------------------------------------------


# função créditos
# ---------------------------------------------------------------------------------------------
def creditos():
    layout = [
        [sg.Text('Projeto de Computação 2')],
        [sg.Text('Feito por Rafael e João Victor')],
        [sg.Text('Professor Jonathan Nogueira')],
        [sg.Button('Voltar'), sg.Button('Sair')]
    ]
    window = sg.Window('Pagina Inicial', layout, size=(
        500, 150), element_justification='center')
    while True:
        button, values = window.read()
        if button == 'Sair' or button == sg.WINDOW_CLOSED:
            break
        if button == 'Voltar':
            window.close()
            inicio()
# ---------------------------------------------------------------------------------------------


def mainpage():

    [sg.theme('Reddit')]
    layout = [[sg.Text('Informe o nome do compromisso, horário, data, e humor')],
              [sg.Text('Nome do compromisso', size=(10, 2)),
               sg.InputText(key='-NAME-')],
              [sg.Text('Horário', size=(10, 2)), sg.Slider(
                  (0, 23), orientation='h', s=(20, 10), k='-Horas-')],
              [sg.Text('Minutos', size=(10, 2)), sg.Slider(
                  (0, 60), orientation='h', s=(20, 10), k='-Minutos-')],
              [sg.Text('Informe a data', size=(10, 2)), sg.Input(key='-DATE-', size=(10, 2)), sg.CalendarButton(
                  'Data',  target='-DATE-', format='%d/%m/%Y', default_date_m_d_y=(1, None, 2022), )],
              [sg.Text('Diga como se sente em relação ao evento', size=(10, 5)), sg.OptionMenu(
                  ['Gosto bastante', 'É OK', 'Odeio com todas as forças'], s=(30, 2))],
              [sg.Button('Submit'), sg.Button('Exit'), sg.Button('Show Table'), sg.Button('Voltar'), ]]

    window = sg.Window('Assitente de rotina', layout)

    while True:

        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Voltar':
            window.close()
            inicio()
        elif event == 'Submit':
            # convertendo int de hora e minutos para datime
            # ---------------------------------------------------------------------------------------------
            NAME = values['-NAME-'].capitalize()
            DATE = values['-DATE-'].capitalize()

            if NAME == '' or DATE == '':
                sg.popup("Digite informações validas para criar o lembrete")

            if NAME != '' and DATE != '':
                day = int(values['-DATE-'].split('/')[0])
                month = int(values['-DATE-'].split('/')[1])
                year = int(values['-DATE-'].split('/')[2])
                Horas = int(values['-Horas-'])
                Minutos = int(values['-Minutos-'])

                tempo = datetime.datetime(
                    day=day, month=month, year=year, hour=Horas, minute=Minutos)
                tempo.strftime('%d%m%y%h%M')
                NAME = (values['-NAME-'])
                DATE = tempo
                PGSQL.write(NAME, DATE)

                sg.popup("Sucesso")


# ---------------------------------------------------------------------------------------------
        elif event == 'Show Table':
            NAME = PGSQL.readname()
            DATE = PGSQL.readDate()
            if NAME:
                window.close()
                Table()
            else:
                sg.popup("Não ha pessoas cadastradas")

#  função array data


def Arrayinfo():
    Compromisso_array = []
    for x in range(len(PGSQL.readname())):
        Compromisso = [PGSQL.readname()[x], PGSQL.readDate()[x]]
        Compromisso_array.append(Compromisso)
    return Compromisso_array

# função table
# ---------------------------------------------------------------------------------------------


def Table():

    headings = ['Compromisso', 'Data']
    layout = [
        [sg.Table(values=Arrayinfo(), headings=headings, max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=True,
                  justification='right',
                  num_rows=20,
                  key='-TABLE-',
                  row_height=35,
                  tooltip='Compromisso info'),
         [sg.Button('Sair'), sg.Button('Voltar'),
          sg.Button('Excluir Compromisso')]
         ]
    ]
    window = sg.Window('ShowTable', layout)
    while True:
        event, values = window.read()
        if event == 'Sair' or event == sg.WINDOW_CLOSED:
            break
        if event == 'Voltar':
            window.close()
            mainpage()
        if event == 'Excluir Compromisso':
            x = values['-TABLE-'][0]
            y = PGSQL.readid()[x]
            PGSQL.excluircompromisso(y)
            window.Element('-TABLE-').Update(Arrayinfo())
            sg.popup("Sucesso")


# ---------------------------------------------------------------------------------------------
inicio()
