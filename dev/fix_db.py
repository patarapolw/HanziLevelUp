import sqlite3


class Reader:
    def __init__(self):
        self.conn = sqlite3.connect('../webapp/user.db')

    def load_vocab(self):
        cursor = self.conn.execute('SELECT id, vocab FROM vocab')
        for row in cursor:
            yield row[1]

    def remove_whitespace(self, params):
        self.conn.execute('UPDATE vocab SET vocab=? WHERE id=?', (params[1].strip(), params[0]))

    def remove_duplicates(self):
        self.conn.execute('DELETE FROM vocab WHERE id NOT IN (SELECT MAX(id) FROM vocab GROUP BY vocab)')
        self.conn.commit()


if __name__ == '__main__':
    print(list(Reader().load_vocab()))
