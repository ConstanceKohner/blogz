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
    return render_template('base.html', title="Navigation")


@app.route('/blog', methods=['GET'])
def blogreader():
    blogs = Blog.query.filter_by(deleted=False).all()
    return render_template('blogreader.html', title="All Blog Posts", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def blogwriter():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        if blog_title == '':
            title_error = 'You must enter a title for your blog post.'
        else:
            title_error = ''
        if blog_body == '':
            body_error = 'You must enter content for your blog post.'
        else:
            body_error = ''
        if title_error == '' and body_error == '':
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog")
        else:
            return render_template('blogwriter.html', title="Create New Blog Post", blog_title=blog_title, blog_body=blog_body, title_error=title_error, body_error=body_error)
        

    blogs = Blog.query.filter_by(deleted=False).all()
    return render_template('blogwriter.html', title="Create New Blog Post", blogs=blogs)


if __name__ == '__main__':
    app.run()