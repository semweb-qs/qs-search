import os
from typing import Any, Optional
from pydantic import BaseModel
from typing import List


class ContentQuery(BaseModel):
  def __init__(self, id: str, type: str, **data: Any):
    super().__init__(**data)
    self.id = id
    self.type = type
  id: Optional[str]
  type: Optional[str]


class SearchQuery(BaseModel):
  content: str
  k: Optional[int] = 10


class Result(BaseModel):
  def __init__(self, score: int, type: str, desc: str, id: str, **data: Any):
    super().__init__(**data)
    self.score = score
    self.id = id
    self.desc = desc
    self.type = type

  type: Optional[str] = ""
  desc: Optional[str] = ""
  score: Optional[int] = 0
  id: Optional[str] = ""


class ContentResponse(BaseModel):
  def __init__(self, code: int, results: dict, **data: Any):
    super().__init__(**data)
    self.code = code
    self.results = results

  results: Optional[dict] = dict()
  code: Optional[int] = 500


class SearchResponse(BaseModel):
  def __init__(self, code: int, results: List[Result],
      top_result: Optional[dict],
      **data: Any):
    super().__init__(**data)
    self.code = code
    self.results = results
    self.top_result = top_result

  top_result: Optional[dict] = dict()
  results: Optional[List[Result]] = []
  code: Optional[int] = 500


class SpellCheckResponse(BaseModel):
  def __init__(self, code: int, spellcheck: str, changed: bool, **data: Any):
    super().__init__(**data)
    self.code = code
    self.spellcheck = spellcheck
    self.changed = changed

  spellcheck: Optional[str] = ""
  changed: Optional[bool] = False
  code: Optional[int] = 500


def get_content(part, cid):
  cur_path = os.path.join(os.getcwd(), "engine", "collection", part, cid)
  try:
    with(open(cur_path, "r")) as buffer:
      return buffer.read()
  except:
    return ""


def engine_to_result_list(engine_list):
  result_list = [Result(engine_result[0], engine_result[1]) for engine_result in
                 engine_list]
  return result_list


class ErrorResponse(BaseModel):
  def __init__(self, error: str, error_description: str, **data: Any):
    super().__init__(**data)
    self.error = error
    self.error_description = error_description

  error: str = "invalid_token"
  error_description: str = "An error has occured"
