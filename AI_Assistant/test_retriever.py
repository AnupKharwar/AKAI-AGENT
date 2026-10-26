from knowledge_retriever import load_documents
from knowledge_retriever import retrieve

documents = load_documents()

# for name, text in documents.items():

    # print(name)
    
    # print(text)
    # print("-" * 40)


filename, content = retrieve("Python")
if filename and content:
    print(f"Found in {filename}:")
    print(content)
else:
    print("Document not found.")