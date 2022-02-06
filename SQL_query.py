import sqlite3


class englishWords:
    def __init__(self):
        self.conn = sqlite3.connect('english_words.db')
        self.cur = self.conn.cursor()
        # self.create()

    def __len__(self):
        return int(self.conn.execute("SELECT count(*) FROM englishWords").fetchone()[0])

    def create(self, ):
        # IF NOT EXISTS поможет при попытке повторного подключения к базе данных
        self.cur.execute("""CREATE TABLE IF NOT EXISTS englishWords(
           id INTEGER PRIMARY KEY,
           word_1 TEXT,
           word_2 TEXT,
           word_3 TEXT,
           translate_word TEXT);
        """)
        self.conn.commit()

    def addInfoDatabase(self, id, word_1, word_2, word_3, translate_word):
        words = (id, word_1, word_2, word_3, translate_word)
        if self.cur.execute("SELECT * FROM englishWords WHERE id=?", (id, )).fetchone() is None:
            self.cur.execute("INSERT OR IGNORE INTO englishWords VALUES(?, ?, ?, ?, ?);", words)
            self.conn.commit()

    def delInfoDatabase(self, item):
        print(type(item))
        if item == type(int):
            self.cur.execute(f"DELETE FROM englishWords WHERE id='{item}';")
        else:
            self.cur.execute(f"DELETE FROM englishWords WHERE word_1='{item}' or word_2='{item}' or word_3='{item}' or translate_word='{item}';")
        self.conn.commit()

    # addInfoDatabase('00004', 'Ilya', 'Ryabikov3', 'ya.ir9@ya.ru', "89102822568")

    def get_db(self, uid):
        user = self.cur.execute(f'SELECT * FROM englishWords WHERE id ={uid}').fetchone()

        if user is None:
            # self.conn.close()
            return None
        else:
            return user[1], user[2], user[3], user[4]

    def printAllTable(self, ):
        self.cur.execute("SELECT * FROM englishWords;")
        result = self.cur.fetchall()
        print('--------------------')
        for r in result:
            print(r)
        print('--------------------')


# en = englishWords()
# en.create()
# with open("f.txt") as file:
#     f = file.readlines()
#     print(f)
#     i = 0
#     while i < len(f) - 4:
#         print(int(i / 4) + 4, f[i][:-1], f[i + 1][:-1], f[i + 2][:-1], f[i + 3][:-1])
#         i += 4
#         en.addInfoDatabase(int(i / 4) + 4, f[i][:-1], f[i + 1][:-1], f[i + 2][:-1], f[i + 3][:-1])


#
# en.addInfoDatabase("0", "arise", "arose", "arisen", "возникать, появляться")
# en.delInfoDatabase(0)
# en.printAllTable()
