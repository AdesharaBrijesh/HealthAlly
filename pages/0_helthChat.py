import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import pandas as pd
import faiss
import pickle
import re
from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client["healthcare_chatbot"]
first_aid_rooms_collection = db["first_aid_rooms"]
chat_history_collection = db["chat_history"]

# Check if user is logged in
def is_logged_in():
    return 'user_id' in st.session_state and 'logged_in' in st.session_state and st.session_state['logged_in']

def get_first_aid_room(department):
    return first_aid_rooms_collection.find_one({"department": department})

def save_chat_to_db(user_id, message, role="user"):
    chat_history_collection.insert_one({
        "user_id": user_id,
        "message": message,
        "role": role,
        "timestamp": datetime.now()
    })

# Load the medicine data and FAISS index
def load_medicine_data():
    try:
        index = faiss.read_index('model/medicine_faiss_index.bin')
        df = pd.read_pickle('model/medicine_df.pkl')
        if df.empty:
            raise ValueError("Loaded DataFrame is empty")
        return index, df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

faiss_index, medicine_df = load_medicine_data()

# Medicine search function
def search_medicine(query):
    try:
        query = query.lower()
        query_terms = re.split(r'\s+|and|or|,', query)
        query_terms = [term.strip() for term in query_terms if term.strip()]
        search_columns = [col for col in medicine_df.columns if medicine_df[col].dtype == 'object']
        mask = medicine_df[search_columns].apply(
            lambda col: col.str.lower().str.contains('|'.join(query_terms), na=False)
        ).any(axis=1)
        results = medicine_df[mask].head(1)
        if not results.empty:
            return results.iloc[0].to_dict()
        else:
            return None
    except Exception as e:
        st.error(f"Error in search: {e}")
        return None

# Create LangChain LLMChain
def create_llm_chain():
    GROQ_API_KEY = "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"
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="gemma2-9b-it",
        temperature=0.5,
        max_tokens=500
    )
    prompt_template = PromptTemplate(
        input_variables=["question"],
        template="""**Question:** {question}

        **Guidelines for Answer:**
        - **Accuracy:** Ensure that all information provided is medically accurate and up-to-date.
        - **Clarity:** Explain complex medical terms in simple language that patients can easily understand.
        - **Patient Focus:** Tailor your response to prioritize patient safety and understanding. Provide clear instructions or advice where applicable.

        **Final Answer:**
        Please generate a response that combines the detailed medical information, relevant research insights, and patient-friendly advice. Include information about Ayurvedic plants in the composition and suggest an alternative medicine or treatment option at the end of your response.
        """
    )
    return LLMChain(llm=llm, prompt=prompt_template)

llm_chain = create_llm_chain()

# Streamlit Application UI
# st.set_page_config(page_title="Healthcare Assistant", page_icon="💊", layout="wide")

# Sidebar Design
with st.sidebar:
    st.markdown("Get insights on your health, search for medicines, and receive AI-driven medical advice — all in one place.")
    st.markdown("---")
    st.subheader("How to Use:")
    st.markdown("""
    - **Search Medicines:** Enter medicine names or symptoms.
    - **Ask Questions:** Get AI-powered answers to medical queries.
    - **Receive Suggestions:** Find treatments and alternative medicines.
    """)
    st.markdown("---")
    st.info("This application is for informational purposes only and should not replace professional medical advice.")

# Main Layout
st.title("Unified Healthcare Chat Assistant")
st.markdown("### Your Personal Guide for Medicine and Health Queries")

def main():
    if not is_logged_in():
        st.warning("Please log in to access the chat.")
        return

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Input Section
    st.markdown("#### 🩺 Enter Your Query Below")
    user_query = st.text_input("Type your symptoms, medicine name, or any medical question:", placeholder="E.g., headache, paracetamol, or remedies for cold")

    # Results Section
    if st.button("Search/Ask"):
        if not user_query.strip():
            st.warning("Please enter a valid query.")
        else:
            st.session_state.messages.append({"role": "user", "content": user_query})
            save_chat_to_db(st.session_state["user_id"], user_query, "user")
            col1, col2 = st.columns([2, 1])

            # Step 1: Search for a medicine
            with col2:
                with st.spinner("🔍 Searching the medicine database..."):
                    medicine_result = search_medicine(user_query)

                    # Step 2: Display Results
                    if medicine_result:
                        st.success("✅ Medicine Found!")
                        st.subheader("Medicine Details:")
                        with st.expander("Click to view details"):
                            for key, value in medicine_result.items():
                                st.markdown(f"- **{key.capitalize()}:** {value}")
                        st.session_state.messages.append({"role": "assistant", "content": medicine_result})
                        save_chat_to_db(st.session_state["user_id"], medicine_result, "medicine")
                    else:
                        st.warning("❌ No direct matches found in the medicine database.")

            
            # Step 3: AI-based Response
            with col1:
                st.info("🤖 Generating AI-based advice...")
                with st.spinner("AI is crafting a response..."):
                    try:
                        ai_response = llm_chain.run({"question": user_query})
                        st.subheader("AI Response:")
                        st.write(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        save_chat_to_db(st.session_state["user_id"], ai_response, "assistant")
                    except Exception as e:
                        st.error(f"Error generating AI response: {e}")


if __name__ == "__main__":
    main()