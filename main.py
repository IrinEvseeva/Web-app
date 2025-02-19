import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📈 Анализ котировок Apple")
st.write("Данные загружаются автоматически из указанного файла.")

# 📂 Шаг 1: Загрузка CSV-файла по пути
file_path = "/Users/irinaevseeva/DS_bootcamp/week_3_day_2/Web-app/tips.csv"
#
try:
    df = pd.read_csv(file_path)
    st.success("✅ Файл успешно загружен!")
    st.write("📊 Первые 5 строк данных:")
    st.write(df.head())

except FileNotFoundError:
    st.error(f"❌ Файл по пути {file_path} не найден!")
    st.stop()

# 🔍 Шаг 2: Проверка пропущенных значений
missed_values = df.isna().sum()
missed_values = missed_values[missed_values > 0]

if len(missed_values) > 0:
    st.warning("⚠️ В данных есть пропуски!")
    
    # Визуализация пропусков
    fig, ax = plt.subplots()
    sns.barplot(x=missed_values.index, y=missed_values.values, ax=ax)
    ax.set_title("Пропущенные значения по столбцам")
    ax.set_ylabel("Количество пропусков")
    plt.xticks(rotation=45)
    
    st.pyplot(fig)

    # 🔧 Шаг 3: Заполнение пропусков
    if st.button("Заполнить пропуски"):
        df_filled = df.copy()

        for col in missed_values.index:
            if df_filled[col].dtype == "object": 
                df_filled[col].fillna(df_filled[col].mode()[0], inplace=True)
            else: 
                df_filled[col].fillna(df_filled[col].median(), inplace=True)

        st.success("✅ Пропуски заполнены!")
        st.write(df_filled.head())

        # 🔽 Шаг 4: Скачать заполненный файл
        st.download_button(
            label="📥 Скачать CSV с заполненными пропусками",
            data=df_filled.to_csv(index=False),
            file_name="filled_data.csv",
            mime="text/csv"
        )

else:
    st.success("✅ В данных нет пропусков!")