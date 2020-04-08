# flask-deploy-test
Test deployment of Flask projects to Heroku
  
go to heroku : https://deploy-test-0001.herokuapp.com/  
go to blog : https://yeowool0217.tistory.com/616
  
  
## **1\. Deploy 하기 전 준비**

-   git 설치(heroku에 flask프로젝트를 master 해주려면 git이 필요합니다.)
-   heroku 회원가입/설치heroku를 사용하기 위해 heroku 회원가입과 heroku CLI를 설치합니다.
-   Flask 설치 / gunicorn 설치

(https://devcenter.heroku.com/articles/heroku-cli)

## **2\. 가상환경 만들기**

\*VSCode를 사용해서 가상 환경을 구축합니다.

일단 VSCode를 열어 원하는 위치에 폴더를 생성합니다.

생성 후 **Ctrl + \`** 를 눌러 터미널에 다음과 같이 입력해 가상 환경을 생성합니다.

`>python -m venv (폴더 이름)`

가상 환경 설정에 관한 것들이 폴더에 생성됩니다.

폴더 이름은 아무거나 해도 상관없지만 보통 폴더명은 env로 합니다.

**Ctrl + Shift + P**를 눌러 **Python: Select Interpreter**를 선택,

방금 생성한 가상 환경의 **Scripts/python.exe**를 선택합니다.

![image](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FciOJ2n%2FbtqDeJnH2Vz%2FnbfbqUjayhhKgndA57qY91%2Fimg.png)  
  

이제 가상 환경 위에서 코드가 돌아갈 수 있도록 활성화시켜줘야 합니다.

**\>프로젝트 폴더/env/Scripts/activate를** VSCode 터미널 창에 입력합니다.

아래와 같이 (env) 혹은 자신이 정한 파일명이 터미널에 명령줄 맨 앞에 출력되어야 합니다.

![image](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FVqovf%2FbtqDecDDP4v%2FXpWhNYe1Sxltam46NhQWl0%2Fimg.png)  

반대로 비활성화할 때는 터미널 창에 **deactivate**를 입력합니다.

![image](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FRdxpz%2FbtqDiaqroqN%2FyYvtYk7TxIUt2ki9mLIYaK%2Fimg.png)  

가상 환경을 사용하면 프로젝트가 독립성을 가지게 됩니다.

\*global 환경에서 사용했던 라이브러리는 사용할 수 없기 때문에 다시 설치해야 합니다.

\*pip list를 해보면 현재 설치된 라이브러리 목록이 출력됩니다.

## **3\. .gitignore 설정**

우리가 가상 환경을 구축하기 위해 만들었던 env 파일에는 민감한 정보가 있을 수 있습니다.

git허브에 push 되지 않도록 .gitignore에 설정하는 과정이 필요합니다.

아래와 같이 프로젝트 폴더에 .gitignore 파일을 생성합니다.

![image](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2F4OAjf%2FbtqDeIWG95T%2F5qNXd6uMKKxkWuEJrsbJKk%2Fimg.png)  

그리고 git에 push하지 않을 예외의 것들을 입력합니다.

![image](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2Fbg7z7b%2FbtqDeUvMnFr%2FHm7eJ38KL9UxpEQ0timsRk%2Fimg.png)  

env 파일과 .vscode는 push 할 필요가 없기 때문에 .gitignore에 입력해줬습니다.

## **4\. heroku에 필요한 파일들**

우리가 만든 프로젝트의 코드를 heroku에서 작동하게 하려면 조금의 준비가 필요합니다.

우선 프로젝트의 코드 실행에 필요한 모든 라이브러리 정보가 있어야 합니다.

> .py 파일

플라스크를 기반으로 작성한 .py 파일을 준비합니다.

```
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h3>Hi, Heroku</h3>'

if __name__ == '__main__':
    #app.run(debug=True, host='127.0.0.1')
    app.run()

```

> **requirements.txt** 파일을 생성  

아래 명령어를 터미널에 입력해서 **requirements.txt** 파일을 생성합니다.

`pip freeze > requirements.txt`

****requirements.txt**** 파일에는 아래와 같이 현재 프로젝트에 필요한 모든 라이브러리가 정리되어 있습니다.

![image](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FbN6dM9%2FbtqDf21fmLY%2FxQpj2WaZGxxWb2UXf3tRvK%2Fimg.png)  

> **Procfile 생성**

VScode에서 현재 프로젝트 폴더에 Procfile을 만들어 줍니다.

Procfile에는 heroku에서 돌아갈 서버에 대한 정의?를 내립니다.

gunicorn을 이용하기 때문에 `web: gunicorn (실행할 파이썬 파일):app과` 같이 입력합니다.

**ex) web: gunicorn text:app**

## **5\. Deploy**

이제 모든 준비를 마쳤으니 Depoy를 해봅시다.

우선 heroku에 로그인합니다

`>heroku login`

로그인이 되었다면 heroku프로젝트를 생성합니다.

`>heroku create 원하는 이름`

ex) heroku create example

heroku에서 서버를 돌리기 위해서는 github에 commit / push가 선행되어야 합니다.

VSCode 터미널 창에 순서대로 입력합니다.

`>git init (깃 디렉토리 생성)`

`>git add . (깃에 올릴 파일 선택)`

`>git commit -m 'first commit'`

이제 깃에 파일을 올리고 올린 파일들을 heroku에 master 합니다.

`>git push heroku master`

이제 배포는 끝났습니다.

서버를 실행하기 위해서 아래와 같이 입력합니다.

`>heroku ps:scale web=1`

확인

`>heroku ps`

아래 명령어로 페이지를 들어가 확인할 수 있습니다.

(heroku 웹 페이지의 프로젝트 대시보드에서도 페이지를 들어갈 수 있고 주소를 확인 할 수 있습니다.) 

`>heroku open `
