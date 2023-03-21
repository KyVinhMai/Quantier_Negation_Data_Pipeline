import sqlite3


con = sqlite3.connect("D:\AmbiLab_data\quant_neg_data.db")
cur = con.cursor()

# sql_query = "INSERT INTO person VALUES(?, ?)"
# sql_data = ("Karl", "Marx")
# cur.execute(sql_query, sql_data)
iteral = cur.execute("""SELECT * FROM links WHERE batches = 1;""")
con.commit()
for i in iteral:
    print(i[0], i[1])
# print(type(cur.fetchone()))

# try:
#     cur.execute(sql_query, sql_data)
#     con.commit()
# except sqlite3.Error as er:
#     print("_" * 40)
#     print("@", (' '.join(er.args)), "@")
#     print("_" * 40)
#
#     # print('SQLite error: %s' % (' '.join(er.args)))
#     # print("Exception class is: ", er.__class__)
#     # print('SQLite traceback: ')
#     # exc_type, exc_value, exc_tb = sys.exc_info()
#     # print(traceback.format_exception(exc_type, exc_value, exc_tb))



con.close()