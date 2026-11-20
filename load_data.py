import requests
import pandas as pd
import matplotlib.pyplot as plt

# 1. تحميل البيانات
url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/3869685.json"
print("Loading data...")
response = requests.get(url)
df = pd.DataFrame(response.json())

# 2. اختيار اللاعبين
player1_name = "Lionel Andrés Messi Cuccittini"
player2_name = "Kylian Mbappé Lottin"

# 3. فلترة البيانات
player1_df = df[df['player'].apply(lambda x: x['name'] if pd.notna(x) else '') == player1_name]
player2_df = df[df['player'].apply(lambda x: x['name'] if pd.notna(x) else '') == player2_name]

# 4. حساب التسديدات
shots1 = len(player1_df[player1_df['type'].apply(lambda x: x['name']) == 'Shot'])
shots2 = len(player2_df[player2_df['type'].apply(lambda x: x['name']) == 'Shot'])

# 5. تجهيز البيانات للرسم البياني
players = ['Messi', 'Mbappé']
shots = [shots1, shots2]

# 6. إنشاء الرسم البياني
plt.figure(figsize=(8, 6)) # تحديد حجم الشاشة
bars = plt.bar(players, shots, color=['#75aadb', '#002654']) # ألوان الأرجنتين وفرنسا

# إضافة الأرقام فوق الأعمدة
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.title('Total Shots in the Match', fontsize=16)
plt.ylabel('Number of Shots', fontsize=12)
plt.xlabel('Players', fontsize=12)
plt.ylim(0, 10) # جعل المحور الصادي يبدأ من 0 وينتهي عند 10 ليتناسب مع الأرقام

# إظهار الرسم البياني
plt.show()