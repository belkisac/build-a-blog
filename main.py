from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyPassword@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'gsr345456gfdfgdfGDFGHDF'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(256))

    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def blog_display():

    if request.args != {}:
        post_id = request.args.get('id', '')
        post = Blog.query.get(post_id)
        title = post.title
        body = post.body
        return render_template('solo.html',title=title,body=body)
    else:
        posts = Blog.query.all()
        return render_template('blog.html',posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title = ''
    body = ''
    errors = False

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == '':
            flash("Please enter a title", "title_error")
            title = ''
            errors = True
        else:
            title = title
        if body == '':
            flash("Please enter the body of your post", "body_error")
            body = ''
            errors = True
        else:
            body = body
        if errors:
            return render_template('newpost.html',title=title,body=body)
        else:
            new_post = Blog(title,body)
            db.session.add(new_post)
            db.session.commit()
            post = Blog.query.filter_by(id=new_post.id).first()
            post_id = post.id
            return redirect(url_for('.blog_display', id=post_id))
    
    return render_template('newpost.html')


if __name__ == '__main__':
    app.run()