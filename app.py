from typing import Optional

from flask import Flask, request, jsonify, abort, Response
from random import choice
from yaml import safe_load
from spacy import load, cli

app = Flask(__name__)
cli.download("en_core_web_sm")
nlp = load("en_core_web_sm")

def calculate_correctness(correct_ans:str, response:str) -> int:
    correct_ans = nlp(correct_ans)
    response = nlp(response)
    return int(response.similarity(correct_ans)*100)

with open('h2_physics.yml', 'r') as file:
    h2_definitions: dict[str,dict[str,dict]] = safe_load(file)
    raw_definitions: dict[str,str] = {term: definition for chapters in h2_definitions.values() for chapter in chapters.values() for term, definition in chapter.items()}

@app.route('/get_term', methods=['GET'])
def get_term() -> Response:
    subject: Optional[str] = request.args.get('subject_code', None)
    if subject not in ["9749"]:
        abort(400)
    random_term: str = choice(list(raw_definitions.keys()))
    for section, chapters in h2_definitions.items():
        for chapter, terms in chapters.items():
            if random_term in terms:
                target_chapter: str = chapter
    return {'term':random_term,'display':f"What is the definition of {random_term}? [{target_chapter}]"}

@app.route('/verify_answer', methods=['POST'])
def verify_answer() -> str:
    data:dict[str,str] = request.get_json()
    term: Optional[str] = data.get('term', None).strip()
    response: Optional[str] = data.get('response', None).strip().lower()
    if term is None or response is None:
        abort(400)

    score: int = calculate_correctness(raw_definitions[term], response)
    if score >= 70:
        return "Your response looks good — Model Answer: {}".format(raw_definitions[term])
    return "Your response is insufficient — Model Answer: {}".format(raw_definitions[term])

if __name__ == '__main__':
    print("App is running")
    app.run()
