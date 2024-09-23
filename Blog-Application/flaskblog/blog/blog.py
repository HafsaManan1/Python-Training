from flask import Blueprint, render_template, request, flash, redirect, url_for
from flaskblog import db, mail, ckeditor
from flaskblog.blog.forms import CommentForm, PostForm, SearchForm
from flaskblog.models import Comments, Posts
from flask_login import login_required, current_user
from flask_mail import Message

blog = Blueprint("blog",__name__)

@blog.route('/add-post', methods = ['GET','POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Login in order to comment","info")
            return redirect(url_for('author.login'))
        poster = current_user.id
        post = Posts(title=form.title.data, poster_id = poster, content = form.content.data)
        form.title.data = ''
        form.content.data = ''
        db.session.add(post)
        db.session.commit()
        flash("Blog submitted successfully","success")
        return redirect(url_for('blog.posts'))

    return render_template('add_post.html', form = form)

@blog.route('/posts')
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=6)
    return render_template('posts.html',posts=posts)

@blog.route('/post/<int:id>',methods = ['GET','POST'])
def post(id):
    post = Posts.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Login in order to comment","info")
            return redirect(url_for('author.login'))
        email = post.poster.email
        body = f"""Hello,
        You have received a new comment on your post!
        ---
        "{form.content.data}"
        ---
        We thought you’d like to stay updated with the latest interactions on your content. Feel free to check out the full discussion or respond directly to keep the conversation going.

        Thank you for being an active part of our community!
        """
        comment = Comments(content=form.content.data, commentor_id = current_user.id, post_id = id)
        form.content.data = ''
        db.session.add(comment)
        db.session.commit()
        msg = Message('New Comment', recipients = [email],body = body)
        mail.send(msg)
        flash("Comment added successfully", "success")
        return redirect(url_for('blog.post', id=id))
    comments = Comments.query.filter_by(post_id=id).order_by(Comments.date_posted.desc()).all() 
    return render_template('post.html', post=post, form=form,comments = comments)

@blog.route('/posts/edit/<int:id>', methods = ['GET','POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Post updated successfully ", "success")
        return redirect(url_for('blog.post',id = post.id))
    if current_user.id == post.poster_id:
        form.title.data = post.title
        form.content.data = post.content
        return render_template('edit_post.html', form = form)
    else:
        flash("You arent authorized to edit this post", "warning")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('edit_post.html', form=form)

@blog.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id: 
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post deleted successfully","success")
            page = request.args.get('page', 1, type=int)
            posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=6)
            return render_template('posts.html',posts=posts)

        except:
            flash("There was a problem in deleting the post","error")
            page = request.args.get('page', 1, type=int)
            posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=6)
            return render_template('posts.html',posts=posts)
    else:
        flash("You arent authorized to delete that post","warning")
        page = request.args.get('page', 1, type=int)
        posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=6)
        return render_template('posts.html',posts=posts)
    
@blog.context_processor
def base():
    form = SearchForm()
    return dict(form = form)

@blog.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search_term = form.searched.data.strip() 
        if search_term:
            posts = Posts.query.filter(Posts.content.like(f'%{search_term}%')).order_by(Posts.title).all()
            return render_template("search.html", form=form, searched=search_term, posts=posts)
        else:
            flash("Please enter a search term","warning")
            return redirect(url_for('blog.posts'))
    return redirect(url_for('blog.posts'))
