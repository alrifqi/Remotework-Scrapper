# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import requests
from remoteworkscrapper.settings import MAILGUN

class RemoteworkscrapperPipeline(object):
    def __init__(self):
        self.setupDBCon()
        self.createWorkTable()
        self.newjob = ''
        self.mailgun_key = MAILGUN['key']
        self.mailgun_requrl = 'https://api.mailgun.net/v2/{0}/messages'.format(MAILGUN['sandbox'])

    def process_item(self, item, spider):
        self.storeToDb(item)
        return item

    def close_spider(self, spider):
        self.sendEmail(self.newjob)
        self.newjob = ''

    def setupDBCon(self):
        self.con = sqlite3.connect('./test.db')
        self.cur = self.con.cursor()

    def createWorkTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS work(id INTEGER PRIMARY KEY NOT NULL, title TEXT, description TEXT, url TEXT, company TEXT, source TEXT)")


    def storeToDb(self, item):
        if not self.checkData(item):
            self.cur.execute("INSERT INTO work(title, description, url, company, source) VALUES(?,?,?,?,?)",
                             (item.get('title',''),
                              item.get('desc',''),
                              item.get('url',''),
                              item.get('company',''),
                              item.get('source','')
                              ))
            self.con.commit()
            self.rememberNew(item.get('title'), item.get('url'))

    def closeDb(self):
        self.con.close()

    def checkData(self, item):
        self.cur.execute("SELECT id FROM work WHERE title=? AND company=?", (item.get('title'), item.get('company')))
        data = self.cur.fetchall()
        if len(data)==0:
            return False
        return True

    def rememberNew(self, title, url):
        self.newjob += "<li>"+title + " (<a href='"+url+"'>"+ url +"</a>) </li> \n"

    def sendEmail(self, data):
        request = requests.post(self.mailgun_requrl, auth=('api', self.mailgun_key), data={
            'from': 'hello@remoteworkscrapper.com',
            'to': MAILGUN['email_receiver'],
            'subject': 'New Remote Work',
            'html': "<html><body><ol>"+data+"</ol></body></html>"
        })