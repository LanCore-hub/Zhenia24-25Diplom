from flask import Flask
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

#Создание сервера Flask
server = Flask(__name__)

# Загрузка данных
df_course1 = pd.read_excel("C:/Users/Zver/Downloads/logs_Python_науч_20240623-0236.xlsx")
df_course2 = pd.read_excel("C:/Users/Zver/Downloads/logs_Time_series _20240623-0046.xlsx")
df_course3 = pd.read_excel("C:/Users/Zver/Downloads/logs_РКИиП_ТВиМС_1_20240623-0235.xlsx")
df_course4 = pd.read_excel("C:/Users/Zver/Downloads/logs_ТВиМС_ИВТ_1_20240623-0234.xlsx")

courses = {
    'Язык программирования Python для научных вычислений': df_course1,
    'Анализ временных рядов': df_course2,
    'Теория вероятностей и математическая статистика (ИВТ)': df_course3,
    'Теория вероятности и математическая статистика (Разработка компьютерных игр и приложений)': df_course4
}

# Создание экземпляра Dash, используя Flask как сервер
app = Dash(__name__, server=server)

# Определение преподавателя
teachers = ['Есин Роман Витальевич']  # Список преподавателей

# Определяем список недель
weeks_list = list(range(1, 19))

# Определяем семестры
semesters = ['Весенний', 'Осенний']

app.layout = html.Div(style={'padding': '20px'}, children=[
    dcc.Location(id='url', refresh=False),  # Компонент для отслеживания URL
    html.Div(id='page-content')  # Контейнер для отображения содержимого страниц
])

# Главная страница
def home_page():
    return html.Div(style={'padding': '20px'}, children=[
        html.H1("Активность преподавателя и студентов в электронной среде", style={'textAlign': 'center'}),
        dcc.Link("Перейти на страницу преподавателя", href="/teacher", style={'fontSize': '20px', 'margin': '20px'}),
        html.Div([
            dcc.Dropdown(
                id='teacher-dropdown',
                options=[{'label': teacher, 'value': teacher} for teacher in teachers],
                value='Есин Роман Витальевич',  # Значение по умолчанию
                clearable=False
            ),
            dcc.Dropdown(
                id='semester-dropdown',
                options=[{'label': semester, 'value': semester} for semester in semesters],
                value='Весенний',  # Значение по умолчанию
                clearable=False
            ),
            dcc.Dropdown(
                id='course-dropdown',
                options=[],  # Список курсов будет обновляться в зависимости от выбранного преподавателя и семестра
                value='',
                clearable=False
            ),
        ], style={'margin-bottom': '20px'}),

        html.Div(style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '20px'}, children=[
            html.Div(dcc.Graph(id='activity-graph'), style={'flex': '1 1 45%', 'min-width': '300px'}),
            html.Div(dcc.Graph(id='weekly-activity-graph'), style={'flex': '1 1 45%', 'min-width': '300px'}),
            html.Div(dcc.Graph(id='student-activity-graph'), style={'flex': '1 1 45%', 'min-width': '300px'}),
            html.Div(dcc.Graph(id='unique-student-activity-graph'), style={'flex': '1 1 45%', 'min-width': '300px'}),
            html.Div(dcc.Graph(id='unique-student-resources-graph'), style={'flex': '1 1 45%', 'min-width': '300px'}),
            html.Div(dcc.Graph(id='total-student-actions-graph'), style={'flex': '1 1 45%', 'min-width': '300px'}),
            html.Div(dcc.Graph(id='component-type-pie-chart'), style={'flex': '1 1 45%', 'min-width': '300px'}),
            html.Div(style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start'}, children=[
                dcc.Dropdown(
                    id='week-dropdown',
                    options=[{'label': f'Неделя {week}', 'value': week} for week in weeks_list],
                    value=1,  # Значение по умолчанию
                    clearable=False,
                    style={'margin': '10px 0', 'width': '250px'}
                ),
                html.Div(dcc.Graph(id='weekly-teacher-activities-graph', style={'width': '100%'}),
                         style={'flex': '1 1 100%', 'min-width': '600px'}),
            ]),
            html.Div(dcc.Graph(id='average-posts-weekly-graph'), style={'flex': '1 1 45%', 'min-width': '300px'}),
            html.Div(dcc.Graph(id='student-teacher-activity-graph'), style={'flex': '1 1 45%', 'min-width': '300px'}),
            html.Div(dcc.Graph(id='hourly-activity-graph'), style={'flex': '1 1 45%', 'min-width': '300px'}),

        ])
    ])

# Страница преподавателя
def teacher_page():
    return html.Div(style={'padding': '20px'}, children=[
        html.H1("Страница преподавателя", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='teacher-dropdown',
            options=[{'label': teacher, 'value': teacher} for teacher in teachers],
            value='Есин Роман Витальевич',  # Значение по умолчанию
            clearable=False
        ),
        dcc.Dropdown(
            id='semester-dropdown',
            options=[{'label': semester, 'value': semester} for semester in semesters],
            value='Весенний',  # Значение по умолчанию
            clearable=False
        ),
        dcc.Graph(id='activity-graph-teacher', style={'flex': '1 1 45%', 'min-width': '300px'}),
        dcc.Graph(id='weekly-activity-graph-teacher', style={'flex': '1 1 45%', 'min-width': '300px'}),
    ])

@app.callback(
            Output('course-dropdown', 'options'),
            Input('teacher-dropdown', 'value'),
            Input('semester-dropdown', 'value'),
)

def update_course_options(selected_teacher, selected_semester):
    # Обновление списка доступных курсов в зависимости от выбранного преподавателя и семестра
    if selected_teacher == 'Есин Роман Витальевич':
        if selected_semester == 'Весенний':
            return [{'label': 'Язык программирования Python для научных вычислений', 'value': 'Язык программирования Python для научных вычислений'},
                    {'label': 'Анализ временных рядов', 'value': 'Анализ временных рядов'}]
        else:  # Осенний семестр
            return [{'label': 'Теория вероятностей и математическая статистика (ИВТ)', 'value': 'Теория вероятностей и математическая статистика (ИВТ)'},
                    {'label': 'Теория вероятности и математическая статистика (Разработка компьютерных игр и приложений)', 'value': 'Теория вероятности и математическая статистика (Разработка компьютерных игр и приложений)'}]
    return []

@app.callback(
    Output('activity-graph-teacher', 'figure'),
    Output('weekly-activity-graph-teacher', 'figure'),
    Input('teacher-dropdown', 'value'),
    Input('semester-dropdown', 'value'),
)

def update_graph_teacher_page(selected_teacher, selected_semester):
    # Объединяем данные за семестр
    df_combined = pd.DataFrame()

    for course_name, df_course in courses.items():
        # Преобразование времени
        df_course['Время'] = pd.to_datetime(df_course['Время'], format="%d/%m/%y, %H:%M", errors='coerce')

        # Фильтрация данных по выбранному преподавателю
        df_teacher = df_course[df_course['Полное имя пользователя'] == selected_teacher]

        # Определение временных рамок для семестров
        if selected_semester == 'Весенний':
            # Объединяем данные за весенний семестр
            df_combined = pd.concat([
                df_course1[df_course1['Полное имя пользователя'] == selected_teacher],
                df_course2[df_course2['Полное имя пользователя'] == selected_teacher]
            ])
            df_combined = df_combined[(df_combined['Время'].dt.month >= 2) & (df_combined['Время'].dt.month <= 5)]

            month_order = [1, 2, 3, 4, 5]  # Январь - Май
        else:  # Осенний семестр
            # Объединяем данные за осенний семестр
            df_combined = pd.concat([
                df_course3[df_course3['Полное имя пользователя'] == selected_teacher],
                df_course4[df_course4['Полное имя пользователя'] == selected_teacher]
            ])
            df_combined = df_combined[(df_combined['Время'].dt.month >= 9) | (df_combined['Время'].dt.month == 1)]

            month_order = [9, 10, 11, 12, 1]  # Сентябрь - Январь

    # Группировка данных по месяцам
    df_combined['Месяц'] = df_combined['Время'].dt.month
    monthly_logins = df_combined.groupby('Месяц').size().reset_index(name='Количество событий')

    # Переименование месяцев
    month_map = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    monthly_logins['Месяц'] = monthly_logins['Месяц'].map(month_map)

    # Переупорядочивание данных по месяцам
    monthly_logins = monthly_logins[monthly_logins['Месяц'].notnull()]  # Удаляем строки с NaN

    monthly_logins['Месяц'] = pd.Categorical(monthly_logins['Месяц'], categories=[month_map[m] for m in month_order],
                                             ordered=True)
    monthly_logins = monthly_logins.sort_values('Месяц')

    # График активности по месяцам
    activity_fig = go.Figure(data=[go.Pie(labels=monthly_logins['Месяц'],
                                          values=monthly_logins['Количество событий'],
                                          hole=.3, sort=False)])
    activity_fig.update_layout(title='Активность преподавателя по месяцам')

    # Переупорядочивание данных по неделям
    if selected_semester == 'Весенний':
        week_ranges = [
            ('2024-02-05', '2024-02-12'),
            ('2024-02-12', '2024-02-19'),
            ('2024-02-19', '2024-02-26'),
            ('2024-02-26', '2024-03-04'),
            ('2024-03-04', '2024-03-11'),
            ('2024-03-11', '2024-03-18'),
            ('2024-03-18', '2024-03-25'),
            ('2024-03-25', '2024-04-01'),
            ('2024-04-01', '2024-04-08'),
            ('2024-04-08', '2024-04-15'),
            ('2024-04-15', '2024-04-22'),
            ('2024-04-22', '2024-04-29'),
            ('2024-04-29', '2024-05-06'),
            ('2024-05-06', '2024-05-13'),
            ('2024-05-13', '2024-05-20'),
            ('2024-05-20', '2024-05-27'),
            ('2024-05-27', '2024-06-03'),
        ]
    else:  # Осенний семестр
        week_ranges = [
            ('2023-09-01', '2023-09-06'),
            ('2023-09-06', '2023-09-13'),
            ('2023-09-13', '2023-09-20'),
            ('2023-09-20', '2023-09-27'),
            ('2023-09-27', '2023-10-04'),
            ('2023-10-04', '2023-10-11'),
            ('2023-10-11', '2023-10-18'),
            ('2023-10-18', '2023-10-25'),
            ('2023-10-25', '2023-11-01'),
            ('2023-11-01', '2023-11-08'),
            ('2023-11-08', '2023-11-15'),
            ('2023-11-15', '2023-11-22'),
            ('2023-11-22', '2023-11-29'),
            ('2023-11-29', '2023-12-06'),
            ('2023-12-06', '2023-12-13'),
            ('2023-12-13', '2023-12-20'),
            ('2023-12-20', '2023-12-27'),
            ('2023-12-27', '2024-01-10'),
        ]

    weekly_data_list_teachers = []

    # Разбиение на недели и добавление данных в список для преподавателя
    for i, (start_date, end_date) in enumerate(week_ranges, 1):
        weekly_data = df_combined.query("@start_date <= Время <= @end_date")
        weekly_data['Неделя'] = i
        weekly_data_list_teachers.append(weekly_data)

    # Объединение всех недельных данных в один DataFrame
    weeks_semestr_teachers = pd.concat(weekly_data_list_teachers)

    # Группировка данных по неделям для преподавателя
    events_per_week_prepod = weeks_semestr_teachers.groupby('Неделя').count().reset_index()
    events_per_week_prepod.rename(columns={'Время': 'Количество событий'}, inplace=True)

    # Определение недостающих недель
    all_weeks = set(range(1, 19))
    existing_weeks = set(events_per_week_prepod['Неделя'])
    missing_weeks = all_weeks - existing_weeks

    # Создание DataFrame для недостающих недель
    missing_weeks_df = pd.DataFrame({'Неделя': list(missing_weeks), 'Количество событий': 0})

    # Объединение исходного DataFrame с недостающими неделями
    events_per_week_prepod = pd.concat([events_per_week_prepod, missing_weeks_df])

    # Сортировка по неделям
    events_per_week_prepod = events_per_week_prepod.sort_values(by='Неделя').reset_index(drop=True)

    # График активности по неделям для преподавателя
    weekly_activity_fig = go.Figure(data=[
        go.Bar(x=events_per_week_prepod['Неделя'], y=events_per_week_prepod['Количество событий'],
               name='Количество событий')
    ])
    # Добавление средней линии активности
    average_activity_events_per_week_prepod = events_per_week_prepod['Количество событий'].mean()
    weekly_activity_fig.add_trace(go.Scatter(
        x=events_per_week_prepod['Неделя'],
        y=[average_activity_events_per_week_prepod] * len(events_per_week_prepod),
        mode='lines',
        name='Средняя активность',
        line=dict(color='red', dash='dash')
    ))

    weekly_activity_fig.update_layout(title='Динамика активности преподавателя по неделям',
                                      yaxis_title='Количество событий',
                                      xaxis_title='Неделя')

    return activity_fig, weekly_activity_fig

@app.callback(
    Output('activity-graph', 'figure'),
    Output('weekly-activity-graph', 'figure'),
    Output('student-activity-graph', 'figure'),
    Output('unique-student-activity-graph', 'figure'),
    Output('unique-student-resources-graph', 'figure'),
    Output('total-student-actions-graph', 'figure'),
    Output('weekly-teacher-activities-graph', 'figure'),
    Output('average-posts-weekly-graph', 'figure'),
    Output('student-teacher-activity-graph', 'figure'),
    Output('component-type-pie-chart', 'figure'),
    Output('hourly-activity-graph', 'figure'),
    Input('teacher-dropdown', 'value'),
    Input('course-dropdown', 'value'),
    Input('week-dropdown', 'value'),
)

def update_graph_main(selected_teacher, selected_course, selected_week):
    # Получаем выбранный датафрейм
    df_selected = courses[selected_course]

    # Преобразование времени
    df_selected['Время'] = pd.to_datetime(df_selected['Время'], format="%d/%m/%y, %H:%M", errors='coerce')
    # Фильтрация данных по выбранному преподавателю
    df_teacher = df_selected[df_selected['Полное имя пользователя'] == selected_teacher]

    # Определение временных рамок для семестров
    if selected_course in ['Язык программирования Python для научных вычислений', 'Анализ временных рядов']:
        # Весенний семестр (январь - май)
        df_teacher = df_teacher[(df_teacher['Время'].dt.month >= 2) & (df_teacher['Время'].dt.month <= 5)]
        month_order = [1, 2, 3, 4, 5]  # Январь - Май
    else:
        # Осенний семестр (сентябрь - январь следующего года)
        df_teacher = df_teacher[(df_teacher['Время'].dt.month >= 9) | (df_teacher['Время'].dt.month == 1)]
        month_order = [9, 10, 11, 12, 1]  # Сентябрь - Январь

        # Группировка данных по месяцам для преподавателя
    df_teacher['Месяц'] = df_teacher['Время'].dt.month
    monthly_logins = df_teacher.groupby('Месяц').size().reset_index(name='Количество событий')

    # Переименование месяцев
    month_map = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    monthly_logins['Месяц'] = monthly_logins['Месяц'].map(month_map)

    # Переупорядочивание данных по месяцам
    monthly_logins = monthly_logins[monthly_logins['Месяц'].notnull()]  # Удаляем строки с NaN

    monthly_logins['Месяц'] = pd.Categorical(monthly_logins['Месяц'], categories=[month_map[m] for m in month_order],
                                             ordered=True)
    monthly_logins = monthly_logins.sort_values('Месяц')

    # График активности по месяцам
    activity_fig = go.Figure(data=[go.Pie(labels=monthly_logins['Месяц'],
                                          values=monthly_logins['Количество событий'],
                                          hole=.3, sort=False)])
    activity_fig.update_layout(title='Активность преподавателя по месяцам')

    if selected_course in ['Теория вероятностей и математическая статистика (ИВТ)', 'Теория вероятности и математическая статистика (Разработка компьютерных игр и приложений)']:
    # Переупорядочивание данных по неделям
        week_ranges = [
            ('2023-09-01', '2023-09-06'),
            ('2023-09-06', '2023-09-13'),
            ('2023-09-13', '2023-09-20'),
            ('2023-09-20', '2023-09-27'),
            ('2023-09-27', '2023-10-04'),
            ('2023-10-04', '2023-10-11'),
            ('2023-10-11', '2023-10-18'),
            ('2023-10-18', '2023-10-25'),
            ('2023-10-25', '2023-11-01'),
            ('2023-11-01', '2023-11-08'),
            ('2023-11-08', '2023-11-15'),
            ('2023-11-15', '2023-11-22'),
            ('2023-11-22', '2023-11-29'),
            ('2023-11-29', '2023-12-06'),
            ('2023-12-06', '2023-12-13'),
            ('2023-12-13', '2023-12-20'),
            ('2023-12-20', '2023-12-27'),
            ('2023-12-27', '2024-01-10'),
        ]
    elif selected_course in ['Язык программирования Python для научных вычислений', 'Анализ временных рядов']:
        week_ranges = [
            ('2024-02-05', '2024-02-12'),
            ('2024-02-12', '2024-02-19'),
            ('2024-02-19', '2024-02-26'),
            ('2024-02-26', '2024-03-04'),
            ('2024-03-04', '2024-03-11'),
            ('2024-03-11', '2024-03-18'),
            ('2024-03-18', '2024-03-25'),
            ('2024-03-25', '2024-04-01'),
            ('2024-04-01', '2024-04-08'),
            ('2024-04-08', '2024-04-15'),
            ('2024-04-15', '2024-04-22'),
            ('2024-04-22', '2024-04-29'),
            ('2024-04-29', '2024-05-06'),
            ('2024-05-06', '2024-05-13'),
            ('2024-05-13', '2024-05-20'),
            ('2024-05-20', '2024-05-27'),
            ('2024-05-27', '2024-06-03'),
        ]

    weekly_data_list_teachers = []

    # Разбиение на недели и добавление данных в список для преподавателя
    for i, (start_date, end_date) in enumerate(week_ranges, 1):
        weekly_data = df_teacher.query("@start_date <= Время <= @end_date")
        weekly_data['Неделя'] = i
        weekly_data_list_teachers.append(weekly_data)

    # Объединение всех недельных данных в один DataFrame
    weeks_semestr_teachers = pd.concat(weekly_data_list_teachers)

    # Группировка данных по неделям для преподавателя
    events_per_week_prepod = weeks_semestr_teachers.groupby('Неделя').count().reset_index()
    events_per_week_prepod.rename(columns={'Время': 'Количество событий'}, inplace=True)

    # Определение недостающих недель
    all_weeks = set(range(1, 19))
    existing_weeks = set(events_per_week_prepod['Неделя'])
    missing_weeks = all_weeks - existing_weeks

    # Создание DataFrame для недостающих недель
    missing_weeks_df = pd.DataFrame({'Неделя': list(missing_weeks), 'Количество событий': 0})

    # Объединение исходного DataFrame с недостающими неделями
    events_per_week_prepod = pd.concat([events_per_week_prepod, missing_weeks_df])

    # Сортировка по неделям
    events_per_week_prepod = events_per_week_prepod.sort_values(by='Неделя').reset_index(drop=True)

    # График активности по неделям для преподавателя
    weekly_activity_fig = go.Figure(data=[
        go.Bar(x=events_per_week_prepod['Неделя'], y=events_per_week_prepod['Количество событий'],
               name='Количество событий')
    ])
    # Добавление средней линии активности
    average_activity_events_per_week_prepod = events_per_week_prepod['Количество событий'].mean()
    weekly_activity_fig.add_trace(go.Scatter(
        x=events_per_week_prepod['Неделя'],
        y=[average_activity_events_per_week_prepod] * len(events_per_week_prepod),
        mode='lines',
        name='Средняя активность',
        line=dict(color='red', dash='dash')
    ))

    weekly_activity_fig.update_layout(title='Динамика активности преподавателя по неделям',
                                      yaxis_title='Количество событий',
                                      xaxis_title='Неделя')

 # Аналогичная логика для студентов
    df_schoolman = df_selected.loc[df_selected['Полное имя пользователя'] != selected_teacher]
    df_schoolman = df_schoolman.loc[df_schoolman['Полное имя пользователя'] != 0]

    weekly_data_list_students = []

 # Разбиение на недели и добавление данных в список для студентов
    for i, (start_date, end_date) in enumerate(week_ranges, 1):
     weekly_data_students = df_schoolman.query("@start_date <= Время <= @end_date")
     weekly_data_students['Неделя'] = i
     weekly_data_list_students.append(weekly_data_students)

 # Объединение всех недельных данных для студентов в один DataFrame
    weeks_semestr_students = pd.concat(weekly_data_list_students)

 # Группировка данных по неделям для студентов
    events_per_week_schoolman = weeks_semestr_students.groupby('Неделя').count().reset_index()
    events_per_week_schoolman.rename(columns={'Время': 'Количество событий'}, inplace=True)

 # Определение недостающих недель для студентов
    existing_weeks_students = set(events_per_week_schoolman['Неделя'])
    missing_weeks_students = all_weeks - existing_weeks_students

 # Создание DataFrame для недостающих недель
    missing_weeks_students_df = pd.DataFrame({'Неделя': list(missing_weeks_students), 'Количество событий': 0})

 # Объединение исходного DataFrame с недостающими неделями для студентов
    events_per_week_schoolman = pd.concat([events_per_week_schoolman, missing_weeks_students_df])

 # Сортировка по неделям
    events_per_week_schoolman = events_per_week_schoolman.sort_values(by='Неделя').reset_index(drop=True)

 # График активности студентов по неделям

    student_activity_fig = go.Figure(data=[
        go.Bar(x=events_per_week_schoolman['Неделя'], y=events_per_week_schoolman['Количество событий'],
               name='Количество событий')
    ])

    # Добавление средней линии активности
    average_activity_events_per_week_schoolman = events_per_week_schoolman['Количество событий'].mean()
    student_activity_fig.add_trace(go.Scatter(
        x=events_per_week_schoolman['Неделя'],
        y=[average_activity_events_per_week_schoolman] * len(events_per_week_schoolman),
        mode='lines',
        name='Средняя активность',
        line=dict(color='red', dash='dash')
    ))

    student_activity_fig.update_layout(title='Динамика активности студентов по неделям',
                                      yaxis_title='Количество событий',
                                      xaxis_title='Неделя')

   # Подсчет уникальных активных студентов каждую неделю
    unique_students_weekly = weeks_semestr_students.groupby('Неделя')['Полное имя пользователя'].nunique().reset_index()
    unique_students_weekly.rename(columns={'Полное имя пользователя': 'Количество активных уникальных студентов'}, inplace=True)

   # Определение недостающих недель для уникальных студентов
    existing_weeks_unique_students = set(unique_students_weekly['Неделя'])
    missing_weeks_unique_students = all_weeks - existing_weeks_unique_students

   # Создание DataFrame для недостающих недель
    missing_weeks_unique_students_df = pd.DataFrame({'Неделя': list(missing_weeks_unique_students), 'Количество активных уникальных студентов': 0})

   # Объединение исходного DataFrame с недостающими неделями для уникальных студентов
    unique_students_weekly = pd.concat([unique_students_weekly, missing_weeks_unique_students_df])

   # Сортировка по неделям
    unique_students_weekly = unique_students_weekly.sort_values(by='Неделя').reset_index(drop=True)

    # Подсчет уникальных студентов за весь курс
    unique_students_count = df_selected['Полное имя пользователя'].nunique()

   # График уникальных активных студентов по неделям
    unique_student_activity_fig = go.Figure(data=[
        go.Bar(x=unique_students_weekly['Неделя'], y=unique_students_weekly['Количество активных уникальных студентов'],
               name='Количество активных уникальных студентов')
    ])

    # Добавление средней линии активности
    average_activity_unique_students_weekly = unique_students_weekly['Количество активных уникальных студентов'].mean()
    unique_student_activity_fig.add_trace(go.Scatter(
        x=unique_students_weekly['Неделя'],
        y=[average_activity_unique_students_weekly] * len(unique_students_weekly),
        mode='lines',
        name='Средняя активность',
        line=dict(color='red', dash='dash')
    ))
    # Добавление линии на график уникальных активных студентов
    unique_student_activity_fig.add_trace(go.Scatter(
        x=unique_students_weekly['Неделя'],
        y=[unique_students_count] * len(unique_students_weekly),
        mode='lines',
        name='Общее количество уникальных студентов',
        line=dict(color='green', dash='dash')
    ))


    unique_student_activity_fig.update_layout(title='Динамика количества активных студентов по неделям',
                                      yaxis_title='Количество активных уникальных студентов',
                                      xaxis_title='Неделя')

   # Подсчет уникальных используемых студентами элементов/ресурсов в курсе каждую неделю
    unique_students_resources_weekly = weeks_semestr_students.groupby('Неделя')['Контекст события'].nunique().reset_index()
    unique_students_resources_weekly.rename(columns={'Контекст события': 'Количество уникальных элементов'}, inplace=True)

   # Определение недостающих недель для уникальных ресурсов студентов
    existing_weeks_unique_resources_students = set(unique_students_resources_weekly['Неделя'])
    missing_weeks_unique_resources_students = all_weeks - existing_weeks_unique_resources_students

   # Создание DataFrame для недостающих недель
    missing_weeks_unique_resources_students_df = pd.DataFrame({'Неделя': list(missing_weeks_unique_resources_students), 'Количество уникальных элементов': 0})

   # Объединение исходного DataFrame с недостающими неделями для студентов
    unique_students_resources_weekly = pd.concat([unique_students_resources_weekly, missing_weeks_unique_resources_students_df])

   # Сортировка по неделям
    unique_students_resources_weekly = unique_students_resources_weekly.sort_values(by='Неделя').reset_index(drop=True)

   # График уникальных используемых студентами элементов/ресурсов в курсе студентов по неделям
    unique_resources_student_activity_fig = px.bar(unique_students_resources_weekly, x='Неделя', y='Количество уникальных элементов', title='Динамика количества используемых студентами ресурсов по неделям')

    # Общее количество действий студентов по использованию элементов/ресурсов ЭОК каждую неделю
    total_student_actions_weekly = weeks_semestr_students.groupby('Неделя').size().reset_index()
    total_student_actions_weekly.rename(columns={0: 'Количество уникальных элементов'}, inplace=True)

    total_student_actions_weekly_df = weeks_semestr_students.groupby('Неделя').size()

    # Определение недостающих недель для студентов
    existing_weeks_total_actions_students = set(total_student_actions_weekly['Неделя'])
    missing_weeks_total_actions_students = all_weeks - existing_weeks_total_actions_students

    # Создание DataFrame для недостающих недель
    missing_weeks_total_actions_students_df = pd.DataFrame({'Неделя': list(missing_weeks_total_actions_students), 'Количество уникальных элементов': 0})

    # Объединение исходного DataFrame с недостающими неделями для студентов
    total_student_actions_weekly = pd.concat([total_student_actions_weekly, missing_weeks_total_actions_students_df])

    # Сортировка по неделям
    total_student_actions_weekly = total_student_actions_weekly.sort_values(by='Неделя').reset_index(drop=True)

    # График общего количества действий студентов по использованию элементов/ресурсов
    total_actions_student_activity_fig = px.bar(total_student_actions_weekly, x='Неделя', y='Количество уникальных элементов', title='Динамика общего количества действий студентов по использованию ресурсов по неделям')

    # Общее количество действий преподавателя по использованию элементов/ресурсов ЭОК каждую неделю
    total_teacher_actions_weekly = weeks_semestr_teachers.groupby('Неделя').size().reset_index()
    total_teacher_actions_weekly.rename(columns={0: 'Количество действий преподавателя'}, inplace=True)

    total_teacher_actions_weekly_df = weeks_semestr_teachers.groupby('Неделя').size()

    # Количество активностей преподавателя в разных компонентах курса
    teacher_activities_components = weeks_semestr_teachers['Компонент'].value_counts().reset_index()
    teacher_activities_components.rename(columns={'count': 'Количество активностей преподавателя'}, inplace=True)

    # Количество активностей преподавателя в разных компонентах курса по неделям
    weekly_teacher_activities = weeks_semestr_teachers.groupby(['Неделя', 'Компонент']).size().reset_index(name='Количество активностей')

    # Фильтрация данных для удаления строк с компонентом '0'
    weekly_teacher_activities = weekly_teacher_activities[weekly_teacher_activities['Компонент'] != 0]

    # Обновление графика активности преподавателя по выбранной неделе
    weekly_teacher_activities_filtered = weekly_teacher_activities[weekly_teacher_activities['Неделя'] == selected_week]

    # График активности преподавателя по компонентам для выбранной недели
    weekly_teacher_activities_graph = px.bar(weekly_teacher_activities_filtered,
                                             x='Компонент',
                                             y='Количество активностей',
                                             title=f'Количество активностей преподавателя по компонентам (Неделя {selected_week})')

    # Соотношение действий преподавателя внутри курса к общему количеству действий всех пользователей в курсе
    teacher_to_total_actions_ratio = (total_teacher_actions_weekly_df / (total_teacher_actions_weekly_df + total_student_actions_weekly_df)).reset_index()
    teacher_to_total_actions_ratio.rename(columns={0: 'Соотношение действий преподавателя'}, inplace=True)

    # Определение недостающих недель
    existing_teacher_to_total_actions_teachers = set(teacher_to_total_actions_ratio['Неделя'])
    missing_teacher_to_total_actions_teachers = all_weeks - existing_teacher_to_total_actions_teachers

    # Создание DataFrame для недостающих недель
    missing_teacher_to_total_actions_teachers_df = pd.DataFrame({'Неделя': list(missing_teacher_to_total_actions_teachers), 'Соотношение действий преподавателя': 0})

    # Объединение исходного DataFrame с недостающими неделями
    teacher_to_total_actions_ratio = pd.concat([teacher_to_total_actions_ratio, missing_teacher_to_total_actions_teachers_df])

    # Сортировка по неделям
    teacher_to_total_actions_ratio = teacher_to_total_actions_ratio.sort_values(by='Неделя').reset_index(drop=True)

    # График общего количества действий преподавателей по использованию элементов/ресурсов
    average_posts_weekly_fig = px.bar(teacher_to_total_actions_ratio, x='Неделя', y='Соотношение действий преподавателя', title='Динамика соотношение действий преподавателя внутри курса к общему количеству действий всех пользователей в курсе')

    #Зависимость между активностью студентов и динамикой активности преподавателя
    student_teacher_activity_fig = go.Figure()

    # Добавление данных для активности преподавателя
    student_teacher_activity_fig.add_trace(go.Scatter(
        x=events_per_week_prepod['Неделя'],
        y=events_per_week_prepod['Количество событий'],
        mode='lines+markers',
        name='Активность преподавателя',
        line=dict(color='blue')
    ))

    # Добавление данных для активности студентов
    student_teacher_activity_fig.add_trace(go.Scatter(
        x=events_per_week_schoolman['Неделя'],
        y=events_per_week_schoolman['Количество событий'],
        mode='lines+markers',
        name='Активность студентов',
        line=dict(color='red')
    ))

    student_teacher_activity_fig.update_layout(
        title='Сравнение активности студентов и преподавателя по неделям',
        xaxis_title='Неделя',
        yaxis_title='Количество событий',
        legend=dict(x=0, y=1)
    )

    # График количества компонентов разного типа в курсе
    component_counts = df_selected['Компонент'].value_counts()

    # Define colors for the pie chart
    colors = px.colors.qualitative.Plotly

    # График количества компонентов разного типа в курсе
    total_components = component_counts.sum()
    percentages = (component_counts / total_components * 100).round(2)  # Calculate percentages

    # Create a DataFrame for the table
    percentage_df = pd.DataFrame({
        'Компонент': component_counts.index,
        'Количество': component_counts.values,
        'Процент': percentages.values
    })

    # Create the pie chart
    component_type_pie_chart = go.Figure(data=[go.Pie(
        labels=component_counts.index,
        values=component_counts.values,
        hoverinfo='label+percent',
        textinfo='label+percent',
        marker=dict(colors=colors),
        pull=[0.1] * len(component_counts)
    )])

    component_type_pie_chart.update_traces(textposition='inside')

    component_type_pie_chart.update_layout(
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        title='Количество компонентов разного типа в курсе',
        height=500,
        showlegend=True
    )

    # Группировка данных по часам
    df_selected['Час'] = df_selected['Время'].dt.hour
    activity_hourly = df_selected.groupby(['Час', 'Полное имя пользователя']).size().reset_index(
        name='Количество событий')

    # Разделяем данные для преподавателей и студентов
    teacher_activity = activity_hourly[activity_hourly['Полное имя пользователя'] == selected_teacher]
    student_activity = activity_hourly[activity_hourly['Полное имя пользователя'] != selected_teacher]

    # Усреднение по часам
    teacher_avg_activity = teacher_activity.groupby('Час')['Количество событий'].mean().reset_index()
    student_avg_activity = student_activity.groupby('Час')['Количество событий'].mean().reset_index()

    # Создание графика для часовой активности
    hourly_activity_fig = go.Figure()
    hourly_activity_fig.add_trace(go.Bar(
        x=teacher_avg_activity['Час'],
        y=teacher_avg_activity['Количество событий'],
        name='Активность преподавателя',
        marker_color='blue'
    ))
    hourly_activity_fig.add_trace(go.Bar(
        x=student_avg_activity['Час'],
        y=student_avg_activity['Количество событий'],
        name='Активность студентов',
        marker_color='red'
    ))

    hourly_activity_fig.update_layout(title='Средняя часовая активность преподавателя и студентов',
                                      xaxis_title='Часы',
                                      yaxis_title='Среднее количество событий')
    # Настройка меток по оси X
    hourly_activity_fig.update_xaxes(
        tickmode='linear',  # Устанавливаем линейный режим для меток
        dtick=1  # Устанавливаем интервал меток на 1 час
    )

    return activity_fig, weekly_activity_fig, student_activity_fig, unique_student_activity_fig, unique_resources_student_activity_fig, total_actions_student_activity_fig, weekly_teacher_activities_graph, average_posts_weekly_fig, student_teacher_activity_fig, component_type_pie_chart, hourly_activity_fig    # Возвращаем все графики

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/teacher':
        return teacher_page()
    else:
        return home_page()

#Оживление сервера
if __name__ == '__main__':
    server.run(debug=True)
