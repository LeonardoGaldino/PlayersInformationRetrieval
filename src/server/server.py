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

document_anchor_HTML = """
    <div class="card" style="height: 93px;margin-left: 166px;margin-bottom: 27px">
        <div class="card-body">
            <a class="card-title" href={} style="margin-bottom: 0px;color: #1a0dab;font-size: 20px;
                font-weight: 400;line-height: 26px;font-family:arial,sans-serif">
                {}
            </a>
            <br>
            <a class="card-subtitle mb-2 text-muted" href={} style="margin-bottom: 0px;margin-top: 0px;
                color:#006621;font-style: normal;font-size: 16px;font-weight: 400;line-height: 24px;
                padding-top: 1px;font-family:arial,sans-serif">
            {}
            </a>
            <br>
            <span class="card-text" style="text-align: left;color: #545454;font-family: arial,sans-serif;
                font-size: 14px;font-weight: 400;line-height: 21.98px;">
            {}
            </span>
        </div>
    </div>'
"""

def extract_req_params(req: Request) -> (str, str, int, bool):
    try:
        max_size = int(req.args.get('max_size', '10'))
    except:
        max_size = 10

    tf_idf = not req.args.get('tfidf', '1') == '0'

    field, query = None, None

    for _field in fields:
        if req.args.get(_field, None) is not None:
            field = _field
            query = req.args.get(_field)
            break

    return field, query, max_size, tf_idf

def get_html_for_docs(docs: [IndexDocument]) -> str:
    for doc in docs:
        description = ""
        attrs = ["name", "nationality", "number", "position", "team"]

        for attr in dir(doc):
            if(getattr(doc, attr) is not None and attr in attrs):
                presentable_attr = attr[0].upper() + attr[1:]
                description = description + " | " + "<strong>" + presentable_attr + ": </strong>" + str(getattr(doc, attr))
                doc.description = description
        doc.description += " |"

    urls = [document_anchor_HTML.format(doc.url, doc.name,doc.url,doc.url.split(".com")[0]+".com",doc.description) for doc in docs]
    return '\n'.join(urls)

@app.route('/search', methods=["GET", "OPTIONS"])
def hello_world():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    if request.method == 'OPTIONS':
        return response

    field, query, max_size, tf_idf = extract_req_params(request)
    if field is None or query is None:
        response.status = "400"
        response.data = "<h1> Specify a valid query field: one of {} </h1>".format(str(fields))
    else:
        docs = index.get_documents_for_query(field, query, max_size, tf_idf)
        response.data = get_html_for_docs(docs)
        response.status = "200"

    return response
