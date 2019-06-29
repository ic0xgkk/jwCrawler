import pymysql


class Database(object):

    def __init__(self, host: str, user: str, password: str, database: str, port: int):

        try:
            self.conn = pymysql.connect(host=host, user=user, password=password,
                                        database=database, port=port)
        except pymysql.Error:
            raise pymysql.Error("Something with wrong, failed to connect database")

    def __del__(self):
        self.conn.close()

    def course_to_db(self, jx0404id, xf, dwmc, jx02id, xkrs, zxs, sksj, xxrs, szkcflmc,
                     syrs, kcmc, skls, skdd, kindName, classKind):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO course("
                               "jx0404id, xf, dwmc, jx02id, xkrs, zxs, sksj, xxrs, "
                               "szkcflmc, syrs, kcmc, skls, skdd, kindName, classKind) "
                               "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s',"
                               "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                                str(jx0404id), str(xf), str(dwmc), str(jx02id), str(xkrs), str(zxs),
                                str(sksj), str(xxrs), str(szkcflmc), str(syrs), str(kcmc), str(skls),
                                str(skdd), str(kindName), str(classKind)))
                self.conn.commit()
            except pymysql.Error:
                raise pymysql.Error("Failed to insert data")
            cursor.close()



