import streamlit as st
from transformers import pipeline, set_seed
import random
from datetime import datetime
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="AI Dungeon Generator", layout="wide")

# --- CUSTOM STYLE ---
if os.path.exists("assets/custom.css"):
    with open("assets/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if os.path.exists("assets/banner.jpeg"):
    st.image("assets/banner.jpeg", use_container_width=True)

# --- LOAD MODEL ---
@st.cache_resource
def load_generator():
    return pipeline('text-generation', model='gpt2')

generator = load_generator()

# --- TITLE + INSTRUCTIONS ---
st.markdown("<h1> The Arcane Storyweaver</h1>", unsafe_allow_html=True)
st.markdown("Let the ancient forces shape a tale from your imagination...")



# --- SIDEBAR SETTINGS ---
st.sidebar.title("Settings")
genre = st.sidebar.selectbox("Choose a Genre", ["Fantasy", "Mystery", "Sci-fi", "Romance", "Horror"])
num_outputs = st.sidebar.slider("How many stories?", 1, 5, 2)
length = st.sidebar.slider("Story Length (tokens)", 50, 700, 300)
user_seed = st.sidebar.number_input("Seed (0 for random)", min_value=0, value=0)

# --- USER PROMPT ---
st.markdown("##  Begin Your Tale")
prompt = st.text_area("Write your opening lines:", "In a land ruled by shadows...")
st.markdown(f"#### 🔮 Genre Selected: *{genre}*")

# --- GENERATE BUTTON ---
if st.button("✨ Generate"):
    seed = user_seed if user_seed else random.randint(1, 10000)
    set_seed(seed)
    base_prompt = f"[{genre}] {prompt}\n\nThis is how the story ends:"

    st.info(f"Using seed: {seed}")

    with st.spinner("Generating your stories..."):
        results = generator(
            base_prompt,
            max_length=length,
            num_return_sequences=num_outputs,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.9
        )

    os.makedirs("stories", exist_ok=True)

    for i, r in enumerate(results):
        story = r['generated_text']
        st.subheader(f"📖 Story {i+1}")
        st.write(story)

        # Save to file
        timestamp = datetime.now().strftime('%H%M%S')
        filename = f"stories/story_{genre.lower()}_{timestamp}_{i+1}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(story)

        # Download button
        st.download_button(
            label="💾 Download this story",
            data=story,
            file_name=os.path.basename(filename),
            mime="text/plain"
        )

if os.path.exists("stories"):
    st.markdown("###  Recently Saved Stories")
    saved_files = sorted(os.listdir("stories"))[-5:]  # Show only the last 5 saved stories
    for file in saved_files:
        with open(os.path.join("stories", file), "r", encoding="utf-8") as f:
            content = f.read()
        with st.expander(file):
            st.write(content)
