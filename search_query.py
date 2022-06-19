
'''
{"query":
{
  "span_near": {
    "clauses": [
      {
        "span_multi": {
          "match": {
            "fuzzy": {
              "content": {
                "fuzziness": "2",
                "value": "word"
              }
            }
          }
        }
      },
      {
        "span_multi": {
          "match": {
            "fuzzy": {
              "content": {
                "fuzziness": "2",
                "value": "another"
              }
            }
          }
        }
      }
    ],
    "slop": 1,
    "in_order": "true"
  }
}

'''

import sys
import json
import pprint
from collections import defaultdict

def build_query(terms):
    nested_dict = lambda: defaultdict(nested_dict)
    query=nested_dict()
    query['span_near']['clauses']=list()
    query['slop']='1'
    query['in_order']="true"

    for w in terms:
        nest = nested_dict()
        nest["span_multi"]["match"]["fuzzy"]["msg"]["fuzziness"]["value"]=w
        nest["span_multi"]["match"]["fuzzy"]["msg"]["fuzziness"]["fuzziness"]="2"
        json.dumps(nest)
        query['span_near']['clauses'].append(json.loads(json.dumps(nest)))

    pprint.pprint(json.loads(json.dumps(query)))

    return query

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print(f'usage: python {sys.argv[0]} <terms>')
        exit(1)

    terms = sys.argv[:]
    print(f'build span multi query from: {terms}')
    build_query(terms=terms)

