import streamlit as st
from ner import perform_ner
import os
import pandas as pd

def save_uploaded_file(uploaded_file):
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def main():
    st.set_page_config(page_title="📄 Advanced NER from PDF", layout="wide")

    # Custom Styling
    st.markdown(
        """
        <style>
        .main-title {font-size: 50px; color: #4CAF50; text-align: center;}
        
        .entity-table {border-radius: 10px; overflow: hidden;}
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown('<h1 class="main-title">📄 Named Entity Recognition from PDF</h1>', unsafe_allow_html=True)
    st.markdown("#### Extract named entities with AI-powered accuracy in seconds!")
    
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"], help="Choose a PDF file for entity extraction.")
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        st.success("✅ File Uploaded Successfully")
        file_path = save_uploaded_file(uploaded_file)
        entities = perform_ner(file_path)

        if entities:
            st.success(f"🔎 Named Entities Extracted Successfully!")
            st.write(f"Total Entities Found: **{len(entities)}**")

            df = pd.DataFrame(entities, columns=["Entity", "Label"])

            # Filter option with better UI
            unique_labels = df['Label'].unique()
            selected_label = st.selectbox(
                "✨ Filter by Entity Type", ['All'] + list(unique_labels),
                index=0
            )

            filtered_df = df if selected_label == 'All' else df[df['Label'] == selected_label]

            # Display styled dataframe
            st.markdown('<div class="entity-table">', unsafe_allow_html=True)
            st.dataframe(filtered_df.style.set_properties(**{'text-align': 'left'}))
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ No Named Entities Found")

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    main()