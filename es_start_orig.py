import os
import sys
from core.metrics import time_it
from core.logger import get_logger
from app.api.process import Process
from app.api import service 
from elasticsearch import Elasticsearch, helpers


processor=Process()
config = processor.config
logger = get_logger(__name__)

def create_index(es,index_field, index_name):
    try:
        """Creates an index in Elasticsearch with specified settings and mappings."""
        settings = {
            "settings": {
                "number_of_shards": 5,
                "number_of_replicas": 1,
                "refresh_interval": "30s",
                "analysis": {
                    "analyzer": {
                        "autocomplete_analyzer": {
                            "type": "custom",
                            "tokenizer": "autocomplete_tokenizer",
                            "filter": ["lowercase", "autocomplete_filter"]
                        }
                    },
                    "filter": {
                        "autocomplete_filter": {
                            "type": "edge_ngram",
                            "min_gram": 1,
                            "max_gram": 20,
                            "token_chars": ["letter", "digit"]
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    index_field : {
                        "type": "text",
                        "analyzer": "autocomplete_analyzer",
                        "search_analyzer": "standard"
                    }
                }
            }
        }
        es.indices.create(index=index_name, body=settings, ignore=400)  # ignore 400 already exists code

    except Exception as e:
        logger.error(f"While processing in Function {create_index.__qualname__}, we got {sys.exc_info()[0]} Exception. \n '{e}' in Line Number {sys.exc_info()[2].tb_lineno}  File Name {os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename)}")

def fetch_data(table_data):
    try:
        connection = service.db_conn()
        with connection.cursor() as cur:
            cur.execute(f"SELECT {table_data[0]}, {table_data[1]} FROM {table_data[2]}")
            for result in cur:
                yield {
                    "_index": table_data[3],
                    "_id": result[table_data[0]],
                    "_source": {
                        table_data[1]: result[table_data[1]]
                    }
                }
            cur.close()
            connection.close()
    except Exception as e:
            logger.error(f"While processing in Function {fetch_data.__qualname__}, we got {sys.exc_info()[0]} Exception. \n '{e}' in Line Number {sys.exc_info()[2].tb_lineno}  File Name {os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename)}")


@time_it("indexing data")
def bulk_index(data, table_data):
    try:
        """Bulk index data into Elasticsearch."""
        es = Elasticsearch("http://localhost:9200")
        create_index(es, table_data[1],table_data[3])
        es = es.options(request_timeout=30)
        helpers.bulk(es, data)

    except Exception as e:
        logger.error(f"While processing in Function {bulk_index.__qualname__}, we got {sys.exc_info()[0]} Exception. \n '{e}' in Line Number {sys.exc_info()[2].tb_lineno}  File Name {os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename)}")

#tables_data = [("ncbi_id","organism_name","Biofilm.organisms","organisms"),("experiment_id","experiment_name","Biofilm.experiment","experiments"),("experiment_id","project","Biofilm.experiment","projects")]
tables_data = [("ncbi_id","organism_name","Biofilm.organisms","organisms")]

if __name__ == '__main__':
    for table_data in tables_data:
        data = fetch_data(table_data)
        bulk_index(data, table_data)
        print(f"Indexing Setup complete for table: {table_data[3]}")