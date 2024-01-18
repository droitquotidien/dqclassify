import csv
import sys

def main():
	if len(sys.argv) > 2:
		line_size = int(sys.argv[2])
	else:
		line_size = 6

	with open(sys.argv[1], newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter='|')
		try:
			for i, row in enumerate(spamreader):
				l = len(row)
				if l != line_size:
					print(row, file=sys.stderr)
					raise ValueError(f"Bad line size (expected={line_size}, found={l}")
				content = row[-1]
				assert '|' not in content, content
		except:
			print(i+1)
			print(row)
			raise


if __name__ == '__main__':
	sys.exit(main())
