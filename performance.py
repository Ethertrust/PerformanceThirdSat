import gs2
import mdb
from datetime import datetime as dt

def getGSheetNames():
    return gs2.read('1Neha8OoG_OORL8sd-1yleBIJB2XjTWj_PqsGSjN2CsY', 'b Performance')

def genPerformance(names):
    perf = []
    for name in names:
        d = {'FIO': name,
             'Нулевое': '',
             'Первое': '',
             'Второе': '',
             'Третье': '',
             'Четвёртое': '',
             'Упражнение 1': '',
             'Упражнение 2': '',
             'Упражнение 3': '',
             'Упражнение 4': '',
             'О себе.py': '',
             'Ошибки': [],
             'Последняя активность': '',
             'AllDone': '',
             'Успех': '',
             '% Успех': '',
             'Зачет': ''}
        perf.append(d)
    return perf

def lastActivity(student, row):
    if student['Последняя активность'] == '':
        student['Последняя активность'] = row[9]
        #"2024-04-24 22:33:23"
    if dt.strptime(student['Последняя активность'], "%Y-%m-%d %H:%M:%S")< dt.strptime(row[9], "%Y-%m-%d %H:%M:%S"):
        student['Последняя активность'] = row[9]
        student['attempt'] = row[13]
        student['q id'] = [row[14], row[4]]

def checkTest(student, row, tries, testNames):
    #Тест.Вопрос
    key = str(testNames[row[0]][1]) + '.' + str(row[4])
    if int(row[6])>0:
        if not key in tries:
            tries[key] = [str(row[7]),  str(row[13]),  str(row[14]),  str(row[4]),  str(row[2]),  str(row[6]), str(row[0])]
        else:
            if tries[key][0] != 'complete' and row[7] == 'complete':
                tries[key] = [str(row[7]),  str(row[13]),  str(row[14]),  str(row[4]),  str(row[2]),  str(row[6]), str(row[0])]

def sumErrors(student, tries):
    for stTry in tries:
        if tries[stTry][0] != 'complete':
            stlTry = stTry.split('.')
            student['Ошибки'].append(stlTry[0] + '.' + tries[stTry][-3] + '.' + stlTry[1] + '.' + tries[stTry][-2])
    student['Ошибки'] = '\'' + ', '.join(student['Ошибки'])

def statusTest(student, tries, testNames):
    for test in testNames:
        fullcomplete = True
        key = ''
        for q in range(1, testNames[test][2]+1):
            key = str(testNames[test][1])+'.'+str(q)
            if not key in tries:
                fullcomplete = False
            elif tries[key][0] !='complete':
                fullcomplete = False
                #  # П.В.Ш https://moodle.surgu.ru/mod/quiz/review.php?attempt=1355811#question-1529449-2
                student[testNames[test][0]] ="=HYPERLINK(\"https://moodle.surgu.ru/mod/quiz/review.php?attempt={}#question-{}-{}\"; \"{}\")".format(
                    tries[key][1], tries[key][2], tries[key][3], str(testNames[test][1])+'.'+str(q)+'.'+tries[key][-2])
        if fullcomplete:
            student[testNames[test][0]] = "=HYPERLINK(\"https://moodle.surgu.ru/mod/quiz/review.php?attempt={}#question-{}-{}\"; \"{}\")".format(
                    tries[key][1], tries[key][2], tries[key][3], '+')

def lastHlink(student):
    if 'attempt' in student:
        student['Последняя активность'] = "=HYPERLINK(\"https://moodle.surgu.ru/mod/quiz/review.php?attempt={}#question-{}-{}\"; \"{}\")".format(
                    student['attempt'], student['q id'][0], student['q id'][1], student['Последняя активность'])

def stPerformance(student, data):
    testNames = {'Нулевое практическое занятие по Python': ['Нулевое', 0, 3],
                'Первое практическое занятие по Python': ['Первое', 1, 5],
                'Второе практическое занятие по Python': ['Второе', 2, 5],
                'Третье практическое занятие по Python': ['Третье', 3, 4],
                'Четвёртое практическое занятие по Python': ['Четвёртое', 4, 7],
                'Упражнение 1': ['Упражнение 1', 5, 4],
                'Упражнение 2': ['Упражнение 2', 6, 4],
                'Упражнение 3': ['Упражнение 3', 7, 4],
                'Упражнение 4': ['Упражнение 4', 8, 5]}
    tries = {}
    # 0 - Тест, 1 - ФИО, 2 - № попытки, 4 - № вопроса, 6 - шаг, 7 - состояние, 9 - дата, 12 - О себе.py, 13 - attempt id, 14 - question usage id
    for row in data:
        if student['FIO'] == row[1]:
            lastActivity(student, row)
            checkTest(student, row, tries, testNames)
    sumErrors(student, tries)
    statusTest(student, tries, testNames)
    lastHlink(student)

def performance(names, data):
    performance = genPerformance(names)
    #print(performance)
    for student in performance:
        stPerformance(student, data)
    newperformance = []
    newperformance += [list(row.values())[:-3] for row in performance]
    return newperformance

if __name__ == '__main__':
    data = mdb.get_data()
    #print(data)
    names = getGSheetNames()
    #print(names)
    table = performance(names, data)
    gs2.write(table,'1Neha8OoG_OORL8sd-1yleBIJB2XjTWj_PqsGSjN2CsY', 'b Performance')