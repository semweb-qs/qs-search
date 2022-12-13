from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://api-qs.hocky.id/bigdata/sparql")


def construct(type="university", queryID='Q1073666'):
  with open(f'sparql/{type}.rq') as f:
    query = f.read() % {'queries': f':{queryID}'}
    print(query)
    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    ret = ret.serialize()
    print(ret)
    return ret

def describe():
  with open('sparql/playground.rq') as f:
    query = f.read() % {'queries': ':Q1073666'}
    print(query)

    sparql.setQuery(query)

    ret = sparql.queryAndConvert()
    ret = ret.serialize(format='json-ld')
    print(ret)

if __name__ == '__main__':
    construct()
# describe()
