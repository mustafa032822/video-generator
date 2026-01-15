import streamlit as st
from moviepy.editor import VideoFileClip, vfx
import os

# --- إعدادات الصفحة والستايل ---
st.set_page_config(page_title="Generator AI - Pro Studio", layout="wide", page_icon="🎥")

# تصحيح الخطأ هنا: تم تغيير unsafe_allow_config إلى unsafe_allow_html
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .stButton>button { 
        background: linear-gradient(90deg, #38bdf8 0%, #3b82f6 100%); 
        color: white; border-radius: 12px; height: 3.5rem; font-size: 1.2rem; font-weight: bold; width: 100%; border: none;
    }
    .download-section { 
        background-color: #1e293b; border: 1px solid #38bdf8; padding: 20px; border-radius: 15px; margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 GENERATOR AI")
st.write("حول فيديو واحد إلى نسخ متعددة بجودة فائقة مع الحفاظ على صوتك الأصلي")

# --- الإعدادات الجانبية ---
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    num_versions = st.number_input("كم نسخة تريد خلقها؟", min_value=1, max_value=50, value=1)
    quality = st.selectbox("الدقة النهائية", ["High Definition (1080p)", "Ultra HD (4K Quality)"])
    st.info("سيقوم النظام بالحفاظ على الموسيقى الأصلية للفيديو.")

# --- منطقة الرفع ---
uploaded_file = st.file_uploader("قم بسحب وإفلات الفيديو هنا", type=["mp4", "mov", "avi"])

if uploaded_file:
    if st.button("بدء عملية التوليد والتحميل ✨"):
        # حفظ الفيديو المرفوع
        input_name = "input_original.mp4"
        with open(input_name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        for i in range(int(num_versions)):
            output_name = f"generated_video_v{i+1}.mp4"
            
            with st.spinner(f'جاري إنتاج النسخة رقم {i+1}...'):
                try:
                    clip = VideoFileClip(input_name)
                    
                    # خلق تنوع في الألوان
                    variation = 1.0 + (i * 0.05)
                    processed = clip.fx(vfx.colorx, variation).fx(vfx.lum_contrast, 5, 20)
                    
                    # الجودة
                    bit_rate = "18000k" if "4K" in quality else "6000k"
                    
                    # التصدير
                    processed.write_videofile(output_name, codec="libx264", audio_codec="aac", bitrate=bit_rate)
                    clip.close()
                    processed.close()
                    
                    # عرض النتيجة وزر التحميل
                    st.markdown('<div class="download-section">', unsafe_allow_html=True)
                    st.subheader(f"🎬 النسخة {i+1} جاهزة")
                    st.video(output_name)
                    
                    with open(output_name, "rb") as file:
                        st.download_button(
                            label=f"📥 تحميل النسخة {i+1}",
                            data=file,
                            file_name=output_name,
                            mime="video/mp4",
                            key=f"btn_{i}"
                        )
                    st.markdown('</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"حدث خطأ في معالجة النسخة {i+1}: {e}")
                
        st.balloons()
