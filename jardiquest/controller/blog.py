from jardiquest.controller import app


@app.get('/blog')
def blog():
    """Print the blog page"""
    from jardiquest.model.path.blog_model import render_blog
    return render_blog()


@app.post('/blog')
def add_blog():
    """Post a new message on the blog page"""    
    from jardiquest.model.path.blog_model import add_new_message
    return add_new_message()


