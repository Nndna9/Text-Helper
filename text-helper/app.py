import streamlit as st
from pathlib import Path
from text_utils import (
    to_upper, to_lower, strip_text, replace_text,
    count_substring, get_stats, add_timestamp
)

st.title("📝 Text Helper")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file is not None:
    if Path(uploaded_file.name).suffix != ".txt":
        st.error("Only .txt files are supported.")
    else:
        mode = st.radio("Select Mode", ["Read", "Append"])

        # Initialize session state
        if "text" not in st.session_state:
            st.session_state.text = uploaded_file.read().decode("utf-8")

        text = st.session_state.text

        # --- Preview ---
        lines = text.splitlines()
        preview = "\n".join(lines[:20])
        st.subheader("📖 Preview (First 20 lines)")
        st.text_area("File Preview", preview, height=200)

        # --- Stats ---
        line_count, word_count, char_count = get_stats(text)
        st.write(f"**Lines:** {line_count} | **Words:** {word_count} | **Characters:** {char_count}")

        # --- String Tools ---
        st.subheader("🔧 String Tools")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("UPPERCASE"):
                st.session_state.text = to_upper(st.session_state.text)

        with col2:
            if st.button("lowercase"):
                st.session_state.text = to_lower(st.session_state.text)

        with col3:
            if st.button("strip"):
                st.session_state.text = strip_text(st.session_state.text)

        old_word = st.text_input("Replace → Old")
        new_word = st.text_input("Replace → New")

        if st.button("Replace"):
            st.session_state.text = replace_text(st.session_state.text, old_word, new_word)
            st.success(f"Replaced '{old_word}' with '{new_word}'")

        substring = st.text_input("Count occurrences of:")
        if st.button("Count"):
            count = count_substring(st.session_state.text, substring)
            st.info(f"The substring '{substring}' appears {count} times.")

        # --- Save Option ---
        st.subheader("💾 Save Options")
        if mode == "Append":
            extra_text = st.text_area("Extra text to append", "")
            if st.button("Save Edited File"):
                final_text = st.session_state.text + "\n" + extra_text
                final_text = add_timestamp(final_text)
                st.download_button(
                    label="Download Edited File",
                    data=final_text,
                    file_name="edited_text.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Saving is disabled in Read mode.")
else:
    st.info("Please upload a .txt file to begin.")

