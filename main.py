import json
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from model import ErrorResponse, SearchQuery, SearchResponse, \
  SpellCheckResponse, ContentQuery, ContentResponse
from search import generate_fuzzy_model, bm25_searcher
from sparql import construct, select, constructBatch

load_dotenv()
app = FastAPI()
STATIC_PATH = "/static"
SPELL_CHECKER = lambda ret: ""


class Dummy:
  def search(self, query, cutoff):
    return ""


SEARCH_ENGINE = Dummy()

origins = [
  "*"
]


@app.on_event("startup")
async def startup_event():
  global SPELL_CHECKER, SEARCH_ENGINE
  SPELL_CHECKER = generate_fuzzy_model()
  SEARCH_ENGINE = bm25_searcher()


app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["POST", "GET"],
  allow_headers=["*"],
)


@app.get("/")
async def read_root():
  return {
    "code": 200
  }


def computeContent(query: ContentQuery):
  triples = construct(query.type, query.id)
  return json.loads(triples)


def computeSearchResult(result: str):
  triples = constructBatch(result)
  print(triples)
  return json.loads(triples)


@app.post("/search", response_model=SearchResponse)
async def search(query: SearchQuery):
  spell_checked = SPELL_CHECKER(query.content)
  changed = not (spell_checked == query.content)
  result = list(SEARCH_ENGINE.search(spell_checked, cutoff=10))
  for i in range(len(result)):
    # print(result[i])
    result[i]['score'] = float(result[i]['score'])
  # print(result[0]['id'])
  contentID, type = result[0]['id'].split()
  print(result)
  top_result = {
    "content": (computeContent(ContentQuery(contentID, type))
                if len(result) > 0
                else dict()),
    "type": type,
    "id": contentID
  }
  desc = computeSearchResult(" ".join([f":{res['id'].split()[0]}" for res in result]))
  return SearchResponse(200, result, desc, top_result, spell_checked, changed)


@app.post("/spellcheck", response_model=SpellCheckResponse)
async def spellcheck(query: SearchQuery):
  result = SPELL_CHECKER(query.content)
  changed = not (result == query.content)
  return SpellCheckResponse(200, result, changed)


@app.post("/content", response_model=ContentResponse)
async def content(query: ContentQuery):
  result = computeContent(query)

  return ContentResponse(200, result)


def common_error(err: Exception):
  """
  Returns abnormal JSONResponse
  """
  return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                      content=ErrorResponse("invalid request",
                                            f"{str(err)}").dict())


if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info",
              reload=True)
