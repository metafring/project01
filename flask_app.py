from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    name = 'John'  # 예시로 이름을 설정
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
    # app.run()