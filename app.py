import streamlit as st
import os
from PIL import Image
import imagehash

st.set_page_config(page_title="Gitarren Logo Datenbank", layout="wide")

st.title("🎸 Classical Guitar Logo Database")

# Ordner-Pfade
UPLOAD_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "guitar_app", "screenshots")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Duplikate Prüffunktion
def is_duplicate(new_img):
    new_hash = imagehash.phash(new_img)
    for filename in os.listdir(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, filename)
        try:
            existing_img = Image.open(file_path)
            existing_hash = imagehash.phash(existing_img)
            # Wenn sich die Bilder zu 90%+ ähneln (Hash-Distanz < 8)
            if new_hash - existing_hash < 8:
                return True, filename
        except Exception:
            continue
    return False, None

# TAB NAVIGATION
tab1, tab2 = st.tabs(["📤 Foto Hochladen (Handy/PC)", "🔍 Logo Katalog & Suche"])

with tab1:
    st.header("Neues Logo Screenshot hochladen")
    uploaded_file = st.file_uploader("Wähle ein Bild aus deiner Galerie", type=["jpg", "png", "jpeg", "webp"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Vorschau", width=300)
        
        if st.button("In Datenbank speichern"):
            duplicate, dup_filename = is_duplicate(image)
            if duplicate:
                st.error(f"❌ Abgelehnt: Dieses Logo existiert bereits in deiner Datenbank! (Ähnlich zu: {dup_filename})")
            else:
                save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                image.save(save_path)
                st.success(f"✅ Neues Logo erfolgreich gespeichert: {uploaded_file.name}")

with tab2:
    st.header("Gespeicherte Logos")
    
    search_query = st.text_input("Suche nach Marke / Dateiname:")
    
    files = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(('png', 'jpg', 'jpeg', 'webp'))]
    
    if search_query:
        files = [f for f in files if search_query.lower() in f.lower()]
        
    if not files:
        st.info("Noch keine Bilder im Ordner vorhanden.")
    else:
        cols = st.columns(3)
        for idx, filename in enumerate(files):
            file_path = os.path.join(UPLOAD_DIR, filename)
            img = Image.open(file_path)
            with cols[idx % 3]:
                st.image(img, use_container_width=True)
                st.caption(filename)