import csv
from unidecode import unidecode
from fuzzywuzzy import process
from termcolor import colored, cprint
from fuzzy_search.fuzzy_phrase_searcher import FuzzyPhraseSearcher
from fuzzy_search.fuzzy_phrase_model import PhraseModel
from rank_bm25 import BM25Okapi



def load_csv():
  with open('semweb-data-007.csv', 'r') as f:
    csv_file = list(csv.reader(f))
  print(csv_file[0])
  return csv_file


def generate_fuzzy_model():
  csv_file = load_csv()
  head = csv_file[0]
  csv_file = csv_file[1:]
  column_size = len(csv_file[0])
  row_size = len(csv_file)

  # highger matching thresholds for higher quality OCR/HTR (higher precision, recall should be good anyway)
  # lower matching thresholds for lower quality OCR/HTR (higher recall, as that's the main problem)
  config = {
    "char_match_threshold": 0.2,
    "levenshtein_threshold": 0.2,
    "ignorecase": True,
    "ngram_size": 2,
    "skip_size": 2,
  }

  # initialize a new searcher instance with the config
  fuzzy_searcher = FuzzyPhraseSearcher(config)
  # create a list of domain keywords and phrases
  domain_phrases = []
  considered_columns = [0, 5, 6, 7, 9]
  cprint("considered columns:", "yellow")
  for cols in considered_columns:
    cprint(head[cols], "blue", end=', ')
  print()
  for i in range(row_size):
    # Nama universitas
    entry = csv_file[i]
    for cols in considered_columns:
      unidecoded = unidecode(entry[cols])
      # if unidecoded != entry[cols]:
      #   cprint(f"{unidecoded}: {entry[cols]}", "red")
      normalized = unidecoded.lower()
      domain_phrases.extend(normalized.split())

  domain_phrases = list(set(domain_phrases))
  # create a PhraseModel object from the domain phrases
  phrase_model = PhraseModel(phrases=domain_phrases)

  # register the phrase model with the searcher
  fuzzy_searcher.index_phrase_model(phrase_model)

  # take some example texts: meetings of the Dutch States General in January 1725
  text1 = "aindoesia"
  # look for matches in the first example text
  for match in fuzzy_searcher.find_matches(text1):
    print(match)
  res = process.extract(text1, domain_phrases, limit=5)
  print(res)

def bm25_searcher():

  csv_file = load_csv()
  head = csv_file[0]
  csv_file = csv_file[1:]
  column_size = len(csv_file[0])
  row_size = len(csv_file)
  corpus = []

  for i in range(row_size):
    entry = csv_file[i]
    corpus.append(unidecode(entry[0]).lower())
  # print(corpus)
  corpus = list(set(corpus))
  corpus = [s.split() for s in corpus]
  bm25 = BM25Okapi(corpus)
  query = "universitas".split()
  top_k = bm25.get_top_n(query, corpus, n=5)
  print(top_k)




def main():
  # generate_fuzzy_model()
  bm25_searcher()
  pass


if __name__ == '__main__':
  main()
