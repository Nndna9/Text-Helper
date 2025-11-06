import streamlit as st
from pathlib import Path
from text_utils import (
    to_upper, to_lower, strip_text, replace_text,
    count_substring, get_stats, add_timestamp
)

st.set_page_config(page_title="Text Helper", layout="centered")
st.title("📝 Text Helper")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file is not None:
    # Validate extension explicitly
    if Path(uploaded_file.name).suffix.lower() != ".txt":
        st.error("Only .txt files are supported.")
    else:
        mode = st.radio("Select Mode", ["Read", "Append"])

        # Load original file into session_state only once per upload
        if "uploaded_name" not in st.session_state or st.session_state.uploaded_name != uploaded_file.name:
            st.session_state.uploaded_name = uploaded_file.name
            st.session_state.text = uploaded_file.read().decode("utf-8")
            # reset other UI-related session keys
            st.session_state.replace_old = ""
            st.session_state.replace_new = ""
            st.session_state.count_sub = ""

        # --- String Tools ---
        st.subheader("🔧 String Tools (operations modify the current text)")
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

        # Replace with explicit validation
        st.write("**Replace** (only replaces if 'Old' is non-empty and found in text)")
        old_word = st.text_input("Replace → Old", value=st.session_state.get('replace_old',''), key="replace_old")
        new_word = st.text_input("Replace → New", value=st.session_state.get('replace_new',''), key="replace_new")

        if st.button("Replace"):
            if not old_word:
                st.error("Please enter the text to replace in the 'Old' field.")
            else:
                occurrences = count_substring(st.session_state.text, old_word)
                if occurrences == 0:
                    st.warning(f"'{old_word}' was not found. No replacement performed.")
                else:
                    st.session_state.text = replace_text(st.session_state.text, old_word, new_word)
                    st.success(f"Replaced {occurrences} occurrence(s) of '{old_word}' with '{new_word}'.")

        # Count occurrences
        substring = st.text_input("Count occurrences of:", value=st.session_state.get('count_sub',''), key="count_sub")
        if st.button("Count"):
            if not substring:
                st.error("Please enter a substring to count.")
            else:
                count = count_substring(st.session_state.text, substring)
                st.info(f"The substring '{substring}' appears {count} time(s).")

        # --- Preview & Stats (always reflect current session text) ---
        st.subheader("📖 Preview (First 20 lines)")
        lines = st.session_state.text.splitlines()
        preview = "\n".join(lines[:20])
        st.text_area("File Preview (read-only)", preview, height=220)

        # Stats
        line_count, word_count, char_count = get_stats(st.session_state.text)
        st.write(f"**Lines:** {line_count} | **Words:** {word_count} | **Characters:** {char_count}")

        # --- Save Option ---
        st.subheader("💾 Save Options")
        if mode == "Append":
            extra_text = st.text_area("Extra text to append", "")
            if st.button("Save Edited File"):
                final_text = st.session_state.text + "\n" + extra_text if extra_text else st.session_state.text
                final_text = add_timestamp(final_text)
                st.download_button(
                    label="Download Edited File",
                    data=final_text,
                    file_name=f"edited_{st.session_state.uploaded_name}",
                    mime="text/plain"
                )
        else:
            st.warning("Saving is disabled in Read mode.")
else:
    st.info("Please upload a .txt file to begin.")
