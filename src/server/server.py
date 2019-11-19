from functools import reduce

from flask import Flask, make_response
from flask import request, Request

from utils import tokenizer

from index.index import Index
from index.document import IndexDocument

app = Flask(__name__)
index = Index()
index.load()

fields = ['term', 'name', 'position', 'nationality', 'number', 'team', 'foot']

def extract_field_query(req: Request) -> (str, str):
    field, query = None, None

    for _field in fields:
        if req.args.get(_field, None) is not None:
            field = _field
            query = req.args.get(_field)
            break

    return field, query

def get_html_for_docs(docs: [IndexDocument]) -> str:
    urls = ['<div> <a href="{}"> {} </a> </div>'.format(doc.url, doc.name) for doc in docs]
    return '\n'.join(urls)

@app.route('/search', methods=["GET", "OPTIONS"])
def hello_world():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    if request.method == 'OPTIONS':
        return response

    field, query = extract_field_query(request)
    if field is None or query is None:
        response.status = "400"
        response.data = "<h1> Specify a valid query field: one of {} </h1>".format(str(fields))
    else:
        docs = index.get_documents_for_query(field, query)
        response.data = get_html_for_docs(docs)
        response.status = "200"

    return response
