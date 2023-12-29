import re
from googletrans import LANGUAGES

def parse_langs(input_str):
    langs = []
    pattern = r'\s+([a-z]{2})'
    matches = re.findall(pattern, input_str)
    if len(matches)==0:
        return False
    for match in matches:
        lang_code = match.strip()
        if len(lang_code) == 2:
            if not (lang_code in LANGUAGES):
                return False
            langs.append(lang_code)
    return langs

# # usage
# str = "/lang     ak ko ja"
# langs = parse_langs(str)
# print(langs)