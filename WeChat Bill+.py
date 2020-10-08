import csv
import os
import re

# for QPython
os.chdir(os.path.dirname(__file__))

# bill file name: 微信支付账单(20121231-20130331)
date = r'20\d\d(?:0[1-9]|1[0-2])(?:0[1-9]|[12][0-9]|3[01])'
pattern = rf'微信支付账单\({date}-{date}\)\.csv'
bill_list = [_ for _ in os.listdir() if re.match(pattern, _)]

bill, time = set(), [[], [], []]
for b in bill_list:
    with open(b, 'r', encoding='utf-8-sig', newline='') as f:
        f = f.read().splitlines()
    for i, v in enumerate([f[2][6:25], f[2][33:52], f[4][6:25]]):
        time[i].append(v)
    for _ in csv.reader(f[17:]):  # bill data start on line 18
        bill.add(tuple(_))
bill = list(bill)

for _ in (bill, *time):  # batch sort
    _.sort(reverse=True)

# may be overlap, need update
count = [[0, 0], [0, 0], [0, 0]]
for b in bill:
    for i, s in enumerate(['收入', '支出', '/']):
        if b[4] == s:
            count[i][0] += 1
            count[i][1] += float(b[5][1:])

head = f"""微信支付账单明细,,,,,,,,
微信昵称：[{f[1][6:-9]}],,,,,,,,
起始时间：[{time[0][-1]}] 终止时间：[{time[1][0]}],,,,,,,,
导出类型：[全部],,,,,,,,
导出时间：[{time[2][0]}],,,,,,,,
,,,,,,,,
共{count[0][0]+count[1][0]+count[2][0]}笔记录,,,,,,,,
收入：{count[0][0]}笔 {count[0][1]}元,,,,,,,,
支出：{count[1][0]}笔 {count[1][1]}元,,,,,,,,
中性交易：{count[2][0]}笔 {count[2][1]}元,,,,,,,,
注：,,,,,,,,
1. 充值/提现/理财通购买/零钱通存取/信用卡还款等交易，将计入中性交易,,,,,,,,
2. 本明细仅展示当前账单中的交易，不包括已删除的记录,,,,,,,,
3. 本明细仅供个人对账使用,,,,,,,,
,,,,,,,,
----------------------微信支付账单明细列表--------------------,,,,,,,,
交易时间,交易类型,交易对方,商品,收/支,金额(元),支付方式,当前状态,交易单号,商户单号,备注
"""

with open('WeChat.csv', 'w', encoding='utf-8-sig', newline='') as f:
    f.write(head)
    f = csv.writer(f)
    f.writerows(bill)
