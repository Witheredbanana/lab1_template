import random
from flask import Flask, render_template
from faker import Faker

# Инициализация генератора фейковых данных
fake = Faker()

# Создание экземпляра Flask-приложения
app = Flask(__name__)
application = app

# Список идентификаторов изображений для постов
images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

# Функция для генерации комментариев и ответов на них
def generate_comments(replies=True):
    """
    Генерирует случайное количество комментариев (от 1 до 3)
    
    Args:
        replies (bool): Флаг, указывающий, нужно ли генерировать ответы на комментарии
        
    Returns:
        list: Список словарей с комментариями
    """
    comments = []
    for i in range(random.randint(1, 3)):
        comment = { 'author': fake.name(), 'text': fake.text() }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

# Функция для генерации данных поста
def generate_post(i):
    """
    Генерирует данные для одного поста
    
    Args:
        i (int): Индекс поста, используется для выбора изображения
        
    Returns:
        dict: Словарь с данными поста
    """
    return {
        'title': fake.sentence(nb_words=random.randint(3, 6)),  # Случайный заголовок из 3-6 слов
        'text': fake.paragraph(nb_sentences=100),               # Текст поста из 100 предложений
        'author': fake.name(),                                  # Случайное имя автора
        'date': fake.date_time_between(start_date='-2y', end_date='now'),  # Случайная дата за последние 2 года
        'image_id': f'{images_ids[i]}.jpg',                     # Изображение для поста
        'comments': generate_comments()                         # Комментарии к посту
    }

# Генерация списка постов и сортировка по дате (от новых к старым)
posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

# Маршрут для главной страницы
@app.route('/')
def index():
    """Отображает главную страницу с заданием"""
    return render_template('index.html')

# Маршрут для страницы со списком постов
@app.route('/posts')
def posts():
    """Отображает страницу со списком всех постов"""
    return render_template('posts.html', title='Посты', posts=posts_list)

# Маршрут для страницы отдельного поста
@app.route('/posts/<int:index>')
def post(index):
    """
    Отображает страницу с отдельным постом
    
    Args:
        index (int): Индекс поста в списке posts_list
    """
    p = posts_list[index]
    return render_template('post.html', title=p['title'], post=p)

# Маршрут для страницы "Об авторе"
@app.route('/about')
def about():
    """Отображает страницу с информацией об авторе"""
    return render_template('about.html', title='Об авторе')
