from crawler import *
from embedding import *
import concurrent.futures
from tts import *

la = 0
lb = 0
def parallel_url_extractor(query, num_results = 5):
    results = web_search(query, num_results)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_results) as executor:
        url_lst = list(executor.map(lambda x: x['href'], results))
    print("-----------------------parallel url return----------------------")
    print(url_lst)
    print("-----------------------parallel url return----------------------")
    return url_lst

def parallel_crawler(url_lst):
    with concurrent.futures.ThreadPoolExecutor(max_workers = len(url_lst)) as executor:
        results = list(executor.map(process_content_for_llm,map(crawler, url_lst)))
    print("-----------------------parallel content return----------------------")
    print(results)
    print("-----------------------parallel content return----------------------")
    global la
    la = len(str(results))
    return results

def batch_embedding(content_list, model_name = "mxbai-embed-large"):
    vector_store = embedding.get_inmemory_vector_store(model_name)

    with concurrent.futures.ThreadPoolExecutor(max_workers = len(content_list)) as executor:
        executor.map(vector_store.add_texts ,map(embedding.split_document, content_list))

    # for i in content_list:
    #     split_doc = embedding.split_document(i, chunk_size = 10000, overlap = 1000)
    #     _ = vector_store.add_texts(split_doc)


    return vector_store

def parallel_crawler_with_embeddings(query, model_name = "mxbai-embed-large"):  
    url_lst = parallel_url_extractor(query)
    content_list = parallel_crawler(url_lst)
    vector_store = batch_embedding(content_list, model_name)
    return vector_store
    
def embedded_query_langchain(query, vector_store):
    retrieved_docs = vector_store.similarity_search(query)
    str_doc = '\n\n'.join([doc.page_content for doc in retrieved_docs])
    print("------------------start of similarity search-----------")
    print(str_doc)
    print("------------------end of similarity search-----------")
    global lb
    global la
    #la is the original length
    #lb is the ne reduce length
    lb = len(str(str_doc))
    print("------------------------similarity fraction reduction------------------")
    print(lb)
    print(la)
    print(lb/la)
    print("------------------------similarity fraction reduction------------------")
    response = query_with_langchain(str_doc, query, llm_model="llama3.2:3b")
    return response

def search(query):
    vector_store = parallel_crawler_with_embeddings(query)
    response = embedded_query_langchain(query, vector_store)
    return response

def play(query):
    response = search(query)
    tts_ = tts()
    tts_.play_audio(response,1)

if __name__ == "__main__":
    play(input("Enter your query: "))