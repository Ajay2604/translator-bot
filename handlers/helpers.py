import re

def parse_langs(input_str):
    langs = []
    pattern = r'\s+([a-z]{2})'
    matches = re.findall(pattern, input_str)
    if len(matches)==0:
        return False
    for match in matches:
        lang_code = match.strip()
        if len(lang_code) == 2:
            langs.append(lang_code)
    return langs

#usage
str = "/lang   en  ko jp"
langs = parse_langs(str)
print(langs)