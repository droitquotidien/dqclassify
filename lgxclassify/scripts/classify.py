import argparse
import sys
import csv
from collections import Counter
from pprint import pprint

from lgxclassify.classifyparagraph import ParagraphKind, ModifyingParagraph, Paragraph
from lgxclassify.categories import ModifierCategory

"""
out = []
out.append(text.id)
out.append('')
out.append('0')
out.append('')
out.append('0')
out.append('fr/lr/' + uri.uri + '/' + str(text.date_publi))
of.write('|'.join(out))
of.write('\n')

out = []
out.append(text.id)
out.append(vers.id)
out.append('0')
out.append('')
out.append('0')
titre = normalize_field_content(text.id, vers.id, 'titrefull', vers.titrefull)
out.append(titre)
of.write('|'.join(out))
of.write('\n')
"""

def parse_args(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('--from-csv', help="CSV file with JORF content")
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
		return f"{self.line}:{self.textid}:{self.childid or ''}:{self.kind or ''}:{self.num or ''}:{self.rank or ''}"


def set_between_alineas(paragraphs):
	"""
	categories = []
	for np in paragraphs:
		# TEST is np is a ModifyingParagraph else continue
		cat = np.get('cat')
		lcat = categories[-1] if categories else None
		if lcat in (AlineaModifierCategory.OPEN_ALINEA,
                    AlineaModifierCategory.ALINEA_OPEN_ALINEA_WITH_ARTICLE,
                    AlineaModifierCategory.ALINEA_OPEN_ALINEA_WITH_SECTION,
                    AlineaModifierCategory.ALINEA_BETWEEN_ALINEA):
            if cat == AlineaModifierCategory.NOT_A_MODIFIER:
                cat = AlineaModifierCategory.ALINEA_BETWEEN_ALINEA
                np['cat'] = cat
        categories.append(cat)
	"""
	pass


def main():
	args, argparser = parse_args(sys.argv)
	if args.from_csv:
		categories = Counter()
		anomalies = Counter()
		for c in ModifierCategory:
			categories[c] = 0
		with open(args.from_csv, 'r') as f:
			jorfreader = csv.reader(f, delimiter='|')
			context = CsvContext()
			artid = None  # Article courant
			art_paragraphs = list()  # Paragraphes de l'article courant
			for i, row in enumerate(jorfreader):
				context.line = i
				context.textid = row[0]
				context.childid = row[1]
				context.kind = int(row[2])
				context.num = row[3]
				context.rank = int(row[4])
				content = row[-1]
				#print(f"{textid} {childid} {resource_kind} {resource_num} {resource_rank} {content}")
				if context.childid.startswith('JORFARTI'):  # C'est un article
					if artid is None:
						artid = context.childid
						assert art_paragraphs is None
					else:
						if artid != context.childid:
							# Nouvel article
							# TODO: set_between_alineas(art_paragraphs)
							# TODO: flush to CSV art_paragraphs
							art_paragraphs = list()
							artid = context.childid
					kind = ParagraphKind(context.kind)
					if kind == ParagraphKind.P_ALINEA:  # On ne classifie pas les tableaux ou autres
						mod_paragraph = ModifyingParagraph.from_kind_and_content(kind, content, context=context)
						categories[mod_paragraph.category] += 1
						if mod_paragraph.anomaly_msg is not None:
							anomalies[mod_paragraph.anomaly_msg.to_tuple()] += 1
						art_paragraphs.append(mod_paragraph)
					else:
						art_paragraphs.append(Paragraph(kind, content))
				else:
					# TODO: flush to CSV text or vers
					pass
		pprint(categories)
		pprint(anomalies)
	return 0


if __name__ == '__main__':
	sys.exit(main())