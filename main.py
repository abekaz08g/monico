#-*- coding:utf-8 -*-

import conf
import proc


DATABASE = proc.database(conf.DBCONF)
DATABASE.connect()
DATABASE.fetchArticles()
print 'finished!'
DATABASE.disconnect()
