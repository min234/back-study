from flask import Flask
from flask import request,redirect

app = Flask(__name__)

nextId = 4
topics = [
    {"id":1,"title":"html","body":"html is..."},
    {"id":2,"title":"css","body":"css is..."},
    {"id":3,"title":"javascript","body":"javascript is..."}
]

def template(contents, content, id=None):
    contextUi = ''

    if id is  None:  # 여기서 None 대신에 id is not None으로 수정
        contextUi = f'''
            <li><a href="/update/{id}/">update</a></li>
        '''

    return f'''<!doctype html>
    
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            <h2>{content}</h2>
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUi}
            </ul>
        </body>
    </html>
    '''

def getContents():
    to = ''
    for topic in topics:
        to = to + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a> </li>'
    return to

@app.route('/')
def index():
    return template(getContents(),'<h2>welcome</h2>Hello,WEB')

@app.route('/read/<int:id>/')
def read(id): 
    title = ''
    body = ''
    for topic in topics:
        if id == str(topic["id"]):
            title = topic["title"]
            body = topic["body"]
            break
    print(title,body)
    return template(getContents(),f'<h2>{title}</h2>{body}')
@app.route('/create/',methods=['GET','POST'])
def create():
    if(request.method == "GET"):

        content = '''
        <form action="/create/" method = "POST">
            <input type ="text" name="title" placeholder="title">
            <p><textarea placeholder ="body" name = "body"></textarea></p>
            <p><input type="submit" calue="create"></p>
        </form>
    '''
        
        return template(getContents(),content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        newTopic ={'id':nextId,'title':title,'body':body}
        topics.append(newTopic)
        url = '/read/' + str(nextId)
        nextId = nextId + 1 
        return redirect(url)
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        title = ''
        body = ''
        for topic in topics:
            if id == topic["id"]:
                title = topic["title"]
                body = topic["body"]
                break

        content = f'''
            <form action="/update/{id}/" method="POST">
                <input type="text" name="title" placeholder="title" value="{title}">
                <p><textarea placeholder="body" name="body">{body}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''

        return template(getContents(), content, id)

    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/' + str(id)
        return redirect(url)

# 아래의 app.run()을 확인해 주세요. 이 부분도 코드 블록 안에 포함되어야 합니다.
app.run(debug=True)