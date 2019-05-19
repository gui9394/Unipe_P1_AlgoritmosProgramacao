import sudoku, curses, pickle, os


#Subrotina de interação com o usuario
def interacao (jogo, solucao):					
	janela0 = curses.newwin(14, 28, 0, 0)  #Janela das Regras
	janela1 = curses.newwin(14, 26, 2, 31) #Janela do Tabuleiro
	janela2 = curses.newwin(14, 27, 0, 60) #Janela das Instruções
	janela3 = curses.newwin(1, 12, 0, 38)  #Janela do Titulo

	cursor = 1
	tecla = ''
	d_cursor =''
	teclas = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
	teclas_limpar = ['0', '.']

	sub_interface(janela0, janela1, janela2, janela3)
	
	while True:
		if tecla in ['w', 'W']:
			if (cursor-9) >= 1:
				cursor = cursor-9

		elif tecla in ['s', 'S']:
			if (cursor+9) <= 81:
				cursor = cursor+9

		elif tecla in ['a', 'A']:
			if (cursor-1) >= 1:
				cursor = cursor-1

		elif tecla in ['d', 'D']:
			if (cursor+1) <= 81:
				cursor = cursor+1

		elif tecla in ['n', 'N']:
			janela0.addstr (10, 8, 'Deseja iniciar')
			janela0.addstr (11, 7, 'novo jogo? (S/N)')
			janela0.refresh()
			while True:
				tecla2 = janela0.getkey()
				if tecla2 in ['s', 'S']:
					jogo, solucao = sudoku.inicia_sudoku()
					break
				elif tecla2 in ['n', 'N']:
					break

		elif tecla in teclas:
			sub_alterar (d_cursor, tecla, teclas, jogo)

		elif tecla in teclas_limpar:
			sub_alterar (d_cursor, '.', teclas_limpar, jogo)

		elif tecla in ['x', 'X']:
			if sub_comparacao (jogo, solucao) == True:
				janela0.addstr (10, 4, '!Parabéns você ganhou!')
				janela0.addstr (11, 8, 'Deseja iniciar')
				janela0.addstr (12, 7, 'novo jogo? (S/N)')
				janela0.refresh()
				while True:
					tecla2 = janela1.getkey()
					if tecla2 in ['s', 'S', 'n', 'N']:
						break
				if tecla2 in ['s', 'S']:
					jogo, solucao = sudoku.inicia_sudoku()
					continue
			else:
				janela0.addstr (10, 8, 'Tem algo errado')
				janela0.refresh()
				tecla = janela1.getkey()
				continue

		elif tecla in ['z', 'Z']:
			tecla = sub_salvar_jogo (jogo, solucao, janela0)
			continue

		elif tecla in ['f', 'F']:
			janela0.addstr (10, 3, 'Deseja sair do jogo (S/N)')
			janela0.refresh()
			while True:
				tecla2 = janela0.getkey()
				if tecla2 in ['s', 'S', 'n', 'N']:
					break
			if tecla2 in ['s', 'S']:
					break
		tecla = ''
		d_cursor = sub_tabuleiro(jogo, janela1, cursor)
		for y in range (3):
			for x in range (28):
				janela0.addstr (y + 10, x, ' ')
		janela0.refresh()
		tecla = janela1.getkey()


#Subrotina para altera o digito
def sub_alterar (d_cursor, tecla, teclas, jogo):
	if jogo[d_cursor[0]][d_cursor[1]][d_cursor[2]][d_cursor[3]]['automatico'] == False:
		jogo[d_cursor[0]][d_cursor[1]][d_cursor[2]][d_cursor[3]]['digito'] = tecla


#Subrotina de leitura do jogo salvo
def sub_ler_jogo ():
	try:
		save = open('sudoku.save', 'rb')
		jogo = pickle.load(save)
		solucao = pickle.load(save)
		save.close()
		os.remove('sudoku.save')
	except:
		jogo, solucao = sudoku.inicia_sudoku() #Uso da Biblioteca
	
	return jogo, solucao


#Subrotina para salvar o jogo
def sub_salvar_jogo (jogo, solucao, janela0):
	save = open('sudoku.save', 'wb')
	pickle.dump(jogo, save)
	pickle.dump(solucao, save)
	save.close()

	janela0.addstr (10, 10, 'Jogo salvo')
	janela0.refresh()

	tecla = janela0.getkey()
	return tecla


#Subrotina de verificação
def sub_comparacao (jogo, solucao):
	#lt - linha do tabuleiro
	#ct - coluna do tabuleiro
	#lr - linha da regiao
	#cr - coluna da regiao

	cp = True
	
	for lt in range (3):
		for ct in range (3):
			for lr in range (3):
				for cr in range (3):
					cp = cp and (jogo[lt][ct][lr][cr]['digito'] == solucao[lt][ct][lr][cr]['digito'])  #cp - comparacao
	return cp


#Subrotina da intefarce
def sub_interface (janela0, janela1, janela2, janela3):

	janela0.addstr (2, 1, 'Regras:')
	janela0.addstr (4, 2, 'Preencha a grade de forma')
	janela0.addstr (5, 2, 'que cada coluna, linha e')
	janela0.addstr (6, 2, 'região contenha todos os')
	janela0.addstr (7, 2, 'dígitos de 1 a 9.')
	janela2.addstr (2, 1, 'Comandos:')
	janela2.addstr (4, 3, 'w')
	janela2.addstr (5, 1, 'a   d move o cursor')
	janela2.addstr (6, 3, 's')
	janela2.addstr (7, 2, '1-9  entra com dígito')
	janela2.addstr (8, 2, '0 .  limpa dígito')
	janela2.addstr (9, 3, 'n   novo jogo')
	janela2.addstr (10, 3, 'z   salva o jogo')
	janela2.addstr (11, 3, 'f   fecha o jogo')
	janela2.addstr (12, 3, 'x   resolve')
	janela3.addstr (0, 0, 'SUDOKU-LOKU')
	for y in [0, 4, 8, 12]:
		for x in [0, 8, 16, 24]: 
			janela1.addstr (y, x, '+')
	for y1 in [1, 2, 3, 5, 6, 7, 9, 10, 11]:
		for x1 in [0, 8, 16, 24]:
			janela1.addstr (y1, x1, '|')
	for x2 in [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23]:	
		for y2 in [0, 4, 8, 12]:
			janela1.addstr (y2, x2, '-')
	
	janela0.refresh()	
	janela1.refresh()
	janela2.refresh()
	janela3.refresh()


#Subrotina da posição do cursor
def sub_posicao (y, x):

	posicao = str(int(y)-1)+str(x)
	lista_y = [0, 1, 2, 4, 5, 6, 8, 9, 10]
	lista_x = [2, 4, 6, 10, 12, 14, 18, 20, 22]
	posicao_dic = 1
	dic = {}

	for fy in lista_y:
		for fx in lista_x:
			dic [str(fy)+str(fx)] = posicao_dic
			posicao_dic = posicao_dic + 1

	return dic[posicao]


#Subrotina para exibição do jogo
def sub_tabuleiro (jogo, janela1, cursor):
	#lt - linha do tabuleiro
	#ct - coluna do tabuleiro
	#lr - linha da regiao
	#cr - coluna da regiao

	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_WHITE)

	for lt in range (3):
		for ct in range (3):
			for lr in range (3):
				for cr in range (3):
					a = jogo[lt][ct][lr][cr]['digito']

					y = 1+(cr+(ct*4))
					x = 2+((lr+(lt*4))*2)

					posicao = sub_posicao(y, x)

					if posicao == cursor:
						if (jogo[lt][ct][lr][cr]['automatico'] == False) and (jogo[lt][ct][lr][cr]['digito'] != '.'):
							janela1.addstr(y, x, a, curses.color_pair(3))
						else:
							janela1.addstr(y, x, a, curses.color_pair(1))
						d_cursor = [lt, ct, lr, cr]
					else:
						if (jogo[lt][ct][lr][cr]['automatico'] == False) and (jogo[lt][ct][lr][cr]['digito'] != '.'):
							janela1.addstr(y, x, a, curses.color_pair(2))
						else:
							janela1.addstr(y, x, a,)

					janela1.refresh()

	return d_cursor


if __name__ == "__main__":
	stdscr = curses.initscr()
	curses.start_color()
	stdscr.clear()
	curses.cbreak()
	curses.curs_set(False)
	curses.noecho()

	jogo, solucao = sub_ler_jogo()

	interacao(jogo, solucao)

	curses.endwin()
