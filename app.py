import streamlit as st
from google import genai
from PIL import Image

# Cấu hình trang
st.set_page_config(page_title="Forex Desk AI", page_icon="FX", layout="centered")

st.markdown("### 🟩 Forex Desk AI")
st.markdown("---")

api_key = st.sidebar.text_input("Nhập Gemini API Key:", type="password")
st.sidebar.markdown("*Lấy key miễn phí tại Google AI Studio*")

tab1, tab2, tab3 = st.tabs(["Tin tức", "Phân tích chart", "Lịch sử"])

# ================= TAB 1: PHÂN TÍCH TIN TỨC =================
with tab1:
    st.write("**Dán nội dung chữ HOẶC dán ảnh chụp tin tức (Ctrl+V vào ô dưới)**")
    news_content = st.text_area("Nội dung", placeholder="Vd: Fed giữ nguyên lãi suất...", height=100, label_visibility="collapsed")
    news_img_file = st.file_uploader("Tải ảnh/Paste ảnh", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    
    btn_news = st.button("Phân tích tin tức", type="primary", use_container_width=True)

    if btn_news:
        if not api_key:
            st.error("⚠️ Vui lòng nhập API Key ở menu bên trái.")
        elif not news_content and not news_img_file:
            st.warning("⚠️ Vui lòng nhập chữ hoặc dán ảnh tin tức.")
        else:
            with st.spinner("AI đang đọc tin..."):
                try:
                    client = genai.Client(api_key=api_key)
                    contents = []
                    
                    if news_img_file:
                        contents.append(Image.open(news_img_file))
                    if news_content:
                        contents.append(news_content)
                        
                    sys_prompt = "Là chuyên gia Forex, hãy phân tích tác động của tin tức này (Tăng/Giảm rủi ro, cặp tiền bị ảnh hưởng). Trả lời ngắn gọn, súc tích."
                    contents.append(sys_prompt)

                    response = client.models.generate_content(model='gemini-1.5-flash', contents=contents)
                    st.success("Kết quả:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Lỗi: {e}")

# ================= TAB 2: PHÂN TÍCH CHART =================
with tab2:
    st.write("**Dán ảnh chụp biểu đồ (Nhấp chuột vào ô dưới rồi ấn Ctrl+V)**")
    chart_file = st.file_uploader("Tải ảnh/Paste ảnh biểu đồ", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
    
    chart_context = st.text_input("Bối cảnh", placeholder="Vd: XAU/USD khung H1, đang cân nhắc Buy...", label_visibility="collapsed")
    btn_chart = st.button("Phân tích chart", type="primary")

    if btn_chart:
        if not api_key:
            st.error("⚠️ Vui lòng nhập API Key.")
        elif not chart_file:
            st.warning("⚠️ Vui lòng dán ảnh biểu đồ.")
        else:
            with st.spinner("AI đang soi chart..."):
                try:
                    client = genai.Client(api_key=api_key)
                    img = Image.open(chart_file)
                    sys_prompt = f"Là chuyên gia Phân tích Kỹ thuật Forex. Dựa vào ảnh biểu đồ và bối cảnh: '{chart_context}'. Đưa ra góc nhìn ngắn gọn, súc tích nhất."     
                    response = client.models.generate_content(model='gemini-1.5-flash', contents=[img, sys_prompt])
                    st.success("Góc nhìn từ AI:")
                    st.write(response.text)
            except Exception as e:
                error_msg = str(e)
                if "503" in error_msg:
                    st.warning("⚠️ Máy chủ AI đang tạm quá tải. Bạn ráng đợi khoảng 30 giây rồi bấm nút phân tích lại nhé!")
                elif "429" in error_msg:
                    st.warning("⏳ API Key đang bị giới hạn lượt hỏi liên tục. Vui lòng đợi 1 phút rồi thử lại nha!")
                else:
                    st.error(f"Có lỗi xảy ra: {error_msg}")
            st.write(response.text)
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg:
                st.warning("⚠️ Máy chủ AI đang tạm quá tải. Bạn ráng đợi khoảng 30 giây rồi bấm nút phân tích lại nhé!")
            elif "429" in error_msg:
                st.warning("⏳ API Key đang bị giới hạn lượt hỏi liên tục. Vui lòng đợi 1 phút rồi thử lại nha!")
            else:
                st.error(f"Có lỗi xảy ra: {error_msg}")

# ================= TAB 3: LỊCH SỬ =================
with tab3:
    st.info("Tính năng lưu lịch sử sẽ được cập nhật trong phiên bản sau.")
