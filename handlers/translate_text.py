from googletrans import Translator, LANGUAGES
translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])

def print_supported_languages():
    str = ''
    str = str + "Supported languages: \n "
    for code, name in LANGUAGES.items():
        if '-' not in code:
            str = str + (f"{name} ({code})\n")
    return str

async def translate_text(text, langs): # translate text to/from langs
    lang1 = langs[0]
    lang2 = langs[1]
    srcLang = translator.detect(text).lang # detect the source 
    if srcLang == lang1:
        translation = translator.translate(text, dest=lang2)
    elif srcLang == lang2:
        translation = translator.translate(text, dest=lang1)
    else:
        return f'''Unsupported source language: {srcLang} 
                \nif it is a mistake, try to change grammer of your text.
                \nYou can change language prefrence by sending /lang <> <> 
                \neg. '/lang en ko' for English-korean 
                \n'''
    # {print_supported_languages()}

    return translation.text

# # usage
# text = "Hello, world!"
# langs = ['en','ko'] # from English to Korean
# print(translate_text(text, langs))