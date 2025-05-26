import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, jsonify, request, render_template, Response
import os
from typing import List, Dict, Optional, Union
import json

app = Flask(__name__)

# Настройки
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = os.path.normpath(r"C:\Users\Cyber Kanojo\Desktop\programming\Levashov_Maxim_python2023\flask-es-06d570dbee0e.json")
SPREADSHEET_ID = "1Jl0OhcH-LhXsI9fIo58pIfEPMrOuBKUHLq_-udr7OjA"

"""
ВСЕ ТЕСТОВЫЕ ЗАПРОСЫ:

1. Получить список всех студентов:
   http://127.0.0.1:1337/names

2. Получить средний балл за домашку:
   http://127.0.0.1:1337/hw-01/mean_score
   http://127.0.0.1:1337/hw-02/mean_score
   http://127.0.0.1:1337/main-hw-01/mean_score
   http://127.0.0.1:1337/main-hw-02/mean_score

3. Получить средний балл за домашку в группе:
   http://127.0.0.1:1337/hw-01/23137/mean_score
   http://127.0.0.1:1337/hw-02/23144/mean_score

4. Получить средний балл через параметры:
   http://127.0.0.1:1337/mean_score?group_id=23137&hw_name=hw-01

5. Получить оценку студента:
   http://127.0.0.1:1337/mark?student_id=1

6. Получить среднюю оценку группы:
   http://127.0.0.1:1337/mark?group_id=23137

7. Получить HTML таблицу с результатами:
   http://127.0.0.1:1337/course_table?hw_name=hw-01
   http://127.0.0.1:1337/course_table?hw_name=hw-02
   http://127.0.0.1:1337/course_table?hw_name=main-hw-01
   http://127.0.0.1:1337/course_table?hw_name=main-hw-02
   http://127.0.0.1:1337/course_table?hw_name=hw-01&group_id=23137

8. Получить итоговую таблицу с оценками:
   http://127.0.0.1:1337/final_grades
   http://127.0.0.1:1337/course_table?hw_name=final

9. Проверить работу сервера:
   http://127.0.0.1:1337/
"""

# Авторизация
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(SPREADSHEET_ID)

def json_response(data: Dict, status: int = 200) -> Response:
    return app.response_class(
        response=json.dumps(data, ensure_ascii=False),
        mimetype='application/json',
        status=status
    )

def get_sheet_data(sheet_name: str) -> List[Dict]:
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        records = worksheet.get_all_records()
        
        ids = worksheet.col_values(5)[1:]
        for i, row in enumerate(records):
            if i < len(ids) and ids[i]:
                row['student_id'] = str(ids[i]).strip()
            else:
                row['student_id'] = str(i+1)
        
        return records
    except Exception as e:
        print(f"Error accessing sheet {sheet_name}: {e}")
        return []

def calculate_mark(total_score: float) -> str:
    if total_score >= 50: return '5'
    elif total_score >= 30: return '4'
    elif total_score >= 1: return '3'
    return '2'

@app.route('/')
def home():
    return json_response({
        "message": "Сервер работает!",
        "endpoints": {
            "/names": "Список всех студентов",
            "/<hw>/mean_score": "Средний балл за домашку",
            "/<hw>/<group>/mean_score": "Средний балл за домашку в группе",
            "/mean_score?group_id=X&hw_name=Y": "Средний балл группы за домашку",
            "/mark?student_id=X": "Оценка студента",
            "/mark?group_id=X": "Средняя оценка группы",
            "/course_table?hw_name=X&group_id=Y": "Таблица с результатами",
            "/final_grades": "Итоговая таблица с оценками"
        }
    })

@app.route('/names')
def get_names():
    try:
        records = get_sheet_data('hw-01-git')
        names = [row['ФИ'] for row in records if 'ФИ' in row and row['ФИ']]
        return json_response({"names": names})
    except Exception as e:
        return json_response({"error": str(e)}, 500)

@app.route('/<hw_name>/mean_score')
def get_hw_mean(hw_name: str):
    try:
        sheet_map = {
            'hw-01': 'hw-01-git',
            'hw-02': 'hw-02-типы и структуры данных',
            'main-hw-01': 'main-hw-01',
            'main-hw-02': 'main-hw-02',
            'final': 'Итог'
        }
        
        if hw_name not in sheet_map:
            return json_response({"error": f"Домашнее задание {hw_name} не найдено"}, 404)
            
        records = get_sheet_data(sheet_map[hw_name])
        scores = []
        score_column = 'Баллы' if hw_name != 'final' else 'Сумма'
        
        for row in records:
            if score_column in row and row[score_column]:
                try:
                    scores.append(float(row[score_column]))
                except (ValueError, TypeError):
                    continue
                    
        if not scores:
            return json_response({"error": f"Нет данных по {hw_name}"}, 404)
            
        mean = sum(scores) / len(scores)
        return json_response({
            "hw_name": hw_name,
            "mean_score": round(mean, 2),
            "students_count": len(scores),
            "max_score": 10 if 'hw-' in hw_name else (50 if 'main-hw-01' in hw_name else 70)
        })
    except Exception as e:
        return json_response({"error": str(e)}, 500)

@app.route('/<hw_name>/<group_id>/mean_score')
def get_hw_group_mean(hw_name: str, group_id: str):
    try:
        sheet_map = {
            'hw-01': 'hw-01-git',
            'hw-02': 'hw-02-типы и структуры данных',
            'main-hw-01': 'main-hw-01',
            'main-hw-02': 'main-hw-02'
        }
        
        if hw_name not in sheet_map:
            return json_response({"error": f"Домашнее задание {hw_name} не найдено"}, 404)
            
        records = get_sheet_data(sheet_map[hw_name])
        scores = []
        
        for row in records:
            if ('Баллы' in row and row['Баллы'] and 
                'Группа' in row and str(row['Группа']) == str(group_id)):
                try:
                    scores.append(float(row['Баллы']))
                except (ValueError, TypeError):
                    continue
                    
        if not scores:
            return json_response({"error": f"Нет данных по {hw_name} для группы {group_id}"}, 404)
            
        mean = sum(scores) / len(scores)
        return json_response({
            "hw_name": hw_name,
            "group_id": group_id,
            "mean_score": round(mean, 2),
            "students_count": len(scores)
        })
    except Exception as e:
        return json_response({"error": str(e)}, 500)

@app.route('/mean_score')
def get_mean_score_params():
    group_id = request.args.get('group_id')
    hw_name = request.args.get('hw_name')
    
    if not group_id or not hw_name:
        return json_response({"error": "Необходимо указать group_id и hw_name"}, 400)
        
    return get_hw_group_mean(hw_name, group_id)

@app.route('/mark')
def get_mark():
    student_id = request.args.get('student_id')
    group_id = request.args.get('group_id')
    
    try:
        if student_id:
            records = get_sheet_data('Итог')
            student = next((s for s in records 
                          if 'student_id' in s 
                          and str(s['student_id']) == str(student_id)), None)
            
            if not student:
                return json_response({"error": f"Студент с ID {student_id} не найден"}, 404)
                
            if 'Оценка' in student and student['Оценка']:
                mark = student['Оценка']
            else:
                total = sum(float(student.get(col, 0)) 
                         for col in ['hw-01-git', 'hw-02-data-types', 
                                    'main-hw-01', 'main-hw-02']
                         if col in student and student[col])
                mark = calculate_mark(total)
            
            return json_response({
                "student_id": student_id,
                "mark": mark,
                "name": student.get('ФИ', 'Неизвестно'),
                "group": student.get('Группа', '')
            })
                
        elif group_id:
            records = get_sheet_data('Итог')
            marks = []
            students = []
            for s in records:
                if 'Группа' in s and str(s['Группа']) == str(group_id):
                    if 'Оценка' in s and s['Оценка']:
                        try:
                            marks.append(float(s['Оценка']))
                            students.append(s.get('ФИ', 'Неизвестно'))
                        except (ValueError, TypeError):
                            continue
                    else:
                        total = sum(float(s.get(col, 0)) 
                                 for col in ['hw-01-git', 'hw-02-data-types', 
                                            'main-hw-01', 'main-hw-02']
                                 if col in s and s[col])
                        marks.append(float(calculate_mark(total)))
                        students.append(s.get('ФИ', 'Неизвестно'))
            
            if not marks:
                return json_response({"error": f"В группе {group_id} нет оценок"}, 404)
                
            return json_response({
                "group_id": group_id,
                "mean_mark": round(sum(marks)/len(marks), 2),
                "students_count": len(marks),
                "students": students
            })
            
        return json_response({"error": "Укажите student_id или group_id"}, 400)
        
    except Exception as e:
        return json_response({"error": str(e)}, 500)

@app.route('/course_table')
def course_table():
    hw_name = request.args.get('hw_name')
    group_id = request.args.get('group_id')
    
    if not hw_name:
        return json_response({"error": "Необходимо указать hw_name"}, 400)
        
    try:
        sheet_map = {
            'hw-01': 'hw-01-git',
            'hw-02': 'hw-02-типы и структуры данных',
            'main-hw-01': 'main-hw-01',
            'main-hw-02': 'main-hw-02',
            'final': 'Итог'
        }
        
        if hw_name not in sheet_map:
            return json_response({"error": f"Домашнее задание {hw_name} не найдено"}, 404)
            
        records = get_sheet_data(sheet_map[hw_name])
        filtered = []
        score_column = 'Баллы' if hw_name != 'final' else 'Сумма'
        
        for row in records:
            if 'ФИ' in row and row['ФИ']:
                if score_column in row and row[score_column]:
                    if not group_id or ('Группа' in row and str(row['Группа']) == str(group_id)):
                        student_data = {
                            'id': row.get('student_id', ''),
                            'Name': row['ФИ'],
                            'group_id': row.get('Группа', ''),
                            'score': row[score_column]
                        }
                        
                        if hw_name == 'final' and 'Оценка' in row:
                            student_data['mark'] = row['Оценка']
                        
                        filtered.append(student_data)
        
        if not filtered:
            return json_response({"error": f"Нет данных для {hw_name}" + (f" в группе {group_id}" if group_id else "")}, 404)
            
        return render_template('table.html', 
                            students=filtered,
                            hw_name=hw_name,
                            group_id=group_id,
                            is_final=hw_name == 'final')
    except Exception as e:
        return json_response({"error": str(e)}, 500)

@app.route('/final_grades')
def final_grades():
    return course_table()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, debug=True)