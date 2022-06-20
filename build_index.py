# docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.6.2

import json
from elasticsearch import Elasticsearch


def get_results(es, index_name, query, place, boost=1, use_boost=True, title=""):

    search_query = {
        "query": {
            "bool": {
                "must":
                    [{
                        "query_string": {
                            "query":  query,
                            "quote_field_suffix": ".exact",
                            "fields": ["content"]
                            }
                    }]
            }
        }
    }

    if use_boost is True:
        search_query = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "content": {
                                "query": query,
                            }
                        }

                    }
                }
            }}

    if boost > 0:
        boost_query = {
            "query": query,
            "boost": boost
        }
        search_query["query"]["bool"]["must"]["match"]["content"] = boost_query

    res = es.search(index=index_name, body=search_query)
    print(f"\nTotal number of results: {len(res['hits']['hits'])}, For query: {query}, Place: {place}, title: {title}")
    for i in range(len(res['hits']['hits'])):
        print(f"Doc id: {res['hits']['hits'][i]['_id']} "
              f" ,Score: {res['hits']['hits'][i]['_score']}, "
              f" ,Place: {res['hits']['hits'][i]['_source']['place']}"
              f" ,Content: {res['hits']['hits'][i]['_source']['content']}")
        break



def add_document(es, index_name, content, place, id):
    body = {}
    body["text"] = content
    body["place"] = place
    es.index(index=index_name, body=body, id=id)
    es.indices.refresh(index=index_name)


def count_num_of_documents(es, index_name):
    res =es.cat.count(index_name, params={"format": "json"})
    print(f"\n---> Total number of docs in index ({index_name}) : {res[0]['count']}\n")




def main():
    es = Elasticsearch(r'http://localhost:9200')
    index_name = "demo_idx"

    # delete old content
    if es.indices.exists(index=index_name) is True:
        es.indices.delete(index=index_name)

    add_document(es=es,
                 index_name=index_name,
                 content="Distributed nature, simple REST APIs, speed, and scalability",
                 place="html",
                 id=1)
    add_document(es=es,
                 index_name=index_name,
                 content="Distributed nature, simple APIs, speed, and scalability",
                 place="html",
                 id=2)
    add_document(es=es,
                 index_name=index_name,
                 content="Known for its simple REST APIs, distributed nature, speed, and scalability, Elasticsearch is the central component of the Elastic Stack, a set of open source tools for data ingestion, enrichment, storage, analysis, and visualization.",
                 place="javascript",
                 id=3)

    get_results(es=es, index_name=index_name, query="simple rest", place=None, boost=0, use_boost=False, title="^None")
    get_results(es=es, index_name=index_name, query="simple^1 rest",   place=None, boost=0, use_boost=False, title="^1")
    get_results(es=es, index_name=index_name, query="simple^2 rest^2", place=None, boost=0, use_boost=False, title="^2")


    get_results(es=es, index_name=index_name, query="simple rest", place=None, boost=0, use_boost=True, title="boost=none")
    get_results(es=es, index_name=index_name, query="simple rest", place=None, boost=1, use_boost=True, title="boost=1")
    get_results(es=es, index_name=index_name, query="simple rest", place=None, boost=2, use_boost=True, title="boost=2")



if __name__ == "__main__":
    main()