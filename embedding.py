from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter

'''
GLOBAL UTILITY FUNCTIONS
'''
def split_document(doc, chunk_size = 7500, overlap = 1000):
    splitter = get_recursive_character_text_splitter(chunk_size, overlap)
    return splitter.split_text(doc)



class inmemory_vector_store:
    def __init__(self, embedding_model = "mxbai-embed-large", **kwargs):
        self.embedding = OllamaEmbeddings(embedding_model = embedding_model)
        self.vector_store =  InMemoryVectorStore(self.embedding)
        self.overlap = kwargs.get('overlap', 1000)
        self.chunk_size = kwargs.get('chunk_size',7500)
    

    def add_texts(self, texts, **kwargs):
        overlap = kwargs.get('overlap', self.overlap)
        chunk_size = kwargs.get('chunk_size', self.chunk_size)
        split = split_document(texts, chunk_size, overlap)
        vector_store.add_tex
    

        


    



def get_inmemory_vector_store(embedding_model = "mxbai-embed-large"):
    embeddings = OllamaEmbeddings(model=embedding_model)
    vector_store = InMemoryVectorStore(embeddings)
    return vector_store


def get_chat_ollama(llm_model = "llama3.2:3b"):
    llm = ChatOllama(model=llm_model)
    return llm

def get_recursive_character_text_splitter(chunk_size = 1000, overlap = 100):
    return RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = overlap)#,length_function=len, separators=['\n','\n\n', '.' , ','])



if __name__ == "__main__":
    print("Can only import embedding.py")
else:
    print("Imported embedding.py")

    