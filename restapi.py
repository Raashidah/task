from flask import Flask, make_response, jsonify, request
import dataset

app = Flask(__name__)
db = dataset.connect('sqlite:///restapi.db')

table = db['topics']

def fetch_db(topic_id):  # Each book scnerio
    return table.find_one(topic_id=topic_id)

def fetch_db_all():
    topics = []
    for topic in table:
        topics.append(topic)
    return topics

@app.route('/db_populate', methods=['GET'])
def db_populate():
    table.insert({
        "topic_id": "1",
        "name": "Azure",
        "comment": "Azure is a good to start cloud platform"
    })

    table.insert({
        "topic_id": "2",
        "name": "aws",
        "comment": "aws is cloud platform"
    })

    return make_response(jsonify(fetch_db_all()),
                         200)


@app.route('/topics', methods=['GET', 'POST'])
def add_get_topics():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
        topic_id = content['topic_id']
        table.insert(content)
        return make_response(jsonify(fetch_db(topic_id)), 201)  # 201 = Created


@app.route('/topics/<topic_id>', methods=['GET', 'POST','PUT'])
def update_view_specific_topic(topic_id):
    if request.method == "GET":
        topic_obj = fetch_db(topic_id)
        if topic_obj:
            return make_response(jsonify(topic_obj), 200)
        else:
            return make_response(jsonify(topic_obj), 404)
    elif request.method == "PUT":  # Updates the book
        content = request.json
        table.update(content, ['topic_id'])

        topic_obj = fetch_db(topic_id)
        return make_response(jsonify(topic_obj), 200)


@app.route('/topics/<topic_id>/comments', methods=['POST'])
def addComments():
        content = request.json
        topic_id = content['comment']
        table.insert(content)
        return make_response(jsonify(fetch_db(topic_id)), 201)  # 201 = Created


if __name__ == '__main__':
    app.run(debug=True)