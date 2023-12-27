from pypinyin import lazy_pinyin
import pandas as pd
import re


df = pd.read_excel(r"C:\Users\19561\Desktop\web开发-hospital\department.xlsx")
data = []

for index, row in df.iterrows():
    department = row['科室名称']
    illnesses = row['对应疾病'].split(',')

    for illness in illnesses:
        x1 = lazy_pinyin(illness)
        first_letter = x1[0][0].lower() if x1[0][0].isalpha() else '#'
        data.append([first_letter, illness.strip(), department])

new_df = pd.DataFrame(data, columns=['alphabet', 'illness', 'department'])
new_df.to_excel(r"C:\Users\19561\Desktop\web开发-hospital\illness.xlsx", index=False)


