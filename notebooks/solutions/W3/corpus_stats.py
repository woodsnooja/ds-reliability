from collections import Counter
import itertools

a3b2b_cleaned = [
    text_cleaner(text=text.lower(), norm_dict=word_normalisation_dictionary)
    for text in a3b2b_corpus
]

a3b2b_tokenized = [word_tokenize(text) for text in a3b2b_cleaned]

a3b2b_phrases = [cleaned_phrase_model[text] for text in a3b2b_tokenized]

a3b2b_counts = Counter(itertools.chain.from_iterable(a3b2b_phrases))

print(f"Total tokens:\n{sum(a3b2b_counts.values())}")
print(f"Top 10 tokens:\n{a3b2b_counts.most_common(10)}")
print(f"Rarest 10 tokens:\n{a3b2b_counts.most_common()[-10:]}")
