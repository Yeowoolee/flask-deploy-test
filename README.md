# flask-deploy-test
Test deployment of Flask projects to Heroku
  
go to heroku : https://roatest.herokuapp.com/
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


#### 사용 라이브러리

flask : flask프레임워크 사용하기 위해 import 했습니다.

flask\_pymongo : mongoDB를 사용하기 위해 import했습니다.

datetime : 현재 시간을 가져오기 위해 사용했습니다.

json : json을 dict로 변환, 클라이언트에 json형태로 data를 주기위해 사용했습니다.

#### MongoDB 모델링

```
    db_data = {'topic': '',
               'topic_list': {'info-title': '',
                              'info-body': '',
                              'creat_time': ''},
               {
                   'posts': [{'b_id': '',
                              'title': '',
                              'body': '',
                              'posted': '',
                              'date': '',
                              'likes': 0,
                              'comment': [{'c_id': '',
                                           'c_text': '',
                                           'c_posted': '',
                                           'c_posted_date': '',
                                           'more_comment': [{'mc_id': '',
                                                             'mc_text': '',
                                                             'mc_posted': '',
                                                             'mc_posted_date': ''}]
                                           }]
                              }]
               }
               }
```

작성된 DB는 mydata.json에 있습니다.

#### 필수 구현 API TEST

아래 테스트 url에 원하는 keyword, id 등을 넣고

host url 뒤에 붙여넣기해서 테스트 할 수 있습니다.

#### \-Pagination

#1페이지당 2개로 limit했습니다.

```
GET /r/{"keyword" : ""}/page/{"pagenum": ""}
```

-   Request

```
{"keyword" : "test"},{"pagenum": "3"}
```

-   Response

```
SUCCESS {

[

    {

        "_id": "test",

        "topic_list": {

            "info-title": "test",

            "info-body": "test",

            "creat_time": "2020/07/06 02:58"

        },

        "posts": {

            "b_id": 7,

            "title": "테스트 글입니다.",

            "body": "테스트",

            "posted": "jinho",

            "date": "2020/07/06 02:39",

            "likes": 0,

            "comment": []

        }

    },

    {

        "_id": "test",

        "topic_list": {

            "info-title": "test",

            "info-body": "test",

            "creat_time": "2020/07/06 02:58"

        },

        "posts": {

            "b_id": 8,

            "title": "테스트 글입니다.",

            "body": "테스트",

            "posted": "jinho",

            "date": "2020/07/06 02:39",

            "likes": 0,

            "comment": []

        }

    }

]

}
```

```
FAIL {'errmsg': '게시판이 존재하지 않습니다.'}
```

#### \-New

```
GET /r/{"keyword" : ""}/new
```

-   Request

```
{"keyword" : "test"}
```

-   Response

```
SUCCESS {

[
    {
        "_id": "test",
        "topic_list": {
            "info-title": "test",
            "info-body": "test",
            "creat_time": "2020/07/06 02:58"
        },
        "posts": {
            "b_id": 11,
            "title": "테스트",
            "body": "테스트",
            "posted": "ROA",
            "date": "2020/07/06 10:37",
            "likes": 0,
            "comment": []
        }
    },
    {
        "_id": "test",
        "topic_list": {
            "info-title": "test",
            "info-body": "test",
            "creat_time": "2020/07/06 02:58"
        },
        "posts": {
            "b_id": 10,
            "title": "테스트 글입니다.",
            "body": "테스트",
            "posted": "jinho",
            "date": "2020/07/06 02:39",
            "likes": 0,
            "comment": [
                {
                    "c_id": 0,
                    "c_body": "testbody",
                    "c_posted": "ROA",
                    "date": "2020/07/06 02:39",
                    "more_comment": []
                    .
                    .
                    .
                    
                }
            ]
        }
    },
    {
        "_id": "test",
        "topic_list": {
            "info-title": "test",
            "info-body": "test",
            "creat_time": "2020/07/06 02:58"
        },
        "posts": {
            "b_id": 9,
            "title": "테스트 글입니다.",
            "body": "테스트",
            "posted": "jinho",
            "date": "2020/07/06 02:39",
            "likes": 0,
            "comment": []
        }
    },
    {
        "_id": "test",
        "topic_list": {
            "info-title": "test",
            "info-body": "test",
            "creat_time": "2020/07/06 02:58"
        },
        "posts": {
            "b_id": 8,
            "title": "테스트 글입니다.",
            "body": "테스트",
            "posted": "jinho",
            "date": "2020/07/06 02:39",
            "likes": 0,
            "comment": []
        }
    }
    .
    .
    .
            
 ]
            
]
}
```

```
FAIL {'errmsg': '게시판이 존재하지 않습니다.'}
```

#### \-Old

```
GET /r/{"keyword" : ""}/old
```

-   Request

```
{"keyword" : "test"}
```

-   Response

```
SUCCESS {

[
    {
        "_id": "test",
        "topic_list": {
            "info-title": "test",
            "info-body": "test",
            "creat_time": "2020/07/06 02:58"
        },
        "posts": {
            "b_id": 0,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 0,
            "comment": [
                {
                    "c_id": 0,
                    "c_body": "ttt",
                    "c_posted": "jinho",
                    "date": "2020/07/06 02:39",
                    "more_comment": []
                }
                .
                .
                .
            ]
        }
    },
    {
        "_id": "test",
        "topic_list": {
            "info-title": "test",
            "info-body": "test",
            "creat_time": "2020/07/06 02:58"
        },
        "posts": {
            "b_id": 2,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 2,
            "comment": []
        }
    },
    {
        "_id": "test",
        "topic_list": {
            "info-title": "test",
            "info-body": "test",
            "creat_time": "2020/07/06 02:58"
        },
        "posts": {
            "b_id": 3,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 7,
            "comment": []
        }
    },
    {
        "_id": "test",
        "topic_list": {
            "info-title": "test",
            "info-body": "test",
            "creat_time": "2020/07/06 02:58"
        },
        "posts": {
            "b_id": 4,
            "title": "테스트",
            "body": "테스트",
            "posted": "ROA",
            "date": "2020/07/06 02:39",
            "likes": 0,
            "comment": []
        }
    }
    .
    .
    .
    
]
}
```

```
FAIL {'errmsg': '게시판이 존재하지 않습니다.'}
```

#### \-Likes Frequency

```
GET /r/{"keyword" : ""}/best
```

-   Request

```
{"keyword" : "test"}
```

-   Response

```
SUCCESS {

[
    {
        "_id": "test",
        "topic_list": {
            "info-title": "test",
            "info-body": "test",
            "creat_time": "2020/07/06 02:58"
        },
        "posts": {
            "b_id": 3,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 7,
            "comment": []
        }
    },
    {
        "_id": "test",
        "topic_list": {
            "info-title": "test",
            "info-body": "test",
            "creat_time": "2020/07/06 02:58"
        },
        "posts": {
            "b_id": 5,
            "title": "테스트 글입니다.",
            "body": "테스트",
            "posted": "ROA",
            "date": "2020/07/06 02:39",
            "likes": 3,
            "comment": []
        }
    },
    {
        "_id": "test",
        "topic_list": {
            "info-title": "test",
            "info-body": "test",
            "creat_time": "2020/07/06 02:58"
        },
        "posts": {
            "b_id": 2,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 2,
            "comment": []
        }
    }
    .
    .
    .
    
]
}
```

```
FAIL {'errmsg': '게시판이 존재하지 않습니다.'}
```

#### 게시판 제목 검색

```
GET /r/{"keyword" : ""}/search/{"text" : ""}
```

-   Request

```
{"keyword" : "test"},{"text": "tt"}
```

-   Response

```
SUCCESS {
{
    "searching_post": [
        {
            "b_id": 0,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 0,
            "comment": [
                {
                    "c_id": 0,
                    "c_body": "ttt",
                    "c_posted": "jinho",
                    "date": "2020/07/06 02:39",
                    "more_comment": []
                },
                {
                    "c_id": 1,
                    "c_body": "ttt",
                    "c_posted": "jinho",
                    "date": "2020/07/06 02:39",
                    "more_comment": []
                },
                {
                    "c_id": 2,
                    "c_body": "ttt",
                    "c_posted": "jinho",
                    "date": "2020/07/06 02:39",
                    "more_comment": []
                },
                {
                    "c_id": 3,
                    "c_body": "ttt",
                    "c_posted": "ROA",
                    "date": "2020/07/06 02:39",
                    "more_comment": []
                },
                {
                    "c_id": 4,
                    "c_body": "ttt",
                    "c_posted": "ROA",
                    "date": "2020/07/06 02:39",
                    "more_comment": []
                },
                {
                    "c_id": 5,
                    "c_body": "ttt",
                    "c_posted": "ROA",
                    "date": "2020/07/06 02:39",
                    "more_comment": []
                }
            ]
        },
        {
            "b_id": 2,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 2,
            "comment": []
        },
        {
            "b_id": 3,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 7,
            "comment": []
        }
    ]
}
}
```

```
FAIL {'errmsg': '게시판이 존재하지 않습니다.'}
```

#### 게시글 (CRUD)

\-Creat

```
POST /r/{"keyword" : ""}/{"cmd": "create", "title":"", "body":""}
```

-   Request

{"keyword" : "test"}

```
{"keyword" : "test"},{"cmd": "create", "title":"tt", "body":"tt"}
```

-   Response

```
SUCCESS {
	{
    "b_id": 0,
    "title": "tt",
    "body": "tt",
    "posted": "ROA",
    "date": "2020/07/06 03:04",
    "likes": 0,
    "comment": []
}
}

```

```
FAIL {'errmsg': '게시글 CRUD중 오류가 발생했습니다.'}
```

\-Read

```
GET /r/{"keyword" : ""}/{"cmd": "read", "b_id": ""}
```

-   Request

```
{"keyword" : "test"}/{"cmd": "read", "b_id": "8"}
```

-   Response

```
SUCCESS {
{
    "_id": "test",
    "posts": [
        {
            "b_id": 8,
            "title": "테스트 글입니다.",
            "body": "테스트",
            "posted": "jinho",
            "date": "2020/07/06 02:39",
            "likes": 0,
            "comment": []
        }
    ]
}
}
```

```
FAIL {'errmsg': '게시글 CRUD중 오류가 발생했습니다.'}
```

\-Update

```
PUT /r/{"keyword" : ""}/{"cmd": "update", "b_id": "", "title":"", "body":""}
```

-   Request

{"keyword" : "test"}

```
{"keyword" : "tset"},{"cmd": "update", "b_id": "4", "title":"update", "body":"update"}
```

-   Response

```
SUCCESS {
{
    "_id": "test",
    "posts": [
        {
            "b_id": 4,
            "title": "update",
            "body": "update",
            "posted": "ROA",
            "date": "2020/07/06 02:39",
            "likes": 0,
            "comment": []
        }
    ]
}
}
```

```
FAIL {"errmsg": "아이디 불일치"}
```

\-Delete

```
DELETE /r/{"keyword" : ""}/{"cmd": "delete", "b_id": ""}
```

-   Request

```
{"keyword" : "test"},{"cmd": "delete", "b_id": "4"}
```

-   Response

```
SUCCESS {
{
    "_id": "test",
    "topic_list": {
        "info-title": "test",
        "info-body": "test",
        "creat_time": "2020/07/06 02:58"
    },
    "posts": [
        {
            "b_id": 0,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 0,
            "comment": [
                {
                    "c_id": 0,
                    "c_body": "ttt",
                    "c_posted": "jinho",
                    "date": "2020/07/06 02:39",
                    "more_comment": []
                }
                .
                .
                .
            ]
        },
        {
            "b_id": 2,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 2,
            "comment": []
        },
        {
            "b_id": 3,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 7,
            "comment": []
        },
        {
            "b_id": 5,
            "title": "테스트 글입니다.",
            "body": "테스트",
            "posted": "ROA",
            "date": "2020/07/06 02:39",
            "likes": 3,
            "comment": []
        }
        .
        .
        .
    ]
}
}
```

```
FAIL {"errmsg": "아이디 불일치"}
```

#### 게시글 좋아요

```
PUT /r/{"keyword" : ""}/{"cmd": "like", "b_id": ""}
```

-   Request

```
{"keyword" : "test"},{"cmd": "like", "b_id": "3"}
```

-   Response

```
SUCCESS {
	{
    "_id": "test",
    "posts": [
        {
            "b_id": 3,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 8,
            "comment": []
        }
    ]
}
}
```

```
FAIL {'errmsg': '게시판이 존재하지 않습니다.'}
```

#### 게시글 링크 공유

```
GET /r/{"keyword" : ""}/{"cmd": "link", "b_id": ""}
```

-   Request

```
{"keyword" : "test"},{"cmd": "link", "b_id": "3"}
```

-   Response

```
SUCCESS {
	#json변환과정에서 err
	{\"url\": \"https://roatest.herokuapp.com/r/{\\\"keyword\\\" : \\\"tset\\\"}/{\\\"cmd\\\": \\\"read\\\", \\\"b_id\\\": \\\"3\\\"}\"}
}
```

```
FAIL {'errmsg': '게시판이 존재하지 않습니다.'}
```

#### 댓글 (CRUD)

\-Creat

```
POST /r/{"keyword" : ""}/comment/{"cmd": "create","b_id": "","body":""}
```

-   Request

```
{"keyword" : "test"},{"cmd": "create","b_id": "3","body":"commet"}
```

-   Response

```
SUCCESS {
  {
      "c_id": 0,
      "c_body": "comment",
      "c_posted": "ROA",
      "date": "2020/07/06 10:56",
      "more_comment": []
  }
}
```

```
FAIL {'errmsg': '댓글 CRUD중 오류가 발생했습니다.'}
```

\-Read

```
GET /r/{"keyword" : ""}/comment/{"cmd": "read", "b_id": "","c_id": ""}
```

-   Request

```
{"keyword" : "test"}/comment/{"cmd": "read", "b_id": "3","c_id": "0"}
```

-   Response

```
SUCCESS {
  {
      "c_id": 0,
      "c_body": "comment",
      "c_posted": "ROA",
      "date": "2020/07/06 10:56",
      "more_comment": []
  }
}
```

```
FAIL {'errmsg': '댓글 CRUD중 오류가 발생했습니다.'}
```

\-Update

```
PUT /r/{"keyword" : ""}/comment/{"cmd": "update", "b_id": "","c_id": "","body":""}
```

-   Request

```
{"keyword" : "tset"},{"cmd": "update", "b_id": "3","c_id": "0","body":"updatecomment"}
```

-   Response

```
SUCCESS {
	SUCCESS {
  {
      "c_id": 0,
      "c_body": "updatecomment",
      "c_posted": "ROA",
      "date": "2020/07/06 10:56",
      "more_comment": []
  }
}
}
```

```
FAIL {'errmsg': '아이디 불일치'}
```

\-Delete

```
DELETE /r/{"keyword" : ""}/comment/{"cmd": "delete", "b_id": "","c_id": ""}
```

-   Request

```
{"keyword" : "test"},{"cmd": "delete", "b_id": "3","c_id": "0"}
```

-   Response

```
SUCCESS {
	{
    "_id": "test",
    "posts": [
        {
            "b_id": 3,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 8,
            "comment": []
        }
    ]
}
}
```

```
FAIL {"errmsg": "아이디 불일치"}
```

#### 게시판 생성

```
POST /create/{"topic" : "", "title" : "", "body": ""}
```

-   Request

```
{"topic" : "createTest", "title" : "tsettitle", "body": "testbody"}
```

-   Response

```
SUCCESS {
	{
    "_id": "createTest",
    "topic_list": {
        "info-title": "tsettitle",
        "info-body": "testbody",
        "creat_time": "2020/07/06 10:56"
    },
    "posts": []
}
}
```

```
FAIL {'errmsg': '이미 존재하는 게시판입니다.'}
```

#### 게시판 전체 검색

```
GET /r/{"keyword" : ""}
```

-   Request

```
{"keyword" : "test"}
```

-   Response

```
SUCCESS {
{
    "_id": "test",
    "topic_list": {
        "info-title": "test",
        "info-body": "test",
        "creat_time": "2020/07/06 02:58"
    },
    "posts": [
        {
            "b_id": 0,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 0,
            "comment": [
                {
                    "c_id": 0,
                    "c_body": "ttt",
                    "c_posted": "jinho",
                    "date": "2020/07/06 02:39",
                    "more_comment": []
                }
                .
                .
                .
            ]
        },
        {
            "b_id": 2,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 2,
            "comment": []
        },
        {
            "b_id": 3,
            "title": "tt",
            "body": "tt",
            "posted": "ROA",
            "date": "2020/07/06 03:04",
            "likes": 8,
            "comment": []
        },
        {
            "b_id": 5,
            "title": "테스트 글입니다.",
            "body": "테스트",
            "posted": "ROA",
            "date": "2020/07/06 02:39",
            "likes": 3,
            "comment": []
        },
        {
            "b_id": 6,
            "title": "테스트 글입니다.",
            "body": "테스트",
            "posted": "ROA",
            "date": "2020/07/06 02:39",
            "likes": 0,
            "comment": []
        }
        .
        .
        .
}
}
```

```
FAIL {'errmsg': '게시판이 존재하지 않습니다.'}
```

```
#-------------------------------예외처리------------------------------#


@app.route('/wrongid')
def wrongid():
    errmsg = {'errmsg': '아이디 불일치'}
    return json.dumps(errmsg, ensure_ascii=False)


@app.route('/notfind')
def notfind():
    errmsg = {'errmsg': '게시판이 존재하지 않습니다.'}
    return json.dumps(errmsg, ensure_ascii=False)


@app.route('/existBoard')
def existBoard():
    errmsg = {'errmsg': '이미 존재하는 게시판입니다.'}
    return json.dumps(errmsg, ensure_ascii=False)


@app.route('/cmderr')
def cmderr():
    errmsg = {'errmsg': '게시글 CRUD중 오류가 발생했습니다.'}
    return json.dumps(errmsg, ensure_ascii=False)


@app.route('/commentcmderr')
def commentcmderr():
    errmsg = {'errmsg': '댓글 CRUD중 오류가 발생했습니다.'}
    return json.dumps(errmsg, ensure_ascii=False)


@app.errorhandler(404)
def page_not_found(e):
    errmsg = {'errmsg': '404 ERROR'}
    return json.dumps(errmsg, ensure_ascii=False), 400


@app.errorhandler(500)
def internal_server_error(e):
    errmsg = {'errmsg': '500 ERROR'}
    return json.dumps(errmsg, ensure_ascii=False), 500
```

