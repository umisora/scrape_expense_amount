#!/usr/bin/env python3
import requests
from html.parser import HTMLParser
import time
import datetime

USER = 'xxxxxxxx'
PASS = 'xxxxxxxx'
CSRFTOKEN = None
COOKIE = None

class ExLoginHTMLParser(HTMLParser):
    matcher = "name", "csrf-token"
    csrftoken = None
    def get_csrftoken(self):
        return self.csrftoken
    def handle_starttag(self, tag, attrs):
        if tag == "meta" and self.matcher in attrs:
            self.csrftoken = attrs[1][1]

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

class ExExpenseReportHTMLParser(HTMLParser):
    matcher = "name", "csrf-token"
    thead = False
    thead_th = []
    tbody = False
    tbody_th = []
    data = []
    ptag = False

    def handle_starttag(self, tag, attrs):
        if tag == "thead":
            self.thead = True
        if tag == "tbody":
            self.tbody = True
        if tag == "p":
            self.ptag = True

    def handle_endtag(self, tag):
        if tag == "thead":
            self.thead = False
        if tag == "tbody":
            self.tbody = False
            self.data.append(self.tbody_th)
            self.tbody_th = [] #初期化
        if tag == "p":
            self.ptag = False

    def handle_data(self, data):
        # 条件によって出力するptagの要素は捨ててしまう
        if self.thead and not self.ptag:
            # print(data)
            self.thead_th.append(data)
        if self.tbody and not self.ptag:
            # print(data)
            self.tbody_th.append(data)

URL='https://expense.moneyforward.com'
headers = {"User-Agent": "UmiSora"}

## CSFR-TOKEN取得
session = requests.session()
resp = session.get(URL+'/session/new', timeout=1, headers=headers)
COOKIE = resp.cookies
#print(resp.status_code)
#print(resp.text)
parser = ExLoginHTMLParser()
parser.feed(resp.text)
CSRFTOKEN = parser.get_csrftoken()

## ログイン処理
login_data = {
   'UTF-8': '✓',
   'sign_in_session_service[email]': USER,
   'sign_in_session_service[password]': PASS,
   'commit': 'ログインする',
   'authenticity_token': CSRFTOKEN
}
session.post('https://expense.moneyforward.com/session', data=login_data, cookies=COOKIE)
resp = session.get('https://expense.moneyforward.com/expense_reports')
parser = ExExpenseReportHTMLParser()
parser.feed(resp.text)
expense_datas = parser.data

message = ""
for expense_data in expense_datas:
    expense_no = expense_data[0] #経費番号
    expense_created_date = expense_data[1] #申請作成日
    expense_title = expense_data[2] #タイトル
    expense_status = expense_data[3] #ステータス
    expense_sum_amount = expense_data[4] #合計金額
    expense_approver = expense_data[5] # 承認者
    expense_approve_date = expense_data[6] # 承認日
    expense_payment_date = expense_data[7] # 支払日
    # 支払日がみらいのものだけ
    if datetime.datetime.now() < datetime.datetime.strptime(expense_payment_date, "%Y/%m/%d"):
        message += "\n" + expense_payment_date + "に" + expense_sum_amount + "の支払いが予定されています。"

if message == "":
    return_message = "あなたに直近支払いのある経費は0件です。"
else:
    return_message = "あなたに直近支払いのある経費は" + message

print(return_message)
output = {"message":return_message}
