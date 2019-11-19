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
    descricao = ""
    for doc in docs:
        descricao = ""
        for attr in dir(doc):
            if(getattr(doc, attr)!=None and (attr=="name" or attr=="nationality" or attr=="number" or attr=="position" or attr=="team")):
                descricao=descricao+attr+"-"+ str(getattr(doc, attr))+" "
                doc.descricao = descricao
                #print("doc.%s = %r" % (attr, getattr(doc, attr)))
    urls = ['<div class="card" style="width: 677px;height: 93px;margin-left: 166px;margin-bottom: 27px"><div class="card-body"><a class="card-title" href={} style="margin-bottom: 0px;color: #1a0dab;font-size: 20px;font-weight: 400;line-height: 26px;font-family:arial,sans-serif">{}</a><br><a class="card-subtitle mb-2 text-muted" href={} style="margin-bottom: 0px;margin-top: 0px;color:#006621;font-style: normal;font-size: 16px;font-weight: 400;line-height: 24px;padding-top: 1px;font-family:arial,sans-serif">{}</a><br><span class="card-text" style="text-align: left;color: #545454;font-family: arial,sans-serif;font-size: 14px;font-weight: 400;line-height: 21.98px;">{}</span></div></div>'.format(doc.url, doc.name,doc.url,doc.url.split(".com")[0]+".com",doc.descricao) for doc in docs]
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
