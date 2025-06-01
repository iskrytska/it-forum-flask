import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Моделі ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# --- Переклади ---
translations = {
    'uk': {
        'welcome': 'Ласкаво просимо на IT Форум!',
        'description': 'Обговорюйте ідеї, проєкти та допомагайте одне одному.',
        'posts': 'Перейти до постів',
        'home_title': 'Головна сторінка',
        'login': 'Увійти',
        'logout': 'Вийти',
        'register': 'Реєстрація',
        'username': 'Ім\'я користувача',
        'password': 'Пароль',
        'submit': 'Надіслати',
        'invalid_credentials': 'Неправильний логін або пароль',
        'user_exists': 'Користувач з таким іменем вже існує',
        'register_success': 'Реєстрація успішна. Тепер увійдіть.',
        'posts_page': 'Сторінка постів',
        'welcome_user': 'Вітаємо,',
        'add_post': 'Додати пост',
        'post_title': 'Заголовок посту',
        'post_content': 'Текст посту',
        'submit': 'Опублікувати',
        'comments': 'Коментарі',
        'add_comment': 'Додати коментар',
        'comment_placeholder': 'Ваш коментар...',
        'login': 'Увійти',
        'to_comment': 'щоб залишити коментар',
        'no_comments_yet': 'Поки що немає коментарів',
    },
    'en': {
        'welcome': 'Welcome to IT Forum!',
        'description': 'Discuss ideas, projects, and help each other.',
        'posts': 'Go to posts',
        'home_title': 'Home page',
        'login': 'Login',
        'logout': 'Logout',
        'register': 'Register',
        'username': 'Username',
        'password': 'Password',
        'submit': 'Submit',
        'invalid_credentials': 'Invalid username or password',
        'user_exists': 'User with this username already exists',
        'register_success': 'Registration successful. Please login now.',
        'posts_page': 'Posts Page',
        'welcome_user': 'Welcome,',
        'add_post': 'Add Post',
        'post_title': 'Post Title',
        'post_content': 'Post Content',
        'submit': 'Submit',
        'comments': 'Comments',
        'add_comment': 'Add comment',
        'comment_placeholder': 'Your comment...',
        'login': 'Login',
        'to_comment': 'to leave a comment',
        'no_comments_yet': 'No comments yet',
    }
}

def get_locale():
    lang = session.get('lang')
    if lang not in translations:
        lang = 'uk'
    return lang

def t(key):
    lang = get_locale()
    return translations.get(lang, {}).get(key, key)

# --- Роут для зміни мови ---
@app.route('/change_lang/<lang_code>')
def change_lang(lang_code):
    if lang_code in translations:
        session['lang'] = lang_code
    return redirect(request.referrer or url_for('index'))

# --- Головна сторінка ---
@app.route('/')
def index():
    return render_template('index.html', t=t, lang=get_locale(), user=session.get('username'))

# --- Сторінка постів ---
@app.route('/posts')
def posts():
    all_posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('posts.html', posts=all_posts, t=t, lang=get_locale(), user=session.get('username'))

# --- Додати пост ---
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        if title and content:
            new_post = Post(title=title, content=content, author=session['username'])
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('posts'))
    return render_template('add_post.html', t=t, lang=get_locale(), user=session.get('username'))

# --- Перегляд посту + додавання коментаря ---
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST' and 'username' in session:
        content = request.form['content'].strip()
        if content:
            user = User.query.filter_by(username=session['username']).first()
            new_comment = Comment(content=content, user_id=user.id, post_id=post.id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('post_detail', post_id=post.id))
    return render_template('post_detail.html', post=post, t=t, lang=get_locale(), user=session.get('username'))



# --- Реєстрація ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash(t('user_exists'), 'error')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash(t('register_success'), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', t=t, lang=get_locale())

# --- Логін ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            flash(f"{t('welcome_user')} {user.username}!", 'success')
            return redirect(url_for('index'))
        flash(t('invalid_credentials'), 'error')
        return redirect(url_for('login'))
    return render_template('login.html', t=t, lang=get_locale())

# --- Логаут ---
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
