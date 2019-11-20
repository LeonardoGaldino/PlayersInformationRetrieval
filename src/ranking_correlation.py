import sys

from index.document import IndexDocument
from index.index import Index
from server.server import fields
from index.utils import kendal_tau


QUERIES = [
            ('term', 'neymar messi', 10), ('term', 'cristiano fifa ronaldo', 30), ('term', 'cristiano brazil attacker', 30),
            ('name', 'Leonel Messi', 10), ('name', 'Robinho', 10), 
            ('position', 'defender', 50), 
            ('nationality', 'brazil', 30),
            ('number', '33', 20), 
            ('team', 'juventus', 15),
            ('foot', 'both', 30)
        ]

for i, query in enumerate(QUERIES):
    if not query[0] in fields:
        print('{} is not a valid field (in query #{}). Try one of: {}'.format(query[0], i+1, str(fields)))
        sys.exit(1)

index = Index()
index.load()

def main():
    for query in QUERIES:
        ranking_tfidf = index.get_documents_for_query(query[0], query[1], query[2], True)
        ranking_raw = index.get_documents_for_query(query[0], query[1], query[2], False)

        correlation = kendal_tau(ranking_tfidf, ranking_raw)
        print('For query [{}] on field [{}]: {} Kendal Tau correlation. Rankings with {} documents.'.format(query[1], query[0], correlation, query[2]))

if __name__ == '__main__':
    main()

