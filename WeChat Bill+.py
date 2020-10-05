import csv
import os
import re

# 适配 QPython
os.chdir(os.path.dirname(__file__))

# 识别账单文件。形如 微信支付账单(20121231-20130331)
date = r'20\d\d(?:0[1-9]|1[0-2])(?:0[1-9]|[12][0-9]|3[01])'
pattern = rf'微信支付账单\({date}-{date}\)\.csv'
bill_list = [_ for _ in os.listdir() if re.match(pattern, _)]

# 读取全部。获取时间信息、去重、排序
time = [[], [], []]


def read(_):
    global f
    with open(_, 'r', encoding='utf-8-sig', newline='') as f:
        f = f.read().splitlines()
        time[0].append(f[2][6:25])
        time[1].append(f[2][33:52])
        time[2].append(f[4][6:25])
        return f


bill = list({
    # 数据从第 18 行开始
    tuple(_) for b in bill_list for _ in csv.reader(read(b)[17:])
})
for _ in (bill, *time):  # 批量排序
    _.sort(reverse=True)

# 可能存在重叠部分，[笔数] 和 [金额] 需重新计算
count = [[0, 0], [0, 0], [0, 0]]
for b in bill:
    for i, s in (0, '收入'), (1, '支出'), (2, '/'):
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
