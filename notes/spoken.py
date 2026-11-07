"""Make every figure in a voiceover script spoken in ENGLISH (user rule, 1 Nov 2026).
GSTR-2B -> 'GSTR two B', 3B -> 'three B', AOC-4 -> 'AOC four', ₹87.33 lakh -> 'eighty-seven point three three lakh rupees',
9% -> 'nine percent', 427 -> 'four hundred and twenty-seven', 31 December 2026 -> 'thirty-first December, twenty twenty-six'."""
import re
ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'zero ten twenty thirty forty fifty sixty seventy eighty ninety'.split()
ORD = {'one': 'first', 'two': 'second', 'three': 'third', 'five': 'fifth', 'eight': 'eighth', 'nine': 'ninth', 'twelve': 'twelfth'}

def words(n):
    n = int(n)
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ('' if n % 10 == 0 else '-' + ONES[n % 10])
    if n < 1000: return ONES[n // 100] + ' hundred' + ('' if n % 100 == 0 else ' and ' + words(n % 100))
    if n < 100000: return words(n // 1000) + ' thousand' + ('' if n % 1000 == 0 else (' and ' if n % 1000 < 100 else ' ') + words(n % 1000))
    if n < 10000000: return words(n // 100000) + ' lakh' + ('' if n % 100000 == 0 else ' ' + words(n % 100000))
    return words(n // 10000000) + ' crore' + ('' if n % 10000000 == 0 else ' ' + words(n % 10000000))

def ordinal(n):
    w = words(n); last = re.split(r'[- ]', w)[-1]
    o = ORD.get(last) or (last[:-1] + 'ieth' if last.endswith('y') else last + 'th')
    return w[: len(w) - len(last)] + o

def year(y):
    y = int(y)
    if 2000 <= y <= 2009: return 'two thousand ' + (ONES[y - 2000] if y > 2000 else '')
    return words(y // 100) + ' ' + (words(y % 100) if y % 100 >= 10 else 'oh ' + ONES[y % 100])

def num(s):
    s = s.replace(',', '')
    if '.' in s:
        a, b = s.split('.'); return words(a) + ' point ' + ' '.join(ONES[int(c)] for c in b)
    return words(s)

MONTHS = 'January|February|March|April|May|June|July|August|September|October|November|December'
def speak(t):
    t = re.sub(r'\b(GSTR|AOC|MGT|DRC|MOV|ADT|DPT|CMP|ITR|PMT)\s*-\s*(\d+)([A-Z]?)\b', lambda m: f"{m.group(1)} {words(m.group(2))}{(' ' + m.group(3)) if m.group(3) else ''}", t)
    t = re.sub(r'\b(\d)([AB])\b', lambda m: f"{words(m.group(1))} {m.group(2)}", t)                     # 3B, 2B
    t = re.sub(r'\b(\d{1,2})\s+(' + MONTHS + r')\s+(\d{4})\b', lambda m: f"{ordinal(m.group(1))} {m.group(2)}, {year(m.group(3))}", t)
    t = re.sub(r'\b(\d{1,2})\s+(' + MONTHS + r')\b', lambda m: f"{ordinal(m.group(1))} {m.group(2)}", t)
    t = re.sub(r'₹\s?([\d,]+(?:\.\d+)?)\s*(lakh|crore)', lambda m: f"{num(m.group(1))} {m.group(2)} rupees", t)
    t = re.sub(r'₹\s?([\d,]+(?:\.\d+)?)', lambda m: f"{num(m.group(1))} rupees", t)
    t = re.sub(r'([\d,]+(?:\.\d+)?)\s?%', lambda m: f"{num(m.group(1))} percent", t)
    t = re.sub(r'\bSection\s+(\d+)\(([a-z0-9]+)\)', lambda m: f"Section {words(m.group(1))} {m.group(2)}", t)
    t = re.sub(r'\b(\d{4})-(\d{2})\b', lambda m: f"{year(m.group(1))}–{words(m.group(2))}", t)
    t = re.sub(r'(?<![\w-])(\d[\d,]*(?:\.\d+)?)(?![\w-])', lambda m: num(m.group(1)), t)
    return t

if __name__ == '__main__':
    import sys
    for l in open(sys.argv[1], encoding='utf-8'): print(speak(l.rstrip('\n')))
