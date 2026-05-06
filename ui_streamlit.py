# ui_streamlit.py
import streamlit as st
import requests

st.set_page_config(
    page_title="RAG IPCC — Climate Q&A",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 RAG Demo — IPCC AR6")
st.caption("Powered by Ollama + LangChain + Chroma")

API_URL = "http://localhost:8000"

# Vérification du backend
try:
    r = requests.get(f"{API_URL}/", timeout=2)
    if r.ok:
        st.success("✅ Backend connecté")
    else:
        st.error("❌ Backend non disponible")
except:
    st.error("❌ Backend non démarré — lance `uvicorn app:app --reload --port 8000`")

st.divider()

# Zone de question
question = st.text_input(
    "Pose une question sur les rapports IPCC AR6",
    placeholder="Ex: What are the main causes of global warming according to AR6?"
)

col1, col2 = st.columns([1, 5])
with col1:
    ask_btn = st.button("Ask 🔍", type="primary")
with col2:
    k = st.slider("Nombre de chunks à récupérer", 2, 8, 4)

if ask_btn and question:
    with st.spinner("Recherche en cours..."):
        try:
            resp = requests.post(f"{API_URL}/ask", json={"question": question}, timeout=300)
            if resp.ok:
                data = resp.json()
                
                st.subheader("📝 Réponse")
                st.write(data["answer"])
                
                if data.get("sources"):
                    st.subheader("📚 Sources utilisées")
                    for i, src in enumerate(data["sources"], 1):
                        with st.expander(f"Source {i} — {src['source']} (page {src['page']})"):
                            st.write(src["preview"])
            else:
                st.error(f"Erreur API : {resp.status_code}")
        except requests.exceptions.Timeout:
            st.error("⏱️ Timeout — le modèle prend du temps, réessaie.")
        except Exception as e:
            st.error(f"Erreur : {e}")