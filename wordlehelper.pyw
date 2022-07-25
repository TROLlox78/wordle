import PySimpleGUI as sg
import collections

def make_list():
    file = open('wordlelist.txt', 'r')
    org_list = []
    for z in range(0, 2315):
        org_list.append(file.readline()[:-1])
    file.close()
    return org_list


# filter out words with invalid letters:
def banning(banned, list):
    for letter in banned:
        templist = []
        for case in list:
            if letter in case:
                templist.append(case)

        for word in templist:
            list.remove(word)


def yellowthining(yellow, list):
    for index, letter in yellow.items():
        # print(index,letter)
        templist = []
        if letter != '':
            # print(f'    testing {letter} at index: {index}')
            for case in list:
                # print(case)
                if letter not in case:
                    # print(f'letter {letter} doesnt appear in {case}(remove case)')
                    templist.append(case)
                if letter == case[index]:
                    # print(f'letter {letter} is in {case} in the wrong spot(remove case)')
                    templist.append(case)
        for item in templist:
            list.remove(item)


def greencheck(greendic, list):
    for index, letter in greendic.items():
        templist = []
        if letter != '':
            for case in list:
                if letter not in case[index]:
                    templist.append(case)

            for item in templist:
                list.remove(item)


def bestuse(list):
    templist = []
    for word in list:
        dic = {}
        for letter in word:
            dic.update({letter: word.count(letter)})
        if len(dic) == len(word):
            templist.append(word)
    if len(list) > 110:
        return templist
    else:
        return list


def main():
    list = make_list()

    def gobuttonlogic(list):
        word = values['-KEYINPUT-']
        graylist = []
        yellowsnow = {}
        greendick = {}
        yellowlist = [f'-YELLOW1-', f'-YELLOW2-', f'-YELLOW3-', f'-YELLOW4-',
                      f'-YELLOW5-']
        greenlist = [f'-GREEN1-', f'-GREEN2-', f'-GREEN3-', f'-GREEN4-', f'-GREEN5-']
        counted_words = collections.Counter(word)
        for idx, green in enumerate(greenlist):
            if values[green]:
                greendick[idx] = word[idx]
            elif values[yellowlist[idx]]:
                # print(values[yellowlist[idx]])
                yellowsnow[idx] = word[idx]
            else:
                if counted_words[word[idx]]==1:
                    graylist.append(word[idx])
        if graylist:
            banning(graylist, list)
        if yellowsnow:
            yellowthining(yellowsnow, list)
        if greendick:
            greencheck(greendick, list)
        # print(graylist,yellowsnow,greendick)
        output = bestuse(list)
        print(output)

    def set():
        for idx, item in enumerate([f'-11-', f'-12-', f'-13-', f'-14-', f'-15-']):
            window[item].update(f' {values["-KEYINPUT-"][idx]} ')

    #     THEME
    sg.theme('DarkGrey')
    turn = 0
    column1 = [
        [sg.Checkbox('', key='-GREEN1-')], [sg.Checkbox('', key='-YELLOW1-')], [sg.Button(f' X ', key='-11-')]
    ]
    column2 = [
        [sg.Checkbox('', key='-GREEN2-')], [sg.Checkbox('', key='-YELLOW2-')], [sg.Button(f' X ', key='-12-')]
    ]
    column3 = [
        [sg.Checkbox('', key='-GREEN3-')], [sg.Checkbox('', key='-YELLOW3-')], [sg.Button(f' X ', key='-13-')]
    ]
    column4 = [
        [sg.Checkbox('', key='-GREEN4-')], [sg.Checkbox('', key='-YELLOW4-')], [sg.Button(f' X ', key='-14-')]
    ]
    column5 = [
        [sg.Checkbox('', key='-GREEN5-')], [sg.Checkbox('', key='-YELLOW5-')], [sg.Button(f' X ', key='-15-')]
    ]
    column6 = [
        [sg.Text('Green', text_color='Green')], [sg.Text('Yellow', text_color='Yellow')],
        [sg.Button('GO', key='-GO1-'), sg.Button('RESET', key='-CLEAR1-')]]
    layout = [
        [sg.Text('Wordle Helper!', key='-WARN-', expand_x=True), sg.Text(f'Turn:{turn}', key='-TURNS-')],
        [sg.Input(key='-KEYINPUT-', s=40), sg.Button('SET', key='-SET-')],
        [sg.Col(column1), sg.Col(column2), sg.Col(column3), sg.Col(column4), sg.Col(column5),
         sg.Col(column6)],
        [sg.Output(s=(42, 20), key='-OUT-')]
    ]
    window = sg.Window('WTC', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        match event:
            case '-GO1-':
                if turn == 4:
                    window['WARN'].update('Remember to hit reset after a game!')
                elif len(values['-KEYINPUT-']) == 5:
                    print('hallo')
                    window['-WARN-'].update('Wordle Helper!')
                    window['-OUT-'].update('')
                    set()
                    gobuttonlogic(list)
                    turn += 1
                    window['-TURNS-'].update(f'Turn:{turn}')
                    window['-KEYINPUT-'].update('')
                    window.refresh()

            case '-CLEAR1-':
                turn = 0
                window['-WARN-'].update('Wordle Helper!')
                window['-TURNS-'].update(f'Turn:{turn}')
                for item in [f'-11-', f'-12-', f'-13-', f'-14-', f'-15-']:
                    window[item].update(f' X ')
                window['-KEYINPUT-'].update('')
                window['-OUT-'].update('')
                window.refresh()
                list = make_list()
            case '-SET-':
                if len(values['-KEYINPUT-']) == 5:
                    set()
                else:

                    window['-WARN-'].update('Normal Wordle uses 5 letter words!')
                    window['-KEYINPUT-'].update('')
    window.close()


def test():
    list = make_list()
    banned = []

    yellow = {0: '', 1: '', 2: '', 3: 'h', 4: 't', }

    greendic = {0: '', 1: '', 2: '', 3: '', 4: ''}

    banning(banned, list)
    yellowthining(yellow, list)
    greencheck(greendic, list)

    # print('all words:',list)
    print(bestuse(list))


if __name__ == '__main__':
    main()
