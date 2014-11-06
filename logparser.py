#!/usr/bin/env python3
import re, sys, logging, toolz, datetime



# [%(asctime)s][%(process)d][%(name)s][%(levelname)s] %(message)s
DEFAULT_LINE_PATTERN = re.compile('^\[(?P<time>.*?)\]\[(?P<process>.*?)\]\[(?P<logger>.*?)\]\[(?P<level>.*?)\] (?P<message>.*?)$')


def parseLine(line, pattern = DEFAULT_LINE_PATTERN) -> dict:
	m = re.match(pattern, line.strip())
	return parseFields(m.groupdict()) if m else {'raw': line}


def parseFields(fields: dict) -> dict:
	'''
	Convert some string fields to native representation (datetime, int, ...).
	'''
	return toolz.merge(fields, {
		'level': levelNameToInt(fields['level']),
		'time': datetime.datetime.strptime(fields['time'], '%Y-%m-%d %H:%M:%S,%f'),
	})


def levelNameToInt(lvl: str) -> int:
	return getattr(logging, lvl.upper())


def parse(text: str, pattern = DEFAULT_LINE_PATTERN) -> iter([dict]):
	for line in text.split('\n'):
		if line:
			yield parseLine(line, pattern)


def parseFile(path: str) -> (dict, [dict]):
	with open(path) as f:
		lines = list(parse(f.read()))
	stats = {
		'levels': toolz.recipes.countby(lambda line: line.get('level'), lines)
	}
	return (stats, lines)




if __name__ == '__main__':
	(stats, lines) = parseFile(sys.argv[1])
	print(lines)
