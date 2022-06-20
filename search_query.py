'''
    build query:
        1. phrase match
        2. multi clause blocks
        3. optional fuzziness per term
        4. optional terms slope in the context of a multi search
        5. terms in order switch
        6. TODO: boost for each term (implement with nested span or )
'''
import sys
import json
from collections import namedtuple
from elasticsearch import Elasticsearch

Term = namedtuple("Term", "value fuzziness")

def build_term_block(term: Term, field_name):
    return {"span_multi":
        {"match":
            {"fuzzy":
                {field_name: {
                    "fuzziness": term.fuzziness,
                    "value": term.value,
                }
                }
            }
        }
    }


def build_query(terms, slop=0, in_order=True, field_name='text'):
    query = {"query": {"span_near": {"clauses": []}}}
    for term in terms:
        term_block = build_term_block(term=term, field_name=field_name)
        query["query"]["span_near"]["clauses"].append(term_block)
    query["query"]["span_near"]["slop"] = slop
    query["query"]["span_near"]["in_order"] = "true" if in_order else "false"
    return query

def get_results(es, index_name, query):
    res = es.search(index=index_name, body=query)
    print(f"Total number of results: {len(res['hits']['hits'])}, For query: {query}")
    for i in range(len(res['hits']['hits'])):
        print(f"Doc id: {res['hits']['hits'][i]['_id']} "
              f" ,Score: {res['hits']['hits'][i]['_score']}, "
              f" ,Text: {res['hits']['hits'][i]['_source']['text']}")


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print(f'usage: python {sys.argv[0]} <terms>')
        exit(1)

    args = sys.argv[1:]
    terms = [Term(fuzziness=2, value=arg) for arg in args]
    print(f'build span multi query from: {terms}')
    query = build_query(terms=terms, slop=5, in_order=False)

    es = Elasticsearch(r'http://localhost:9200')
    index_name = "demo_idx"
    get_results(es=es, index_name=index_name, query=query)
