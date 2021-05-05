# Trabalho Programação com arquivos
#
# Trabalho (segunda parte)
#
# Luan Freire e Cleber Feijó

import io
import pickle
import os


class Config:
	path = '' #'C:/Users/Luky/Desktop/UFF/Prog Arq/'


def contagem_ocorrencias(p, linhas, lista_todas_palavras, Indice):
	ocorrencias = {'arquivo': Indice['qtdArquivos'], 'qtdOcorrencias': lista_todas_palavras.count(p), 'linhas': [count + 1 for count, i in enumerate(linhas) for j in i.split() if p == j.lower().replace(",", "")]}
	return ocorrencias

def contagem_palavras(nomearq, Indice):
	arq = io.open(Config.path + nomearq + '.txt', mode='r', encoding="utf-8")
	linhas = arq.readlines()
	lista_frase = [' '.join(linhas)]
	frase_processada = lista_frase[0].lower().replace(",", "")
	lista_todas_palavras = frase_processada.split()
	lista_palavras = [*{*lista_todas_palavras}]
	for p in lista_palavras: 
		if p not in [x['letras'] for x in Indice['palavras']]:
			Indice['palavras'].append({'letras': p, 'qtdOcorrencias': 1, 'ocorrencias': [contagem_ocorrencias(p, linhas, lista_todas_palavras, Indice)]})
		else:
			i = [x['letras'] for x in Indice['palavras']].index(p)
			Indice['palavras'][i]['qtdOcorrencias'] += 1
			Indice['palavras'][i]['ocorrencias'].append(contagem_ocorrencias(p, linhas, lista_todas_palavras, Indice))
	Indice['palavras'] = sorted(Indice['palavras'], key=lambda k: k['letras'])
	Indice['iniciais'] = {}
	for count, p in enumerate(Indice['palavras']):
		try:
			if Indice['iniciais'][p['letras'][0]] is not None:
				pass
		except:
			Indice['iniciais'][p['letras'][0]] = count
	arq.close()
	return Indice

def pesquisa_por_indice(Indice, palavra):
	count = 0
	while True:
		letra = ord(palavra[0])-count
		try:
			if letra < 97:
				palavras = Indice['palavras']
			else:
				palavras = Indice['palavras'][Indice['iniciais'][chr(letra)]:]
			aux = set([a['arquivo'] for i in palavras for a in i['ocorrencias'] if i['letras'] == palavra.lower()])
			break
		except:
			count+=1
			pass
	return aux

def main():
	if len(Config.path) == 0:
		raise ValueError("Colocar o caminho dos arquivos no código!")
	Indice = {'qtdArquivos': 0, 'arquivos': [], 'qtdPalavras': 0, 'iniciais': {}, 'palavras': []}
	while True:
		opcao = input(
			f'1) Processar um (novo) arquivo texto;\n2) Salvar o índice atual;\n3) Ler um arquivo de índice;\n4) Realizar Busca usando o Indice atual; \n5) Encerrar o programa.\n')
		if opcao == '1':
			nomearq = input(f'Qual o nome do arquivo de texto?\n')
			if f'{nomearq}.txt' not in Indice['arquivos']:
				Indice['qtdArquivos'] += 1
				Indice['arquivos'].append(f'{nomearq}.txt')
				Indice = contagem_palavras(nomearq, Indice)
				Indice['qtdPalavras'] = len(Indice['palavras'])
			else:
				print(f"\nO arquivo já foi lido!\n")
		if opcao == '2':
			arq = io.open(Config.path + "indice.dat", mode="wb")
			pickle.dump(Indice['qtdArquivos'], arq)
			for i in Indice['arquivos']:
				pickle.dump(len(i.replace('.txt', '')), arq)
				for j in range(len(i.replace('.txt', ''))):
					pickle.dump(i.replace('.txt', '')[j], arq)
			pickle.dump(Indice['qtdPalavras'], arq)
			for k in Indice['palavras']:
				pickle.dump(len(k['letras']), arq)
				for l in range(len(k['letras'])):
					pickle.dump(k['letras'][l], arq)
				pickle.dump(k['qtdOcorrencias'], arq)
				for m in k['ocorrencias']:
					pickle.dump(m['arquivo'], arq)
					pickle.dump(m['qtdOcorrencias'], arq)
					for n in m['linhas']:
						pickle.dump(n, arq)
			arq.close()
		if opcao == '3':
			del Indice
			arq = io.open(Config.path + "indice.dat", mode="rb")
			Indice = {'qtdArquivos': 0, 'arquivos': [], 'qtdPalavras': 0, 'iniciais': {}, 'palavras': []}
			Indice['qtdArquivos'] = pickle.load(arq)
			for i in range(Indice['qtdArquivos']):
				aux = pickle.load(arq)
				palavra = ''
				for j in range(aux):
					palavra += pickle.load(arq)
				Indice['arquivos'].append(f'{palavra}.txt')
			Indice['qtdPalavras'] = pickle.load(arq)
			for k in range(Indice['qtdPalavras']):
				palavras = {}
				aux = pickle.load(arq)
				palavra = ''
				for l in range(aux):
					palavra += pickle.load(arq)
				try:
					if Indice['iniciais'][palavra[0]] is not None:
						pass
				except:
					Indice['iniciais'][palavra[0]] = k
				palavras['letras'] = palavra
				palavras['qtdOcorrencias'] = pickle.load(arq)
				lista_ocorrencias = []
				for m in range(palavras['qtdOcorrencias']):
					ocorrencias = {}
					ocorrencias['arquivo'] = pickle.load(arq)
					ocorrencias['qtdOcorrencias'] = pickle.load(arq)
					ocorrencias['linhas'] = [pickle.load(arq) for n in range(ocorrencias['qtdOcorrencias'])]
					lista_ocorrencias.append(ocorrencias)
				palavras['ocorrencias'] = lista_ocorrencias
				Indice['palavras'].append(palavras)
		if opcao == '4':
			busca = input(f'Selecione o tipo de Busca:\n1) Simples;\n2) Compostas.\n')
			if busca == '1':
				palavra = input('Digite uma única palavra: ')
				count = 0
				while True:
					letra = ord(palavra[0])-count
					try:
						if letra < 97:
							palavras = Indice['palavras']
							aux = [i['ocorrencias'] for i in palavras if i['letras'] == palavra.lower()]
							break
						else:
							palavras = Indice['palavras'][Indice['iniciais'][chr(letra)]:]
						aux = [i['ocorrencias'] for i in palavras if i['letras'] == palavra.lower()][0]
						break
					except:
						count+=1
						pass
				if len(aux) == 0:
					print('Palavra não encontrada')
				else:
					print(f'A palavra {palavra} foi encontrada: ')
					for i in aux:
						print(f'\n{i["qtdOcorrencias"]} vezes no arquivo {Indice["arquivos"][i["arquivo"]-1]}, nas linhas {", ".join(map(str, i["linhas"]))} ')
				os.system("pause")
			if busca == '2':
				opcao = input(f'1)Buscar com E;\n2)Buscar com OU.\n')
				palavra = input('Digite a primeira palavra: ')
				aux = pesquisa_por_indice(Indice, palavra)
				palavra2 = input('Digite a segunda palavra: ')
				aux2 = pesquisa_por_indice(Indice, palavra2)
				if len(aux) == 0:
					print(f'A palavra {palavra} é inválida!')
				elif len(aux2) == 0:
					print(f'A palavra {palavra} é inválida!')
				else:
					if opcao == '1':
						aux3 = list(aux & aux2)
						if len(aux3) == 0:
							print('As palavras não aparecem juntas em nenhum arquivo!')
						else:
							print(f'As palavras aparecem juntas no(s) arquivo(s) {", ".join(map(str, aux3))}.')
					if opcao == '2':
						aux3 = list(aux | aux2)
						if len(aux3) == 0:
							print('As palavras não aparecem em nenhum arquivo!')
						else:
							print(f'As palavras aparecem no(s) arquivo(s) {", ".join(map(str, aux3))}.')
				os.system("pause")
		if opcao == '5':
			break
		print(Indice)

if __name__ == "__main__":
	main()

