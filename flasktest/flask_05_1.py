from flask import Flask, render_template

# app = Flask(__name__, static_folder='static', template_folder='templates')
app = Flask(__name__, template_folder='templates')


@app.route('/hello/<user>')
def hello_name(user):
    return render_template('templates_05_1.html', name=user)


if __name__ == '__main__':
    app.run(debug=True)

'''
Jinja : 파이썬으로 작성된 템플릿팅 엔진 : API 응답을 쉽게 렌더링함 

{{ }} : 변수 블럭 : varialbe block : 변수 저장
{% %} : 구조(처리)를 제어하기 위한 명령 지정 :  if/else, 반복(loop), 매크로, 템플릿 상속
{# 주석 #} : 주석 : 웹 페이지에 표시 않됨

필터 : |
------------------
{{ variable | filter_name(*args)}} : 인수가 있는 경우 
{{ variable | filter_name} : 인수가 없는 경우 


기본 필터
------------------
{{ todo.item | default('이것은 기본 todo 아이템입니다.')}}


변환 필터
------------------
{{ 3.142 | int }} : 3
{{ 31 | float }} : 31.0
{{ ['한빛', '책'] : join(' ') }} : 한빛 책


길이 필터
------------------
Todo count : {{ todos : length }}
Todo count : 4


이스케이프 필터
------------------
{{ "<title>Todo Application</title>"} | escape }} : <title>Todo Application</title>


 if 문
 ------------------
 {% if todo : length < 5 %}
    할 일 목록에 할 일이 많지 안네요.
 {% else %}
    바쁜 날을 보내고 있군요!
 {% endif %}

 반복묵
 {% for todo in toods %}
    <b>{{ todo.item }}</b>
 {% endfor %}
 
'''    