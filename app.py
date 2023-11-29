import streamlit as st
import os
import random

# Function to load markdown files1
def load_markdown_files(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                files.append((filename, file.read()))
    return files

# Function to extract key sentences
def extract_key_sentences(content, filename):
    key_sentences = []
    lines = content.split('\n')
    capture = False
    for line in lines:
        if line.startswith("5 Key Sentences:"):
            capture = True
            continue
        if capture:
            if line.strip().startswith(tuple("12345.")):
                key_sentences.append((line, filename))
            else:
                break
    return key_sentences

# Load notes once and store in session state
if 'notes' not in st.session_state:
    content_dir = "./content"  # Update with the path to your content directory
    st.session_state['notes'] = load_markdown_files(content_dir)
    st.session_state['current_note'] = None
    st.session_state['view_note'] = False

# Set up the Streamlit app
st.title("Poor Man's Founders Notes")
st.markdown("[Go to the podcast page for the full transcripts](https://www.joincolossus.com/episodes?prod-episode-release-desc%5BrefinementList%5D%5BpodcastName%5D%5B0%5D=Founders)", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
selected_option = st.sidebar.selectbox("Choose an option", ["Note Index", "Key Sentences Feed", "Random Summary"])

def display_note_content():
    note_content = next((content for (filename, content) in st.session_state['notes'] if filename == st.session_state['current_note']), "")
    st.markdown(note_content, unsafe_allow_html=True)
    if st.button("Back to Key Sentences"):
        st.session_state['view_note'] = False

if selected_option == "Note Index":
    selected_note = st.selectbox("Select a note", [note[0] for note in st.session_state['notes']])
    st.session_state['current_note'] = selected_note
    display_note_content()

elif selected_option == "Key Sentences Feed":
    all_key_sentences = [sentence for _, content in st.session_state['notes'] for sentence in extract_key_sentences(content, _)]
    random.shuffle(all_key_sentences)

    for idx, (sentence, filename) in enumerate(all_key_sentences):
        st.write(sentence)
        if st.button("View Note", key=f"btn_{idx}"):
            st.session_state['current_note'] = filename
            st.session_state['view_note'] = True
            break

elif selected_option == "Random Summary":
    random_note = random.choice(st.session_state['notes'])
    st.session_state['current_note'] = random_note[0]
    display_note_content()

if st.session_state['view_note']:
    display_note_content()
