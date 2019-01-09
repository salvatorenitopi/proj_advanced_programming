'''
- Cerca in un file di testo una keyword che abbia determinate caratteristiche (es. Doppia, lenght, maiuscola)
- Contare quante volte la parola figura nel file


f = build_matching (array_parole)	# dove f -> lamda

count (array_parole, f())
'''

import re

def read (filename):
	f = open(filename,"r")
	d = f.read()
	a = []
	for w in d.split():
		a.append(re.sub(r'[^A-Za-z]', '', w))
	return a

#########################PARTE FUNZIONALE#######################

class Functional:

	def __init__(self):
		pass

	def double (self, w):
		if len(w) > 2:
			if w[0] == w[1]:
				return True
			return self.double(w[1:])
		return False


	def match (self, s):
		if ((len(s) < 6) and (s.istitle() == True) and (self.double(s) == True) and (s[-1:] == "o")):
			return True
		else:
			return False

	# Caratteristiche scelte:
	# - La parola deve iniziare con la lettera maiuscola
	# - La parola deve terminare con la lettera "o"
	# - La parola deve avere una lunghezza inferiore a 6 caratteri
	# - La parola deve avere una doppia
	# Verranno contate il numero di volte che figura la prima keyword incontrata

	build_matching = lambda self, a: filter (self.match, a)

	def count(self, a, fx):
		if len(list(set(fx(a)))) > 1:
			if fx(a)[-1] == fx(a)[0]:
				# Switch
				return self.count ([a[0]] + [a[-1]] + list(a[1:-1]), fx)
			else:
				# Pop
				return self.count (list(a[:-1]), fx)
		else:
			return len(fx(a))

#########################PARTE FUNZIONALE#######################

'''
a1 = read ("lyrics_originale.txt")
a2 = read ("lyrics_artificiale1.txt")
a3 = read ("lyrics_artificiale2.txt")

f = Functional ()

print "Occorrenze della Keyword nel file originale: " + str(f.count(a1, f.build_matching))
print "Occorrenze della Keyword nel file artificiale: " + str(f.count(a2, f.build_matching))
print "Occorrenze della Keyword nel file artificiale: " + str(f.count(a3, f.build_matching))
'''