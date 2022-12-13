import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from model import ErrorResponse, SearchQuery, SearchResponse, \
  SpellCheckResponse, ContentQuery
from search import generate_fuzzy_model, bm25_searcher

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


@app.post("/search", response_model=SearchResponse)
async def search(query: SearchQuery):
  spell_checked = SPELL_CHECKER(query.content)
  result = list(SEARCH_ENGINE.search(spell_checked, cutoff=10))
  for i in range(len(result)):
    # print(result[i])
    result[i]['score'] = float(result[i]['score'])
  return SearchResponse(200, result)


@app.post("/spellcheck", response_model=SpellCheckResponse)
async def spellcheck(query: SearchQuery):
  result = SPELL_CHECKER(query.content)
  changed = not (result == query.content)
  return SpellCheckResponse(200, result, changed)


@app.post("/content", response_model=SearchResponse)
async def content(query: ContentQuery):
  spell_checked = SPELL_CHECKER(query.content)
  result = list(SEARCH_ENGINE.search(spell_checked, cutoff=10))
  for i in range(len(result)):
    # print(result[i])
    result[i]['score'] = float(result[i]['score'])
  return SearchResponse(200, result)

def common_error(err: Exception):
  """
  Returns abnormal JSONResponse
  """
  return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                      content=ErrorResponse("invalid request",
                                            f"{str(err)}").dict())


if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", reload=True)
