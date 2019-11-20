import sys

from index.document import IndexDocument
from index.index import Index
from server.server import fields
from index.utils import kendal_tau


QUERIES = [('term', 'neymar messi'), ('foot', 'both'), ('nationality', 'brazil'),
            ('position', 'attacker'), ('position', 'defender'), ('name', 'Leonel Messi'), 
            ('term', 'cristiano fifa ronaldo'),('number', '33'), ('team', 'juventus')]

for i, query in enumerate(QUERIES):
    if not query[0] in fields:
        print('{} is not a valid field (in query #{}). Try one of: {}'.format(query[0], i+1, str(fields)))
        sys.exit(1)

index = Index()
index.load()

def main():
    for query in QUERIES:
        ranking_tfidf = index.get_documents_for_query(query[0], query[1], True)
        ranking_raw = index.get_documents_for_query(query[0], query[1], False)

        correlation = kendal_tau(ranking_tfidf, ranking_raw)
        print('For query [{}] on field [{}]: {} Kendal Tau correlation'.format(query[1], query[0], correlation))

if __name__ == '__main__':
    main()

