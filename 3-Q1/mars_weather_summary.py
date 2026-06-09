import csv

import mysql.connector


class MySQLHelper:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        self.cursor = self.connection.cursor()

    def execute(self, query, values=None):
        if values is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, values)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


def create_table(mysql_helper):
    """
    mars_weather 테이블 생성
    """
    query = '''
    CREATE TABLE IF NOT EXISTS mars_weather (
        weather_id INT AUTO_INCREMENT PRIMARY KEY,
        mars_date DATETIME NOT NULL,
        temp INT,
        storm INT
    )
    '''

    mysql_helper.execute(query)
    mysql_helper.commit()


def read_csv_file(file_name):
    """
    CSV 파일을 읽어 리스트로 반환
    """
    weather_data = []

    with open(file_name, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            weather_data.append(
                (
                    row['mars_date'],
                    int(float(row['temp'])),
                    int(row['storm'])
                )
            )

    return weather_data


def insert_weather_data(mysql_helper, weather_data):
    """
    CSV 데이터를 DB에 저장
    """
    query = '''
    INSERT INTO mars_weather
    (mars_date, temp, storm)
    VALUES (%s, %s, %s)
    '''

    for data in weather_data:
        mysql_helper.execute(query, data)

    mysql_helper.commit()


def print_csv_data(weather_data):
    """
    CSV 데이터 확인용 출력
    """
    print('===== CSV 데이터 =====')

    for data in weather_data:
        print(data)

    print()


def main():
    mysql_helper = MySQLHelper(
        host='localhost',
        user='root',
        password='1234',
        database='mars_db'
    )

    create_table(mysql_helper)

    weather_data = read_csv_file('mars_weathers_data.csv')

    print_csv_data(weather_data)

    print(f'읽어온 데이터 수: {len(weather_data)}')

    insert_weather_data(mysql_helper, weather_data)

    print('데이터 저장 완료')

    mysql_helper.close()


if __name__ == '__main__':
    main()