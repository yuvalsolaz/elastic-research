'''
    build query:
        1. phrase match
        2. multi clause blocks
        3. optional fuzziness per term
        4. optional terms slope in the context of a multi search
        5. terms in order switch
        6. whatever
'''
import sys
import json


def build_term(term, field_name, fuzziness):
    query = {"span_multi":
        {"match":
            {"fuzzy":
                {field_name: {
                    "fuzziness": fuzziness,
                    "value": term
                }
                }
            }
        }
    }

    return json.dumps(query)


def build_query(terms):
    clouse = []
    for term in terms:
        term_block = build_term(term=term, field_name='text', fuzziness=3)
        clouse.append(term_block)
    return clouse



if __name__ == '__main__':

    if len(sys.argv) < 2:
        print(f'usage: python {sys.argv[0]} <terms>')
        exit(1)

    terms = sys.argv[1:]

    print(f'build span multi query from: {terms}')
    query = build_query(terms=terms)
    print(query)
