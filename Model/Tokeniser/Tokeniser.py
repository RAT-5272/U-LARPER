import unicodedata
from collections import defaultdict
import heapq
import time
import json


SPACE_PLACEHOLDER = "ᚐ"

SPECIAL_TOKENS: list[str] = [
	"[Ꝟ Header Ꝟ]",
	"[Ꝟ ConversationID Ꝟ]",
	"[Ꝟ Timestamp Ꝟ]",
	"[Ꝟ LatestTimestamp Ꝟ]",
	"[Ꝟ HeaderEnd Ꝟ]",

	"[Ꝟ ResponseID Ꝟ]",
	"[Ꝟ ParentResponseID Ꝟ]",
	"[Ꝟ Sender Ꝟ]",
	"[Ꝟ Channel Ꝟ]",
	"[Ꝟ StartMessage Ꝟ]",
	"[Ꝟ EndMessage Ꝟ]",
	"[Ꝟ EndTurn Ꝟ]",

	"[Ꝟ ToolCall Ꝟ]",


	"[Ꝟ Mask Ꝟ]",
]

PREMADE_TOKENS: list[str] = []

# Every digit from 0-999
for i in range(1000):
	PREMADE_TOKENS.append(str(i))

WHITESPACE_GROUPS = {
	" ": [4, 2, 1],
	"	": [1]
}

class Tokeniser:
	def __init__(self, **kwargs: str | int):
		if kwargs:
			self.Train(str(kwargs["text"]), int(kwargs["targetCount"]))
		pass

	def Train(self, text: str, targetCount: int):
		groups: list[str] = []
		groups.extend(self._PreProcess(text))

		# Populate the starting tokens with every character found in the training data
		tokenIndex = 0
		tokenToID: dict[str, int] = dict()
		IDtoToken: dict[int, str] = dict()
		EXTRA_TOKENS: list[str] = []
		EXTRA_TOKENS.extend(SPECIAL_TOKENS)
		EXTRA_TOKENS.extend(PREMADE_TOKENS)
		for token in EXTRA_TOKENS:
			if tokenToID.get(token) is None:
				tokenIndex += 1
				tokenToID[token] = tokenIndex
				IDtoToken[tokenIndex] = token

		for group in groups:
			for char in group:
				if tokenToID.get(char) is None:
					tokenIndex += 1
					tokenToID[char] = tokenIndex
					IDtoToken[tokenIndex] = char

		# Tokenise the whole list with the special, additional, and base tokens.
		tokenisedGroups: list[list[int]] = []
		for group in groups:
			result: list[int] = []
			i = 0
			while i < len(group):
				best = None
				# Try every possible length
				for j in range(i + 1, len(group) + 1):
					token = group[i:j]
					if token in tokenToID:
						best = token

				if best is None:
					raise RuntimeError(f"No token for {group[i]!r}")

				result.append(tokenToID[best])
				i += len(best)

			tokenisedGroups.append(result)

		startTime: float = time.time()

		# Pair to number of counts
		pairCounts: dict[tuple[int, int], int] = defaultdict(int)

		# Pair to locations where it occurs
		# (document index, token index)
		pairLocations: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)

		# Build initial pair database
		for docID, group in enumerate(tokenisedGroups):
			for i in range(len(group) - 1):
				pair = (group[i], group[i + 1])

				pairCounts[pair] += 1
				pairLocations[pair].add((docID, i))

		# Max heap
		heap: list[tuple[int, int, int]] = []
		for pair, count in pairCounts.items():
			heapq.heappush(
				heap,
				(-count, pair[0], pair[1])
			)

		def AddPair(pair: tuple[int, int], docID: int, pos: int):
			if pair[0] == pair[1] and False:
				pass
			pairCounts[pair] += 1
			pairLocations[pair].add((docID, pos))
			heapq.heappush(
				heap,
				(-pairCounts[pair], pair[0], pair[1])
			)

		def RemovePair(pair: tuple[int, int], docID: int, pos: int):
			if pair in pairLocations:
				pairLocations[pair].discard((docID, pos))
			pairCounts[pair] -= 1

		while len(tokenToID) < targetCount:
			# Current highest pair
			while heap:
				negativeCount, a, b = heapq.heappop(heap)
				if pairCounts[(a, b)] == -negativeCount:
					break
			else:
				break

			# Create token
			tokenIndex += 1
			newToken = IDtoToken[a] + IDtoToken[b]
			if newToken in tokenToID:
				continue

			newID = tokenIndex
			tokenToID[newToken] = newID
			IDtoToken[newID] = newToken

			# Get all locations before modfying
			locations = list(pairLocations[(a, b)])

			for docID, pos in locations:
				group = tokenisedGroups[docID]

				# Position may be invalid after previous merges
				if pos >= len(group)-1:
					continue
				if group[pos] != a or group[pos+1] != b:
					continue

				# Remove affected pairs
				if pos > 0:
					RemovePair(
						(group[pos-1], a),
						docID,
						pos-1
					)
				RemovePair(
					(a, b),
					docID,
					pos
				)
				if pos + 2 < len(group):
					RemovePair(
						(b, group[pos+2]),
						docID,
						pos+1
					)

				# Replace pair
				group[pos] = newID
				del group[pos+1]

				# Add new neighbouring pairs
				if pos > 0:
					AddPair(
						(group[pos-1], newID),
						docID,
						pos-1
					)
				if pos + 1 < len(group):
					AddPair(
						(newID, group[pos+1]),
						docID,
						pos
					)

			# Remove old pair completely
			pairLocations[(a,b)].clear()
			pairCounts[(a,b)] = 0

		endTime: float = time.time()
		print(f"It took: {endTime-startTime} seconds.")




		with open("Tokeniser.json", "w", encoding = "utf-8") as file:
			json.dump(tokenToID, file, indent = 4)


	_categoryCache: dict[str, str] = {}

	def _DecideType(self, character: str, previous: str) -> str:
		category: str = self._categoryCache.get(character, "").upper()
		if category == "":
			category: str = unicodedata.category(character)
			self._categoryCache[character] = category

		TEXT_CODES: list[str] = [
			"Lu", "Ll", "Lt", "LC", "Lm", "Lo", "L", # Letters with different cases
			"Mn", "Mc", "Me", "M" # Modifier characters
		]
		NUMBER_CODES = [
			"Nd", "Nl", "No", "N" # Numbers
		]
		PUNCTUATION_CODES = [
			"Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po", "P", # Punctuation
			"Sm", "Sc", "Sk", "So", "S", # Maths, currency, modifier, other symbols
		]
		WHITESPACE_CODES = [
			"Zs"
		]
		NEWLINE_CODES = [
			"Zl", "Zp", # Line+paragraph separators
			"Cc", "Cf" # Control + format
		]

		if category in TEXT_CODES:
			return "text"
		elif category in NUMBER_CODES:
			return "number"
		elif category in PUNCTUATION_CODES:
			return f"punctuation{character}{previous}"
		elif category in WHITESPACE_CODES:
			return f"whitespace{character}"
		elif category in NEWLINE_CODES:
			return f"whitespace{character}{previous}"
		else:
			return "other"

	def _PreProcess(self, text: str) -> list[str]:
		"""
		What it must do:
		- Accumulate whitespace
		- Accumulate numbers
		"""
		
			

		groups1: list[tuple[str, str]] = []

		accumulator: list[str] = []
		type: str = ""
		prevType: str = ""

		for i in range(len(text)):
			prevChar = text[i-1]
			char = text[i]

			type = self._DecideType(char, prevChar)

			if type != prevType and prevType != "":
				groups1.append((prevType, "".join(accumulator)))
				accumulator = []

			accumulator.append(char)
			prevType = type
		groups1.append((type, "".join(accumulator)))



		# Fuse spaces with the next word
		groups2: list[tuple[str, str]] = []
		prevGroup: tuple[str, str] = ("", "")
		nextGroup: tuple[str, str] = ("", "")
		for i in range(len(groups1)):
			group = groups1[i]
			if prevGroup == ("", ""):
				prevGroup = group
				groups2.append(group)
				continue

			if i < len(groups1)-1:
				nextGroup = groups1[i+1]
			else:
				nextGroup = ("", "")

			if group[0] == "text" and prevGroup[0] == "whitespace ":
				if len(prevGroup[1]) == 1:
					groups2.append((group[0], " "+group[1]))
					prevGroup = group
					continue
				groups2.append((prevGroup[0], prevGroup[1][:-1]))
				groups2.append((group[0], " "+group[1]))
				prevGroup = group
				continue

			if group[0] == "whitespace " and nextGroup[0] == "text":
				prevGroup = group
				continue

			groups2.append(group)
			prevGroup = group

		# Chunk numbers into blocks of 3 (from the end)
		# Split whitespace into correct chunks
		# Separate all punctuations
		groups3: list[str] = []
		for group in groups2:
			if "punctuation" in group[0]:
				for char in group[1]:
					groups3.append(char)

			if "whitespace" in group[0]:
				if WHITESPACE_GROUPS.get(group[1][0]) == None:
					# If its not got a set amount of sizes it can have then do individually
					for char in group[1]:
						groups3.append(char)
					continue
				sizes: list[int] | None = WHITESPACE_GROUPS.get(group[1][0])
				currentLen: int = 0
				if sizes is not None:
					currentLen = len(group[1])
					for size in sizes:
						for i in range(currentLen // size):
							groups3.append(group[1][0]*size)
						currentLen = currentLen % size
				continue

			if group[0] == "number":
				count: int = len(group[1]) // 3
				if len(group[1])%3 != 0:
					groups3.append(group[1][:len(group[1])%3])
					for i in range(count):
						groups3.append(group[1][i*3+len(group[1])%3:i*3+3+len(group[1])%3])
					continue
				for i in range(count):
					groups3.append(group[1][i*3:i*3+3])
				continue

			groups3.append(group[1])
						
		return groups3

#tokeniser = Tokeniser(text = "Hello, World! My name is RAT! How are you doing? Here are 5 spaces: '     ' And seven: '       '. Now I will give some numbers 123456789501245", targetCount = 5)

with open("Model/Tokeniser/TokeniserData.txt", "r", encoding = "utf-8") as tokeniserDataFile:
	tokeniser = Tokeniser(text = tokeniserDataFile.read(), targetCount = 4096)