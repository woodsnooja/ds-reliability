a3b2a_text_tokens_punkt = word_tokenize(a3b2a_text)
a3b2a_text_phrases = phrase_model[practice_text_tokens_punkt]

print(f'Tokens: {a3b2a_text_tokens_punkt}\nPhrases: {a3b2a_text_phrases}')