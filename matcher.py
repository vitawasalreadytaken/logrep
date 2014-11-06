import re

import logparser



class Match:

	def __init__(self, text: str):
		self.text = text


	def __repr__(self):
		return self.text


	__str__ = __repr__


class Pattern:

	def __init__(self, positive: bool, pattern: str):
		self.positive = positive
		self.pattern = pattern

	def __repr__(self):
		return '{}{}'.format('✓' if self.positive else '✗', self.pattern)

	def match(self, value: str) -> Match:
		raise NotImplementedError()



class RegExpPattern(Pattern):
	def match(self, value: str) -> Match:
		m = re.search(self.pattern, value)
		if m:
			return Match(m.group(0))


class LevelPattern(Pattern):
	def match(self, value: str) -> Match:
		if value >= logparser.levelNameToInt(self.pattern):
			return Match(value)




class Matcher:

	def __init__(self, patterns: dict):
		self.patterns = patterns


	def __repr__(self):
		return '\n'.join((field + ':').ljust(12) + '  '.join(map(repr, pats)) for field, pats in sorted(self.patterns.items()))


	def match(self, record: dict) -> (bool, [str, Match]):
		#matches = {}
		for field, patterns in self.patterns.items():
			val = record.get(field, '')
			for pattern in patterns:
				match = pattern.match(val)

				if pattern.positive and match:
					# Positive pattern found => record the match (TODO).
					# matches[field].append(...)
					pass
				elif pattern.positive and not match:
					# Positive pattern not found => automatic fail.
					return (False, None)
				elif not pattern.positive and match:
					# Negative pattern found => automatic fail.
					return (False, None)
				elif not pattern.positive and not match:
					# Negative pattern not found => no action.
					pass

		return (True, None)
