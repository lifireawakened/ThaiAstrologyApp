import streamlit as st
import google.generativeai as genai

# --- 設定頁面 ---
st.set_page_config(page_title="泰國皇家占星", page_icon="🙏")

# --- 這裡貼上剛剛在 AI Studio 拿到的 API Key ---
# 注意：真實發布時不能這樣直接貼，但新手練習可以先這樣做
GOOGLE_API_KEY = "AIzaSyAZsA2l0Qv07VDHGfTKAHTSWPMMCLJ59J4"

# --- 設定 AI 大腦 ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash') # 使用強大的 Gemini Pro 模型
except Exception as e:
    st.error("API Key 設定有誤，請檢查代碼。")

# --- 設定大師的靈魂 (System Instruction) ---
master_instruction = """
你是一位專業的「泰國占星大師」。
請根據用戶的輸入，進行詳細的命盤解析。
輸出格式要求：
1. 使用 Markdown 格式。
2. 包含【九宮格位解析】表格。
3. 包含【人生軌距】分析。
4. 給出具體的【泰國改運建議】。
語氣要慈悲、專業、權威。
"""

# --- 網頁介面設計 (前端) ---
st.title("🇹🇭 泰國皇家九宮占星 APP")
st.markdown("### 薩瓦迪卡，有緣人。請輸入您的生辰，讓大師為您指引迷津。")

# 建立側邊欄讓用戶輸入資料
with st.sidebar:
    st.header("輸入生辰資料")
    birth_date = st.date_input("出生日期")
    birth_time = st.time_input("出生時間")
    birth_place = st.text_input("出生地點 (例如：台北市)")
    
    # 按鈕
    submit_btn = st.button("開始解讀命盤")

# --- 按下按鈕後的動作 ---
if submit_btn:
    if not birth_place:
        st.warning("請輸入出生地點。")
    else:
        with st.spinner("大師正在推算星盤，請稍候..."):
            # 1. 整理用戶資料
            user_data = f"用戶資料：出生日期 {birth_date}, 時間 {birth_time}, 地點 {birth_place}。請為我算命。"
            
            # 2. 發送給 Gemini
            try:
                chat = model.start_chat(history=[
                    {"role": "user", "parts": master_instruction},
                    {"role": "model", "parts": "好的，我明白了。我是泰國占星大師，請提供用戶資料。"}
                ])
                response = chat.send_message(user_data)
                
                # 3. 顯示結果
                st.success("解讀完成！")
                st.markdown("---")
                st.markdown(response.text) # 顯示 AI 的回答
                
            except Exception as e:
                st.error(f"連線發生錯誤：{e}")
                st.info("請檢查您的 API Key 是否正確，或網路是否通暢。")

# --- 頁尾 ---
st.markdown("---")

st.caption("© 2024 泰國占星大師 | Powered by Google Gemini AI")

