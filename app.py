import os

import openai
from flask import Flask, render_template, request, Response

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # 使用环境变量 OPENAI_API_KEY
openai.api_base = os.getenv("OPENAI_API_BASE")  # 指定请求地址，使用环境变量 OPENAI_API_BASE


# run on model gpt-3.5-turbo
@app.route("/", methods=["GET"])
def turbo():
    return render_template("index.html")


@app.route("/gen_text", methods=["POST"])
def generate_text():
    prompt = request.form.get("prompt")
    print(f"prompt is :{prompt}")
    response = openai.ChatCompletion.create(  # Needs OpenAI 0.27 above )
        model="gpt-3.5-turbo-16k",
        max_tokens=4096,
        temperature=0,
        stream=True,
        messages=[
          {"role": "user", "content": prompt}
        ]
    )

    def event_stream():
        for line in response:
            text = line.choices[0].delta.get('content', '')
            if len(text):
                yield text

    return Response(event_stream(), mimetype='text/event-stream')
