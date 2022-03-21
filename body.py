import PySimpleGUI as sg
import datetime
import PGSQL
import time
import threading
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import timedelta, date

#função que atualiza a data para os compromissos que se repetem
def novadata():
    NEWDATE = datetime.datetime.now() + timedelta(days=7)
    NEWDATE = NEWDATE.strftime("%Y-%m-%d %H:%M")
    DATENOW = datetime.datetime.now()
    DATENOW = DATENOW.strftime("%Y-%m-%d %H:%M")
    PGSQL.write_newdate(NEWDATE,DATENOW)




#função mensagem, nela um popup de um png aparece informando que o horário do compromisso chegou
def popupmsg(msg):
    root = tk.Tk()
    root.geometry("1920x1080")
    root.title("Seu compromisso chegou!!")
    bg = PhotoImage(master = root, file = "meme2.png")
    label1 = tk.Label(root, text=f'Está no horário:  {msg}', font=('*Font', '50'))
    label = tk.Label(root, image=bg)
    label.place(x=0, y=0, relwidth=1, relheight=1)
    label.pack(side="top", fill="x", pady=10, padx=10)
    label1.place(x=0, y=0, relwidth=1, relheight=1)
    label1.pack(side="top", fill="x", pady=10, padx=10)
    
    B1 = tk.Button(root, text="Okay", command = root.destroy, width=80)
    B1.pack()
    root.mainloop()



    
#função que compara o horário atual com o do compromisso no banco de dados 
def verificaz():
    while True:
        for x in range(len(PGSQL.lista_datas())):
            data = PGSQL.lista_datas()[x]
            if data == datetime.datetime.now().strftime("%Y-%m-%d %H:%M"):
                y = PGSQL.readid()[x]
                msg = PGSQL.readname()[x]
                popupmsg(msg)
                if PGSQL.read_repet()[x] == False:
                    PGSQL.excluircompromisso(y)

                else:
                    novadata()

        time.sleep(3)
                    
                


#processamento paralelo responsável por executar a função em conjunto com o código fonte 
threading.Thread(target=verificaz).start()

# função:inicio(tela inical)
# ---------------------------------------------------------------------------------------------
def inicio():
    sg.theme('Reddit')
    layout = [
        [sg.Text('Agenda de Lembretes')],
        [sg.Button('Creditos'), sg.Button('Entrar')]
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


# função créditos(dedicatórias e integrantes do grupo)
# ---------------------------------------------------------------------------------------------
def creditos():
    layout = [
        [sg.Text('Projeto de Computação 2')],
        [sg.Text('Feito por Rafael e João Victor')],
        [sg.Text('Professor Jonathan Nogueira')],
        [sg.Button('Voltar')]
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

#mainpage, onde o usuário informa os dados de seu compromisso
def mainpage():

    [sg.theme('Reddit')]
    layout = [[sg.Text('Informe o nome do compromisso, horário, data, e humor')],
              [sg.Text('Nome do compromisso', size=(10, 2)),
               sg.InputText(key='-NAME-')],
              [sg.Text('Horário', size=(10, 2)), sg.Slider(
                  (0, 23), orientation='h', s=(20, 10), k='-Horas-')],
              [sg.Text('Minutos', size=(10, 2)), sg.Slider(
                  (0, 59), orientation='h', s=(20, 10), k='-Minutos-')],
              [sg.Text('Informe a data', size=(10, 2)), sg.Input(key='-DATE-', size=(10, 2)), sg.CalendarButton(
                  'Data',  target='-DATE-', format='%d/%m/%Y', default_date_m_d_y=(1, None, 2022), )],
                  [sg.Text('Esse compromisso se repete?'), sg.Checkbox('', default=False,  key = '-REPET-')],
              [sg.Text('Diga como se sente em relação ao evento', size=(10, 5)), sg.OptionMenu(
                  ['Gosto bastante', 'É OK', 'Odeio com todas as forças'], s=(30, 2))],
              [sg.Button('Submit'), sg.Button('Show Table'), sg.Button('Voltar'), ]]

    window = sg.Window('Assitente de rotina', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Voltar':
            window.close()
            inicio()
        elif event == 'Submit':
            # convertendo int de hora e minutos para datime(para se adequar ao formato da lib time)
            # ---------------------------------------------------------------------------------------------
            NAME = values['-NAME-'].capitalize()
            DATE = values['-DATE-'].capitalize()
            REPET = values['-REPET-']
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
                tempo.strftime("%Y-%m-%d %H:%M")
                NAME = (values['-NAME-'])
                DATE = tempo
                REPET = (values['-REPET-'])
                print(REPET)
                PGSQL.write(NAME, DATE, REPET)

                sg.popup("Sucesso")


# ---------------------------------------------------------------------------------------------
        elif event == 'Show Table':
            NAME = PGSQL.readname()
            DATE = PGSQL.readDate()
            if NAME:
                window.close()
                Table()
            else:
                sg.popup("Não existe pessoas cadastradas")



#função que monta um array com informações do nome e data do compromisso
def Arrayinfo():
    Compromisso_array = []
    for x in range(len(PGSQL.readname())):
        Compromisso = [PGSQL.readname()[x], PGSQL.readDate()[x]]
        Compromisso_array.append(Compromisso)
    return Compromisso_array


# ---------------------------------------------------------------------------------------------

#Table, onde o usuário pode ver seus compromissos 
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
         [sg.Button('Voltar'),
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


#iniciando o programa
inicio()





