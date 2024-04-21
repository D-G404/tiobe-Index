import pandas as pd
import bar_chart_race as bcr
df = pd.read_csv('test.csv', index_col=0) #倒入数据
bcr.bar_chart_race(df, 'test.gif')  #默认保持mp4格式，bar_chart_race会根据后缀决定保存格式

