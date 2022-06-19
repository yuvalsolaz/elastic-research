# elastic-research
Elasticsearch queries  research

elasticsearch and kibana server 
# elastic - kibana bridge 
docker network create es-net --driver=bridge

# running elastic server from docker 
docker run -d --name es-container --net es-net -p 9200:9200 -e xpack.security.enabled=false -e discovery.type=single-node docker.elastic.co/elasticsearch/elasticsearch:7.11.0

firefox http://localhost:9200

# running kibana server from docker   
docker run -d --name kb-container --net es-net -p 5601:5601 -e ELASTICSEARCH_HOSTS=http://es-container:9200 docker.elastic.co/kibana/kibana:7.11.0

firefox http://localhost:5601

