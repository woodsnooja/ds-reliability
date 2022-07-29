practice_text = "[PM] change out idler bearing."

practice_text_tokens_punkt = word_tokenize(practice_text)
practice_text_phrase = phrase_model[practice_text_tokens_punkt]

print(f'{practice_text_tokens_ws}\n{practice_text_phrase}')
