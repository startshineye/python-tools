# !usr/bin/python
# -*- coding: utf-8 -*-
from flask import jsonify, abort, request
from flask_swagger import swagger
import jiebahelper
from flask_swagger_ui import get_swaggerui_blueprint
from collections import Counter
import jieba
from flask import Flask
from flask_cors import CORS
from json_flask import JsonFlask
from json_response import JsonResponse
# app = Flask(__name__)
app = JsonFlask(__name__)
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/swagger'
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Jiebao Application"
    }
)


# Register blueprint at URL
# (URL must match the one given to factory function above)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
CORS(app, supports_credentials=True)


@app.route("/swagger")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Segment API"
    return jsonify(swag)


@app.route('/')
def index():
    return 'Jiebao Segment API by Python.'


from flask import make_response


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def para_error(error):
    # 数据错误
    return make_response(jsonify({'error': 'Parameter Error'}), 400)


@app.route('/segment', methods=['POST'])
def segment():
    '''
        切词。不带词性，去停词
        ---
        tags:
          - segment
        parameters:
          - in: body
            name: body
            description: 内容
            required: true
            schema:
                type: string
     '''
    a = request.data.strip()
    if a == '':
        abort(400)
    ret = jiebahelper.dosegment(a)
    return JsonResponse.success(ret, 200, "success")


@app.route('/segmentpos', methods=['POST'])
def segmentpos():
    '''
        切词。带词性，去停词
        ---
        tags:
          - segment
        parameters:
          - in: body
            name: body
            description: 内容
            required: true
            schema:
                type: string
     '''
    a = request.data.strip()
    if a == '':
        abort(400)
    ret = jiebahelper.dosegment_with_pos(a)
    return JsonResponse.success(ret, 200, "success")


@app.route('/segmentall', methods=['POST'])
def segmentall():
    '''
        切词。带词性，不去停词
        ---
        tags:
            - segment
        parameters:
          - in: body
            name: body
            description: 内容
            required: true
            schema:
                type: string
    '''
    a = request.data.strip()
    if not a:
        abort(400)
    ret = jiebahelper.dosegment_all(a)
    return JsonResponse.success(ret, 200, "success")


# 词频率统计
@app.route('/wordcount', methods=['POST'])
def wordcount():
    '''
        切词。带词性，去停词
        ---
        tags:
          - segment
        parameters:
          - in: body
            name: body
            description: 内容
            required: true
            schema:
                type: string
     '''
    a = request.data.strip()
    if a == '':
        abort(400)
    ret = jieba.cut(a.strip())
    wordcount = Counter()
    for word in ret:
        if len(word) > 1 and word not in jiebahelper.stopwords:
            wordcount[word] += 1
    print(wordcount.most_common(10))
    return JsonResponse.success(wordcount.most_common(10), 200, "success")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
