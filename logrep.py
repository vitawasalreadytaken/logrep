#!/usr/bin/env python3

import click, sys

import logparser, matcher, output



@click.command()
@click.option('--min-line', default = 0)
@click.option('--max-line', default = float('inf'))
# TODO: time
@click.option('--logger', default = [], multiple = True)
@click.option('--no-logger', default = [], multiple = True)
@click.option('--min-level', default = 'DEBUG')
@click.option('--message', default = [], multiple = True)
@click.option('--no-message', default = [], multiple = True)
@click.argument('filename', default = '-')
def cli(min_line: int, max_line: int, logger: [str], no_logger: [str], min_level: str, message: [str], no_message: [str], filename: str):
	if filename == '-':
		file = sys.stdin
	else:
		file = open(filename, 'r')

	patterns = {
		'logger': mkPatterns(logger, no_logger),
		'level': (matcher.LevelPattern(True, min_level),),
		'message': mkPatterns(message, no_message),
	}
	mtr = matcher.Matcher(patterns)
	print(mtr)

	for i, line in enumerate(file):
		if min_line <= i <= max_line:
			record = logparser.parseLine(line)
			(matches, detail) = mtr.match(record)
			if matches:
				print(i, output.colorize(line.strip(), output.logLevelColor(record['level'])))



def mkPatterns(includes: [str], excludes: [str], cls = matcher.RegExpPattern) -> [matcher.Pattern]:
	return [ cls(True, x) for x in includes ] + [ cls(False, x) for x in excludes ]



if __name__ == '__main__':
	cli()
