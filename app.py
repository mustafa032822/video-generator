import streamlit as st
from moviepy.editor import ImageClip, vfx
import os

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Image to Video Generator", layout="wide", page_icon="🖼️")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .stButton>button { 
        background: linear-gradient(90deg, #f472b6 0%, #db2777 100%); 
        color: white; border-radius: 12px; height: 3.5rem; font-size: 1.2rem; font-weight: bold; width: 100%; border: none;
    }
    .download-section { 
        background-color: #1e293b; border: 1px solid #f472b6; padding: 20px; border-radius: 15px; margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🖼️ Image to Video Generator")
st.write("حول صورك الثابتة إلى فيديوهات سينمائية بدقة عالية")

# --- الإعدادات الجانبية ---
with st.sidebar:
    st.header("⚙️ إعدادات الفيديو")
    duration = st.slider("مدة الفيديو (بالثواني)", 2, 10, 5)
    fps = st.select_slider("سلاسة الفيديو (FPS)", options=[24, 30, 60], value=30)
    motion_effect = st.checkbox("إضافة تأثير الحركة الذكية (Zoom In)", value=True)

# --- منطقة رفع الصور ---
uploaded_image = st.file_uploader("قم برفع الصورة هنا", type=["jpg", "jpeg", "png"])

if uploaded_image:
    # عرض الصورة الأصلية
    st.image(uploaded_image, caption="الصورة الأصلية", width=400)
    
    if st.button("توليد الفيديو وتحميله 🚀"):
        # حفظ الصورة مؤقتاً
        img_path = "temp_image.png"
        with open(img_path, "wb") as f:
            f.write(uploaded_image.getbuffer())
        
        output_video = "image_to_video.mp4"
        
        with st.spinner('جاري معالجة الصورة وتحويلها إلى فيديو عالي الجودة...'):
            try:
                # 1. إنشاء كليب من الصورة بالمدة المحددة
                clip = ImageClip(img_path).set_duration(duration)
                
                # 2. إضافة تأثير الحركة (Zoom Effect) إذا تم اختياره
                if motion_effect:
                    # تقنية تحريك الصورة لجعلها تبدو كفيديو
                    clip = clip.fx(vfx.resize, lambda t: 1 + 0.02*t) # تكبير تدريجي بسيط
                
                # 3. ضبط التردد (FPS) والجودة
                clip = clip.set_fps(fps)
                
                # 4. التصدير بجودة عالية
                clip.write_videofile(output_video, codec="libx264", bitrate="8000k")
                clip.close()
                
                # --- عرض النتيجة والتحميل ---
                st.markdown('<div class="download-section">', unsafe_allow_html=True)
                st.subheader("✅ تم توليد الفيديو بنجاح")
                st.video(output_video)
                
                with open(output_video, "rb") as file:
                    st.download_button(
                        label="📥 تحميل الفيديو الآن",
                        data=file,
                        file_name="generated_from_image.mp4",
                        mime="video/mp4"
                    )
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")

        st.balloons()
