import deepl

auth_key = "" # DeepL API key paste
translator = deepl.Translator(auth_key)

result = translator.translate_text("Merhaba dostum nasılsın ?", target_lang="RU")
print(result.text)