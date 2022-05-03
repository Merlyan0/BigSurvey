# flask
import flask
from flask import Flask, render_template, make_response, request
from werkzeug import Response
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

# форма добавления опроса
from add_form import AddingSurveyForm

# БД
from data import db_session
from data.attempts import Attempt
from data.questions import Question
from data.surveys import Survey

# дополнительно
import secrets
import string
from typing import Union

app = Flask(__name__)  # приложение Flask
app.config['SECRET_KEY'] = 'SS2c7HBWzyJvmA8y5gW5'  # секретный ключ (рекомендуется ввести свой)
db_session.global_init('main.db')  # инициализация базы данных


@app.route('/')
def index() -> str:
    """
    Главная страница.
    """
    return render_template('index.html')


@app.route('/survey/<survey_id>', methods=['GET', 'POST'])
def get_survey(survey_id) -> Union[str, Response]:
    """
    Получение опроса по конкретному id с возможностью его прохождения.
    """
    db_sess = db_session.create_session()

    if not db_sess.query(Survey).filter_by(id=survey_id).all() \
            and not db_sess.query(Survey).filter_by(private_url=survey_id).all():  # если опрос с таким id не найден
        return redirect('/')

    if db_sess.query(Survey).filter_by(private_url=survey_id).first():
        survey = db_sess.query(Survey).filter_by(private_url=survey_id).first()  # получение опроса в БД
    else:
        survey = db_sess.query(Survey).filter_by(id=survey_id).first()  # получение опроса в БД

    if request.method == 'POST':  # если пользователь прошел опрос (пришел метод POST)
        answers = list()  # список ответов пользователя

        for i in range(1, len(db_sess.query(Question).filter_by(survey=survey.id).all()) + 1):
            answers.append(request.form.get(f'radio{i}'))

        # Создание попытки в БД
        attempt = Attempt()
        attempt.name = request.form.get('name')
        attempt.answers = ' / '.join(answers)
        attempt.survey = survey.id
        db_sess.add(attempt)
        db_sess.commit()

        db_sess_new = db_session.create_session()
        attempt_id = str(db_sess_new.query(Attempt).filter_by(name=request.form.get('name'),
                                                              answers=' / '.join(answers),
                                                              survey=survey.id).first().id)

        # Создание cookie о пройденном опросе с id необходимой попытки
        res = make_response(redirect(f'/survey/{survey.id}/thanks'))
        res.set_cookie(f'survey{survey.id}_finished', f'{attempt_id}', max_age=60 * 60 * 24 * 365)
        return res

    if survey.private and survey_id != survey.private_url:  # если опрос приватный
        return render_template('survey.html', error='Данного опроса не существует или он является приватным.')

    elif request.cookies.get(f'survey{survey.id}_finished'):  # если опрос уже пройден
        return redirect(f'/survey/{survey.id}/thanks')

    else:  # проверки пройдены, отрисовка опроса
        questions = db_sess.query(Question).filter_by(survey=survey.id).all()
        return render_template('survey.html', survey=survey, questions=questions, error='')


@app.route('/add_survey', methods=['GET', 'POST'])
def add_survey() -> Union[str, Response]:
    """
    Добавить опрос.
    """
    form = AddingSurveyForm()  # инициализация формы

    if form.validate_on_submit():  # если пройдена валидация
        db_sess = db_session.create_session()

        # Создание опроса в БД
        survey = Survey()
        survey.title = form.title.data
        survey.description = form.description.data
        survey.ask_name = form.ask_name.data
        survey.private = form.private.data
        survey.set_password(form.password.data)

        # Генерация приватного url
        letters_and_digits = string.ascii_letters + string.digits
        crypt_rand_string = ''.join(secrets.choice(letters_and_digits) for _ in range(10))
        survey.private_url = crypt_rand_string

        db_sess.add(survey)
        db_sess.commit()

        # перенаправление на редактирование только что созданной формы
        return redirect(f'/survey/{db_sess.query(Survey).filter_by(title=form.title.data).first().id}/edit')

    return render_template('adding.html', form=form)


@app.route('/survey/<survey_id>/edit/login', methods=['GET', 'POST'])
def login_to_edit(survey_id) -> Union[str, Response]:
    """
    Страница авторизации для редактирования опроса.
    """
    db_sess = db_session.create_session()

    if not db_sess.query(Survey).filter_by(id=survey_id).all():  # если опроса с таким id нет
        return redirect('/')

    if request.cookies.get(f'survey{survey_id}'):  # если пользователь уже ввёл пароль
        return redirect(f'/survey/{survey_id}/edit')

    if flask.request.method == 'POST':  # запрос на вход (пришел метод POST)
        original_password = db_sess.query(Survey).filter_by(id=survey_id).first().hashed_password

        if check_password_hash(original_password, request.form.get('password')):  # если введен верный пароль

            # создание cookie на время работы браузера, чтобы не вводить пароль несколько раз
            res = make_response(redirect(f'/survey/{survey_id}/edit'))
            res.set_cookie(f'survey{survey_id}', 'yes', max_age=None)
            return res

        else:  # если введен неверный пароль
            return render_template('login.html', error='Неправильный пароль')

    return render_template('login.html', error='')


@app.route('/survey/<survey_id>/edit', methods=['GET', 'POST'])
def edit_survey(survey_id) -> Union[str, Response]:
    """
    Редактировать опрос.
    """
    db_sess = db_session.create_session()

    if db_sess.query(Survey).filter_by(private_url=survey_id).all():  # если ссылка состоит из приватного url
        return redirect(f'/survey/{db_sess.query(Survey).filter_by(private_url=survey_id).first().id}/edit')

    if not db_sess.query(Survey).filter_by(id=survey_id).all():  # если запрашиваемого опроса нет
        return redirect('/')

    if not request.cookies.get(f'survey{survey_id}'):  # если не введён пароль для редактирования опроса
        return redirect(f'/survey/{survey_id}/edit/login')

    survey = db_sess.query(Survey).filter_by(id=survey_id).first()
    message = ''

    if flask.request.method == 'POST':  # если пришел запрос на изменение настроек

        if request.form.get('save_settings') == 'Сохранить настройки':  # кнопка "Сохранить настройки" (Вкладка "Общее")
            db_sess = db_session.create_session()

            survey = db_sess.query(Survey).filter_by(id=survey_id).first()
            on_off = {'on': True, 'None': False}

            survey.ask_name = on_off[str(request.form.get('ask_name'))]
            survey.private = on_off[str(request.form.get('private'))]

            db_sess.commit()

        elif request.form.get('del') == 'Удалить':  # кнопка "Удалить" (Вкладка "Все вопросы")
            db_sess = db_session.create_session()

            all_questions = db_sess.query(Question).filter_by(survey=survey_id).all()

            if 0 < int(request.form.get('del_id')) <= len(all_questions):
                del_id = all_questions[int(request.form.get('del_id')) - 1].id
                db_sess.query(Question).filter_by(id=del_id).delete()
                db_sess.commit()

                return render_template('edit.html',
                                       survey=survey,
                                       questions=db_sess.query(Question).filter_by(survey=survey_id).all(),
                                       attempts=db_sess.query(Attempt).filter_by(survey=survey_id).all(),
                                       message='Вопрос удалён успешно.')

        elif request.form.get('save') == 'Сохранить':  # кнопка "Сохранить" (Вкладка "Добавить вопрос")
            db_sess = db_session.create_session()

            temp = str([request.form.get('var')]).rstrip("']").lstrip("['").replace('\\r\\n', ' / ')

            if ''.join(list(filter(lambda a: a[-1] == '*', temp.split(' / ')))).rstrip('*') == '':
                right = ''
            else:
                right = ''.join(list(filter(lambda a: a[-1] == '*', temp.split(' / ')))).rstrip('*')

            # Создание нового вопроса в БД
            question = Question()
            question.title = request.form.get('title')
            question.right = right
            question.var = temp.replace('*', '')
            question.survey = survey_id

            db_sess.add(question)
            db_sess.commit()

            message = 'Вопрос успешно сохранён.'

        elif request.form.get('play') == 'Воспроизвести':  # кнопка "Воспроизвести" (Вкладка "Попытки")
            db_sess = db_session.create_session()
            attempt_id_old = int(request.form.get('attempt_id'))

            if attempt_id_old - 1 > len(db_sess.query(Attempt).filter_by(survey=survey_id).all()):
                return render_template('edit.html',
                                       survey=survey,
                                       questions=db_sess.query(Question).filter_by(survey=survey_id).all(),
                                       attempts=db_sess.query(Attempt).filter_by(survey=survey_id).all(),
                                       message='Ошибка воспроизведения попытки. Неверное число.')

            else:
                user_attempt = db_sess.query(Attempt).filter_by(survey=survey_id).all()[attempt_id_old - 1]
                return render_template('edit.html',
                                       survey=survey,
                                       questions=db_sess.query(Question).filter_by(survey=survey_id).all(),
                                       attempts=db_sess.query(Attempt).filter_by(survey=survey_id).all(),
                                       user_attempt=user_attempt,
                                       message='Попытка воспроизведена: она находится во вкладке "Попытки".')

    return render_template('edit.html',
                           survey=survey,
                           questions=db_sess.query(Question).filter_by(survey=survey_id).all(),
                           attempts=db_sess.query(Attempt).filter_by(survey=survey_id).all(),
                           message=message)


@app.route('/survey/<survey_id>/thanks')
def thanks_for_participating(survey_id) -> Union[str, Response]:
    """
    Вывести надпись об окончании опроса.
    """
    db_sess = db_session.create_session()

    if not request.cookies.get(f'survey{survey_id}_finished'):  # если опрос еще не пройден
        return redirect(f'/survey/{survey_id}')

    # получение вопросов и попытки пользователя в БД
    attempt = db_sess.query(Attempt).filter_by(id=request.cookies.get(f'survey{survey_id}_finished')).first()
    questions = db_sess.query(Question).filter_by(survey=attempt.survey).all()

    return render_template('thanks.html', questions=questions, user_attempt=attempt)


@app.route('/catalog')
def catalog() -> Union[str, Response]:
    """
    Вывести каталог публичных опросов.
    """
    db_sess = db_session.create_session()
    return render_template('catalog.html', surveys=list(reversed(db_sess.query(Survey).filter_by(private=False).all())))


if __name__ == '__main__':
    app.run()
