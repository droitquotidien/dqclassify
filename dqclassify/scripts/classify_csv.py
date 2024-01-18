import argparse
import nis
import sys
import csv
from collections import Counter
from pprint import pformat

from dqclassify.classifyparagraph import ParagraphKind, ModifyingParagraph, Paragraph
from dqclassify.categories import ModifierCategory


def parse_args(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('incsv', help="CSV file with JORF content")
	return parser.parse_args(argv[1:]), parser


class CsvContext(object):

	def __init__(self):
		self.line = 0
		self.textid = None
		self.childid = None
		self.kind = None
		self.num = None
		self.rank = None

	def __repr__(self):
		return (f"{self.line}:{self.textid}:{self.childid or ''}"
				f":{self.kind or ''}:{self.num or ''}:{self.rank or ''}")


def set_between_alineas(paragraphs, catstats:Counter|None=None):
	categories = []
	for p in paragraphs:
		if not isinstance(p, ModifyingParagraph):
			continue
		cat = p.category
		lcat = categories[-1] if categories else None
		if lcat in (ModifierCategory.OPEN_ALINEA,
				ModifierCategory.OPEN_ALINEA_WITH_ARTICLE,
				ModifierCategory.OPEN_ALINEA_WITH_SECTION,
				ModifierCategory.BETWEEN_ALINEA):
			if cat == ModifierCategory.NOT_MODIFYING:
				if categories:
					catstats[ModifierCategory.NOT_MODIFYING] -= 1
					catstats[ModifierCategory.BETWEEN_ALINEA] += 1
				cat = ModifierCategory.BETWEEN_ALINEA
				p.category = cat
		categories.append(cat)


class TextCSV(object):

	def __init__(self, textid, category, uri, separator='|'):
		self.textid = textid
		self.category = category
		self.uri = uri
		self.versions = list()
		self.separator = separator
		assert self.separator not in uri
	def __repr__(self):
		line = [
			self.textid, '', '0', '', '0', str(self.category.value), self.uri
		]
		return self.separator.join(line)

	def to_csv(self):
		lines = []
		lines.append(str(self))
		for v in self.versions:
			lines.append(v.to_csv())
		return '\n'.join(lines)


class TextVersionCSV(object):

	def __init__(self, textid, textversionid, category, title, separator='|'):
		self.textid = textid
		self.textversionid = textversionid
		self.category = category
		self.title = title
		self.separator = separator
		self.articles = list()
		assert separator not in title

	def __repr__(self):
		line = [
			self.textid, self.textversionid, '0', '', '0', str(self.category.value), self.title
		]
		return self.separator.join(line)

	def to_csv(self):
		lines = []
		lines.append(str(self))
		for a in self.articles:
			lines.append(a.to_csv())
		return '\n'.join(lines)


class ArticleCSV(object):
	"""Génération d'un article sous la forme d'un CSV.

	Chaque ligne du CSV a la forme suivante, où chaque colonne est séparée par '|':

	- Identificateur du texte `JORFTEXTxxx` (str)
	- Idenfiticateur de l'article `JORFARTIxxx` (str)
	- Type de paragraphe: 1=ALINEA 2=TABLE 3=RAW (int)
	- Numéro de l'article (str ou vide)
	- Rang du paragraphe, démarrant à 1 (int)
	- Classification du paragraphe modificateur (categories.ModifierCategory.value (int) ou vide)
	- Contenu (str)
	"""

	def __init__(self, textid, artid, num, separator='|'):
		self.textid = textid
		self.artid = artid
		self.num = num
		self.paragraphs = list()
		self.separator = separator

	def to_csv(self):
		lines = []
		for p in self.paragraphs:
			if p.kind == ParagraphKind.P_ALINEA:
				assert isinstance(p, ModifyingParagraph)
				line = [
					self.textid, self.artid, str(p.kind.value), self.num,
					str(p.rank), str(p.category.value), p.content
				]
			elif p.kind in (ParagraphKind.P_TABLE, ParagraphKind.P_RAW):
				assert isinstance(p, Paragraph)
				line = [
					self.textid, self.artid, str(p.kind.value), self.num,
					str(p.rank), '', p.content
				]
			else:
				raise ValueError(f"Bad paragraph type: {p.kind}")
			lines.append(self.separator.join(line))
		return '\n'.join(lines)


def main():
	args, argparser = parse_args(sys.argv)
	filename = args.incsv
	categories = Counter()
	anomalies = Counter()
	for c in ModifierCategory:
		categories[c] = 0
	with open(filename, 'r') as f:
		jorfreader = csv.reader(f, delimiter='|')
		context = CsvContext()
		text = None
		vers = None
		art = None
		for i, row in enumerate(jorfreader):
			context.line = i
			context.textid = row[0]
			context.childid = row[1]
			context.kind = int(row[2])
			context.num = row[3]
			context.rank = int(row[4])
			content = row[-1]
			if context.childid.startswith('JORFARTI'):  # C'est un article
				assert text is not None
				assert vers is not None
				assert text.textid == context.textid
				if art is None:
					art = ArticleCSV(context.textid, context.childid, context.num)
				else:
					if art.artid != context.childid:
						# C'est un nouvel article
						# Finalise l'article courant
						set_between_alineas(art.paragraphs, categories)
						# Création d'un nouvel article
						art = ArticleCSV(context.textid, context.childid, context.num)
						vers.articles.append(art)
				kind = ParagraphKind(context.kind)
				if kind == ParagraphKind.P_ALINEA:
					# On ne classifie que les vrais paragraphes
					mod_paragraph = ModifyingParagraph.from_kind_and_content(kind, content,
						context.rank, context=context)
					categories[mod_paragraph.category] += 1
					if mod_paragraph.anomaly_msg is not None:
						anomalies[mod_paragraph.anomaly_msg.to_tuple()] += 1
					art.paragraphs.append(mod_paragraph)
					if mod_paragraph.category != ModifierCategory.NOT_MODIFYING:
						vers.category = ModifierCategory.MODIFYING
						text.category = ModifierCategory.MODIFYING
				else:
					# Tableaux et autres
					art.paragraphs.append(Paragraph(kind, content, context.rank))
			elif not context.childid:  # C'est un nouveau texte
				if text is not None:
					print(text.to_csv())
				text = TextCSV(context.textid, ModifierCategory.NOT_MODIFYING, content)
			elif context.childid.startswith('JORFVERS'):  # C'est une nouvelle version
				assert text is not None
				assert text.textid == context.textid
				vers = TextVersionCSV(context.textid, context.childid,
					ModifierCategory.NOT_MODIFYING, content)
				text.versions.append(vers)
	if text is not None:
		# Cas particulier du dernier texte
		print(text.to_csv())
	print(pformat(categories), file=sys.stderr)
	print(pformat(anomalies), file=sys.stderr)
	return 0


if __name__ == '__main__':
	sys.exit(main())
