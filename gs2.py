import gspread

gc = gspread.service_account(filename="C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Thursday\\8\\sa_creds_new.json")

def read(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
    sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
    get_values = sh.values_get(range=SAMPLE_RANGE_NAME + '!A:A')['values']
    values = get_values[2:]
    return values

def write(data, SAMPLE_SPREADSHEET_ID, sheetname):
    sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
    worksheet = sh.worksheet(sheetname)
    worksheet.update('A3', data)

if __name__ == '__main__':
    # for val in read('13UIj4U0ry16Ib5W6dWMrtCpNyv-5TW5hUMzIJlkIFb4', 'b Performance'):
    #     print(val[0])
    data = [['Стрельцов Андрей Александрович', '', "'+", "'+", '', "'+", "'+", "'+", "'+", "'+", '', '', '2024-03-05 23:34:08', '', '', '', ''],
            ['Стрельцов Андрей Александрович', '', "'+", "'+", '', "'+", "'+", "'+", "'+", "'+", '', '', '2024-03-05 23:34:08', '', '', '', '']]
    write(data, '13UIj4U0ry16Ib5W6dWMrtCpNyv-5TW5hUMzIJlkIFb4', 'b Performance')
    print("evil commit")
    print("more evil commits")