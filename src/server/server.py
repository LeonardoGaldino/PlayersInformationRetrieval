from functools import reduce

from flask import Flask
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

@app.route('/search')
def hello_world():
    field, query = extract_field_query(request)
    if field is None or query is None:
        return "<h1> Specify a valid query field: one of {} </h1>".format(str(fields))

    docs = index.get_documents_for_query(field, query)
    return get_html_for_docs(docs)
