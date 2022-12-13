from SPARQLWrapper import SPARQLWrapper, JSON, CSV

sparql = SPARQLWrapper("https://api-qs.hocky.id/bigdata/sparql")


def select(type="university", queryID='Q1073666'):
  with open(f'sparql/{type}.rq') as f:
    query = f.read() % {'queries': f':{queryID}'}
    print(query)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    ret = sparql.queryAndConvert()["results"]["bindings"]
    return ret


def construct(type="university", queryID='Q1073666'):
  if (type != "university"): type = "item"
  with open(f'sparql/{type}.rq') as f:
    query = f.read() % {'queries': f':{queryID}'}
    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    ret = ret.serialize(format='json-ld')
    return ret


def constructBatch(resultIDs: str):
  with open(f'sparql/labeler.rq') as f:
    query = f.read() % {'resultIDs': f'{resultIDs}'}
    sparql.setQuery(query)
    # print(query)
    ret = sparql.queryAndConvert()
    ret = ret.serialize(format='json-ld')
    return ret


def describe():
  with open('sparql/playground.rq') as f:
    query = f.read() % {'queries': ':Q1073666'}
    # print(query)

    sparql.setQuery(query)

    ret = sparql.queryAndConvert()
    ret = ret.serialize(format='json-ld')
    # print(ret)


if __name__ == '__main__':
  construct()
# describe()
