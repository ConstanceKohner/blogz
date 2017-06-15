from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))
    deleted = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.deleted = False

@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')


@app.route('/blog', methods=['POST', 'GET'])
def blogreader():

    if request.method == 'POST':
        blog_name = request.form['title']
        blog_content = request.form['body']
        new_blog = Blog(blog_name, blog_content)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.filter_by(deleted=False).all()
    return render_template('blogwriter.html', blogs=blogs)


if __name__ == '__main__':
    app.run()