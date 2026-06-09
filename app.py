import gradio as gr
from ingest import load_documents, chunk_text
from retriever import embed_and_store, retrieve, get_collection
from generator import generate_response

# ---------------------------------------------------------------------------
# Ingestion — runs once on startup
# ---------------------------------------------------------------------------

def run_ingestion():
    """
    Load UF/Gainesville activities sources, chunk them, and store in ChromaDB.

    If the vector store is already populated, ingestion is skipped.
    To re-ingest (e.g. after changing your chunking strategy), delete the
    ./chroma_db folder and restart the app.
    """
    collection = get_collection()

    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        print("To re-ingest, delete the ./chroma_db folder and restart.")
        return

    print("Ingesting rule documents...")
    documents = load_documents()
    all_chunks = []

    all_chunks = chunk_text(documents)

    if all_chunks:
        embed_and_store(all_chunks)
        print(f"Ingestion complete. {len(all_chunks)} chunks stored.")
    else:
        print(
            "\n⚠️  No chunks produced. Make sure chunk_text() is implemented in ingest.py.\n"
            "   Activities guide will start, but won't be able to answer questions yet.\n"
        )

# ---------------------------------------------------------------------------
# Chat handler
# ---------------------------------------------------------------------------

def chat(message, history):
    if not message.strip():
        return ""
    retrieved = retrieve(message)
    return generate_response(message, retrieved)

# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

with gr.Blocks(
    theme=gr.themes.Glass(primary_hue="orange", secondary_hue="blue"),
    title="UF Activities Guide",
    css="#textbox_id textarea {color: white}",
) as demo:

    gr.HTML("""
        <div style="text-align:center; padding:1.25rem 0 0.5rem;">
            <h1 style="font-size:2rem; font-weight:700; color:#e07707; margin:0;">
                🐊 UF Activities Guide
            </h1>
            <p style="color:#ffffff; font-size:1rem; margin:0.4rem 0 0;">
                Get the inside scoop on what to do on and around campus!
            </p>
        </div>
    """)

    with gr.Row():
        with gr.Column(scale=3):
            gr.ChatInterface(
                fn=chat,
                chatbot=gr.Chatbot(
                    height=440,
                    placeholder=(
                        "<div style='text-align:center; color:##ffffff; margin-top:3rem;'>"
                        "Ask about any activity around UF or Gainesville!"
                        "</div>"
                    ),
                ),
                textbox=gr.Textbox(
                    placeholder='e.g. "What is there to do around the University of Florida?"',
                    container=False,
                    elem_id="textbox_id",
                    scale=7, 
                ),
                examples=[
                    "Where can I go to watch a play at UF?",
                    "What museums are in Gainesville?",
                    "What trails are within walking distance of campus?",
                    "Where can I take my parents to around UF when they come to visit?",
                    "Are there any places for seniors in Gainesville?",
                    "What are some local pizza spots around UF?",
                    "What kind of activities are in Downtown Gainesville?",
                    "Are there any places for kids around UF?",
                    "What are some budget friendly restaurants around Gainesville?",
                ],
                cache_examples=False,
            )

        with gr.Column(scale=1, min_width=180):
            gr.HTML("""
                <div style="background:#e07707; border:1px solid #ddd6fe;
                            border-radius:10px; padding:1rem; margin-top:0.5rem;">
                    <p style="font-size:1.2rem; font-weight:700; color:#0038d1;
                               margin:0 0 0.5rem; letter-spacing:0.05em;">
                         📍 HOTSPOTS TO ASK ABOUT
                    </p>
                    <ul style="font-size:1.0rem; color:#000000; list-style:none; padding:0; margin:0; line-height:1.8;">
                        <li>🍕 Satchel's </li>
                        <li>🖼️ Cade Museum</li>
                        <li>🎯 La Tienda</li>
                        <li>🦇 UF Bat Houses</li>
                        <li>🌲 Depot Park</li>
                        <li>🎮 Arcade Bar</li>
                        <li>🦋 Butterfly Rainforest</li>
                        <li>👟 La Chua Trail</li>
                    </ul>
                    <hr style="border:none; border-top:1px solid #ddd6fe; margin:0.75rem 0;">
                    <p style="font-size:0.95rem; color:#0038d1; margin:0; line-height:1.5;">
                        Don't miss out on these local spots!
                    </p>
                </div>
            """)


if __name__ == "__main__":
    print("\n" + "="*50)
    print(" UF Activities Guide — starting up")
    print("="*50 + "\n")
    run_ingestion()
    demo.launch()
