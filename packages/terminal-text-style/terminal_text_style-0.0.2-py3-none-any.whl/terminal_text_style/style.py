'''
O código para mudar cores padrão é \033...\033[m
Estilo de fonte: 0(none); 1(bold); 4(underline); 7(negative/troca cor de fundo com a fonte)
texto: 30(branco) 31(vermelho); 32(verde); 33(amarelo); 34(azul); 35(roxo); 36(anil); 37(cinza)
fundo: 40(branco) 41(vermelho); 42(verde); 43(amarelo); 44(azul); 45(roxo); 46(anil); 47(cinza)

nome = 'Victor'
print(f'Hello, \033[4;33;44m{nome}\033[m!!!')
'''

def color_text(type=0, text=0, back=0, message=0):
    """
color_text(type=0, text=0, back=0, message=0)

Apply ANSI style, color, and background to terminal text.

Parameters:
- type (str): 'bold', 'italic', 'underline', 'negative', 'strike' or 0 (no style)
- text (str): text color ('red', 'green', etc.) or 0
- back (str): background color ('yellow', 'blue', etc.) or 0
- message (str): the message to be styled

Example:
print(color_text(type='bold', text='white', back='red', message='Alert!'))
"""
    styl = {0:0, 'bold' : 1, 'italic' : 3, 'underline' : 4, 'negative': 7, 'strike':9}
    txt = {'black' : 30, 'red' : 31, 'green' : 32, 'yellow' : 33, 'blue' : 34,
    'magenta' : 35, 'cyan' : 36, 'white' : 37}
    background = {'black' : 40, 'red' : 41, 'green' : 42, 'yellow' : 43, 'blue' : 44,
    'magenta' : 45, 'cyan' : 46, 'white' : 47}

    if type== 0 and 0 not in [back, text, message]:
        return f'\033[{txt[text]};{background[back]}m{message}\033[m'
    elif text==0 and 0 not in [back, type, message]:
        return f'\033[{styl[type]};{background[back]}m{message}\033[m'
    elif back== 0 and 0 not in [type, text, message]:
        return f'\033[{styl[type]};{txt[text]}m{message}\033[m'
    elif type== 0 and text==0:
        return f'\033[{background[back]}m{message}\033[m'
    elif type== 0 and back== 0:
        return f'\033[{txt[text]}m{message}\033[m'
    elif text== 0 and back== 0:
        return f'\033[{styl[type]}m{message}\033[m'
    elif text== 0 and back== 0:
        return f'\033[{styl[type]}m{message}\033[m'
    else:
        return f'\033[{styl[type]};{txt[text]};{background[back]}m{message}\033[m'

if __name__ == '__main__':
    print(color_text(type='bold', message='Abacaxi com goiaba'))
    print(color_text(text='red', message='Abacaxi com goiaba'))
    print(color_text(back='yellow', message='Abacaxi com goiaba'))
    print(color_text(type='strike', back='green', message='Abacaxi com goiaba'))
    print(color_text(type='bold', text='yellow', message='Abacaxi com goiaba'))
    print(color_text(back='red', text='white', message='Abacaxi com goiaba'))
    print(color_text(text='magenta', type='bold', back='black', message='Abacaxi com goiaba'))

    print('------------------------------------')
    print(f'\033[9;37;40mOlá mundo\033[m')
