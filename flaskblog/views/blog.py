from flask import Blueprint, request, current_app, render_template

from flaskblog.models import Article, Recommend, Category, Tag

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/',methods = ["GET"])
def index():

    page = request.args.get('page',1,type=int)
    per_page = current_app.config["BLOG_POST_PER_PAGE"]

    pagination = Article.query.filter_by(state=1).order_by(Article.timestamp.desc()).paginate(page,per_page=per_page)
    recommends = Recommend.query.filter(Recommend.state ==1).order_by(Recommend.sn.desc()).all()
    articles = pagination.items

    return render_template('front/index.html', articles = articles, recommends = recommends, pagination = pagination)


@blog_bp.route('/article/<int:article_id>')
def article(article_id):
    all_article = Article.query.all()
    curr_article = None
    previous_index = 0
    next_index = 0
    previous_article = None
    next_article = None

    # 对于一个可迭代的（iterable）/可遍历的对象（如列表、字符串），
    # enumerate将其组成一个索引序列，利用它可以同时获得索引和值
    for index, article in enumerate(all_article):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_article) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1

        # 通过id判断当前记录;
        if article.id == int(article_id):
            curr_article = article
            previous_article = all_article[previous_index]
            next_article = all_article[next_index]
            break

    return render_template('front/detail.html',article = curr_article,article_first=previous_article,article_last=next_article)


@blog_bp.route('/category/<int:category_id>')
def category(category_id):
    """显示该分类下的文章列表"""
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page',1,type = int)
    per_page = current_app.config["BLOG_POST_PER_PAGE"]
    pagination = Article.query.with_parent(category).order_by(Article.timestamp.desc()).paginate(page,per_page)
    articles = pagination.items
    return render_template('front/category.html',category=category, pagination=pagination,articles = articles)

@blog_bp.route('/tag/<int:tag_id>')
def tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    page = request.args.get('page',1,type = int)
    per_page = current_app.config["BLOG_POST_PER_PAGE"]
    pagination = Article.query.with_parent(tag).order_by(Article.timestamp.desc()).paginate(page, per_page)
    articles = pagination.items
    return render_template('front/category.html', tag=tag, pagination=pagination, articles=articles)


@blog_bp.route('/about')
def about():
    return render_template('front/time.html')

@blog_bp.route('/achives')
def achives():
    return render_template('front/achives.html')


@blog_bp.route('/search',methods  = ["GET","POST"])
def search():
    # 搜索关键词
    if request.args.get("paramter"):
        paramter = request.args.get("paramter")
    else:
        paramter = request.form.get("paramter")

    print(paramter)
    page = request.args.get('page',1,type=int)
    pagination = Article.query.filter(Article.title.like('%%%s%%' % paramter)).order_by(Article.timestamp.desc()). \
        paginate(page, per_page=current_app.config['BLOG_POST_PER_PAGE'], error_out=False)
    articles = pagination.items
    return render_template('front/search.html',articles=articles,pagination=pagination,paramter = {"paramter":paramter})
