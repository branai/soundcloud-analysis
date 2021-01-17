import string
import sqlite3

escape_set = set('"' + "'" + '“' + '”')
escape_table = str.maketrans(dict.fromkeys(escape_set))

insert_row_save = '''INSERT OR IGNORE INTO {} VALUES ('''
create_table_save = '''CREATE TABLE IF NOT EXISTS {} ('''

class Database_Instance:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()

    def create_table(self, table_name, data_types):
        create_table = create_table_save.format(table_name)
        for i in range(len(data_types)):
            curr = data_types[i][0] + " " + data_types[i][1]
            if(data_types[i][0] == "id"):
                curr += " NOT NULL UNIQUE"
            create_table += curr + ", "
        create_table = create_table[:-2] + ")"
        self.c.execute(create_table)
        self.conn.commit()

    def query(self, q):
        try:
            self.c.execute(q)
            ids = [x for x in self.c.fetchall()]
            self.conn.commit()
            return ids
        except sqlite3.OperationalError:
            print("ERROR. Syntax error for query: " + q)
        except:
            print("ERROR. Unkown error for query: " + q)

    def add_row(self, table_name, data, data_types):
        insert_row = insert_row_save.format(table_name)
        for i in range(len(data_types)):
            curr = ""
            if(data_types[i][1] == "text"):
                curr_pre = str(data[data_types[i][0]])
                if(data_types[i][2] == 1):
                    curr_pre = curr_pre.translate(escape_table)
                curr = '"' + curr_pre + '"'
            elif(data_types[i][1] == "int" or data_types[i][1] == "real" or data_types[i][1] == "boolean"):
                if(type(data[data_types[i][0]]) is bool):
                    if(data[data_types[i][0]]):
                        curr = "1"
                    else:
                        curr = "0"
                else:
                    curr = str(data[data_types[i][0]])
            if(data[data_types[i][0]] == None):
                curr = "NULL"
            insert_row += curr + ", "
        insert_row = insert_row[:-2] + ")"
        self.query(insert_row)
