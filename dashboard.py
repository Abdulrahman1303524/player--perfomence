import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

# إعدادات الصفحة
st.set_page_config(page_title="مقارنة اللاعبين", layout="wide")
st.title("⚽ لوحة مقارنة أداء اللاعبين")
st.markdown("اختر لاعبين من القائمة لمقارنة أدائهما في نهائي كأس العالم 2022.")

# تحميل البيانات (يتم تخزينها مؤقتاً لتسريع الموقع)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/3788741.json"
    df = pd.DataFrame(requests.get(url).json())
    # استخراج أسماء اللاعبين المتاحين
    players = df['player'].dropna().apply(lambda x: x['name']).unique()
    return df, sorted(players)

df, players_list = load_data()

# القائمة المنسدلة لاختيار اللاعبين
col1, col2 = st.columns(2)
with col1:
    player1 = st.selectbox("اللاعب الأول:", players_list, index=players_list.index("Lionel Andrés Messi Cuccittini"))
with col2:
    player2 = st.selectbox("اللاعب الثاني:", players_list, index=players_list.index("Kylian Mbappé Lottin"))

# فلترة البيانات للاعبين المختارين
df_p1 = df[df['player'].apply(lambda x: x['name'] if pd.notna(x) else '') == player1]
df_p2 = df[df['player'].apply(lambda x: x['name'] if pd.notna(x) else '') == player2]

# حساب الإحصائيات
shots_p1 = len(df_p1[df_p1['type'].apply(lambda x: x['name']) == 'Shot'])
shots_p2 = len(df_p2[df_p2['type'].apply(lambda x: x['name']) == 'Shot'])

# عرض الإحصائيات في أعمدة
st.subheader("📊 الإحصائيات الأساسية")
stat_col1, stat_col2 = st.columns(2)
stat_col1.metric(label=f"تسديدات {player1.split()[-1]}", value=shots_p1)
stat_col2.metric(label=f"تسديدات {player2.split()[-1]}", value=shots_p2)

# رسم الخريطة الحرارية
st.subheader("🔥 الخريطة الحرارية (أماكن التواجد)")

def get_coords(player_df):
    x = [loc[0] for loc in player_df['location'] if isinstance(loc, list)]
    y = [loc[1] for loc in player_df['location'] if isinstance(loc, list)]
    return x, y

x1, y1 = get_coords(df_p1)
x2, y2 = get_coords(df_p2)

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 7))
fig.patch.set_facecolor('#1c2531')

# الملعب الأول
pitch1 = Pitch(pitch_type='statsbomb', pitch_color='#1c2531', line_color='#e1e1e1')
pitch1.draw(ax=axs[0])
axs[0].hexbin(x1, y1, gridsize=15, cmap='Blues', alpha=0.8, mincnt=1)
axs[0].set_title(player1, color='white', fontsize=16)

# الملعب الثاني
pitch2 = Pitch(pitch_type='statsbomb', pitch_color='#1c2531', line_color='#e1e1e1')
pitch2.draw(ax=axs[1])
axs[1].hexbin(x2, y2, gridsize=15, cmap='Reds', alpha=0.8, mincnt=1)
axs[1].set_title(player2, color='white', fontsize=16)

plt.tight_layout()
# عرض الرسم البياني في Streamlit
st.pyplot(fig)
