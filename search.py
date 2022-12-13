import csv
from unidecode import unidecode
from fuzzywuzzy import process
from termcolor import colored, cprint
from fuzzy_search.fuzzy_phrase_searcher import FuzzyPhraseSearcher
from fuzzy_search.fuzzy_phrase_model import PhraseModel
from rank_bm25 import BM25Okapi
from retriv import SearchEngine

UNIVERSITY = "university"
CITY = "city"
REGION = "region"
COUNTRY = "country"
TYPE = "type"
YEAR = "year"
AWARD = "award"


def load_csv():
  with open('semweb-data-008.csv', 'r') as f:
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
  collection = []
  print(head[15])
  id_exist = set()

  def insert_to_collection(id, text, jenis):
    if id in id_exist: return
    id_exist.add(id)
    collection.append({
      "id": f"{id} {jenis}",
      "text": text
    })

  for i in range(row_size):
    entry = csv_file[i]
    cleaned = unidecode(entry[0]).lower()
    corpus.append(cleaned)
    insert_to_collection(entry[15].split('/')[-1], cleaned, UNIVERSITY)
    try:
      rank = entry[17].split(':')[1].replace('-', ' ')
      insert_to_collection(entry[17].replace(':', 'R').replace('-', 'to'),
                           f"qs world ranking peringkat ke award penghargaan {entry[1]} tahun year {rank}",
                           AWARD)
      insert_to_collection(entry[1],
                           f"qs world ranking list peringkat daftar tahun year {entry[1]}",
                           YEAR)
    except:
      pass
    if(entry[9]):
      insert_to_collection(entry[9], f"tipe type {entry[9]}" ,TYPE)
    insert_to_collection(entry[18], f"city kota located location lokasi di at {entry[6]} {entry[5]}" ,CITY)
    insert_to_collection(entry[19], f"nation country negara located location lokasi di at {entry[5]} {entry[7]}" ,COUNTRY)
    insert_to_collection(entry[20], f"region benua daerah located location lokasi di at {entry[7]}" ,REGION)


  se = SearchEngine("university")
  print(collection[0:10])
  # print(corpus)

  se.index(collection)

  result = se.search("university indonesia")
  print(result)


def main():
  # generate_fuzzy_model()
  bm25_searcher()
  pass


if __name__ == '__main__':
  main()
