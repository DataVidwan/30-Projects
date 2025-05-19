import os
import PyPDF2
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# STEP 1: Add your OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your-api-key-here"  # Replace with your key

# STEP 2: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# STEP 3: Chunk the text
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks

# STEP 4: Create vector store
def create_vector_store(chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    return vectorstore

# STEP 5: Ask questions using a chatbot
def ask_question(vectorstore, question):
    llm = ChatOpenAI(temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )
    result = qa_chain({"query": question})
    return result["result"]

# MAIN EXECUTION
if __name__ == "__main__":
    pdf_path = "sample.pdf"  # Replace with your PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(extracted_text)

    print(f"\n✅ PDF extracted and chunked into {len(chunks)} pieces.")

    try:
        vectorstore = create_vector_store(chunks)
        print("✅ Vector store created. You can now ask questions about your PDF!")

        # Simple chatbot loop
        while True:
            user_input = input("\n❓ Ask a question (or type 'exit' to quit): ")
            if user_input.lower() == "exit":
                print("👋 Exiting chatbot. Goodbye!")
                break
            response = ask_question(vectorstore, user_input)
            print(f"\n🤖 Answer: {response}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
