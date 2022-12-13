from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://api-qs.hocky.id/bigdata/sparql")


def select():
  sparql.setReturnFormat(JSON)
  with open('sparql/playground.rq') as f:
    query = f.read() % {'queries': ':Q1073666'}
    print(query)
    sparql.setQuery(query)

    ret = sparql.queryAndConvert()['results']['bindings']
    print(ret)


def describe():
  with open('sparql/playground.rq') as f:
    query = f.read() % {'queries': ':Q1073666'}
    print(query)

    sparql.setQuery(query)

    ret = sparql.queryAndConvert()
    ret = ret.serialize(format='json-ld')
    print(ret)


# select()
describe()
