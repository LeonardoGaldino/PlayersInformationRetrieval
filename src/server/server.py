from functools import reduce

from flask import Flask
from flask import request, Request

from utils import tokenizer

from index import index, document

app = Flask(__name__)
_index = index.Index()
_index.load()

def extract_query_type_terms(mapping: dict) -> (str, [str]):
    query_type, query = None, None

    for key, value in mapping.items():
        if value is not None:
            query_type = key
            query = value
            break

    if query_type is None and query is None:
        return None, None
    
    return query_type, [token.lower() for token in tokenizer.tokenize(query)]


def _reduce_set_return(d: dict, query_type: str):
    d[query_type] = request.args.get(query_type, None)
    return d

def get_docs_ids(req: Request):
    query_types = ['term', 'name', 'position', 'nationality', 'number', 'team', 'foot']
    mapping = reduce(_reduce_set_return, query_types, {})

    query_type, terms = extract_query_type_terms(mapping)
    if query_type is None:
        return []

    docs = [_index.find_documents(query_type, term) for term in terms]

    docs = reduce(lambda acc, v: acc+v, docs, [])

    docs_vectors = [document.DocumentVector(doc, _index) for doc in docs]

    query_doc = document.QueryDocument(None, terms)
    query_vector = document.DocumentVector(query_doc, _index)

    for doc_vector in docs_vectors:
        doc_vector.project(query_vector)

    docs_score_vectors = [(query_vector.similarity(doc_vector), doc_vector) for doc_vector in docs_vectors]

    docs_score_vectors.sort()
    docs_score_vectors.reverse()

    return [d[1].doc.id for d in docs_score_vectors]

@app.route('/search')
def hello_world():
    ids = get_docs_ids(request)
    ids = [str(_id) for _id in ids]
    return 'Hello, world: ' + ','.join(ids)
