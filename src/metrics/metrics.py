import sys
from datetime import datetime

from index.document import IndexDocument
from index.index import Index
from server.server import fields
from index.utils import kendal_tau
from metrics.utils import avg_sd

index = Index()
index.load()

def validate_queries(queries):
    for i, query in enumerate(queries):
        if not query[0] in fields:
            print('{} is not a valid field (in query #{}). Try one of: {}'.format(query[0], i+1, str(fields)))
            sys.exit(1)

def ranking_correlation(queries):
    validate_queries(queries)

    for query in queries:
        ranking_tfidf = index.get_documents_for_query(query[0], query[1], query[2], True)
        ranking_raw = index.get_documents_for_query(query[0], query[1], query[2], False)

        correlation = kendal_tau(ranking_tfidf, ranking_raw)
        print('For query [{}] on field [{}]: {} Kendal Tau correlation. Rankings with {} documents.'.format(query[1], query[0], correlation, query[2]))


def query_response_time(queries):
    validate_queries(queries)
    num_repetitions = 100

    for query in queries:
        delays = []
        for _ in range(num_repetitions):
            t0 = datetime.now()
            index.get_documents_for_query(query[0], query[1], query[2], True)
            t1 = datetime.now()
            delays.append((t1 - t0).microseconds)
        avg_tfidf, sd_tfidf = avg_sd(delays)

        delays = []
        for _ in range(num_repetitions):
            t0 = datetime.now()
            index.get_documents_for_query(query[0], query[1], query[2], False)
            t1 = datetime.now()
            delays.append((t1 - t0).microseconds)
        avg_raw, sd_raw = avg_sd(delays)

        avg_tfidf /= 1000.0
        sd_tfidf /= 1000.0
        avg_raw /= 1000.0
        sd_raw /= 1000.0

        print('For query [{}] on field [{}], {} documents with tf_idf: {}ms avg | {}ms standard deviation.'.format(query[1], query[0], query[2], avg_tfidf, sd_tfidf))
        print('For query [{}] on field [{}], {} documents without tf_idf: {}ms avg | {}ms standard deviation.'.format(query[1], query[0], query[2], avg_raw, sd_raw))