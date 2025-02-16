import requests
from bs4 import BeautifulSoup
import re
from langchain import hub
from langchain.document_loaders import BSHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain.chains import ConversationChain
from langchain.chains import LLMChain
from langchain.schema import Document
from duckduckgo_search import DDGS
from langchain_ollama import ChatOllama
import embedding





def clean_text(text):
    """Remove extra whitespace and special characters"""
    return re.sub(r'\s+', ' ', text).strip()



def crawler(url):
    try:
        # Fetch page with headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }


        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()
        


        # Extract content
        content=  {
            'title': clean_text(soup.title.string) if soup.title else '',
            'main_content': [],
            'headings': [],
        }


        
        # Get headings
        for heading in soup.find_all(['h1', 'h2', 'h3']):
            if heading.text:
                content['headings'].append(clean_text(heading.text))
        


        # Get main content
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        if main_content:
            paragraphs = main_content.find_all('p')
        else:
            paragraphs = soup.find_all('p')
            



        for p in paragraphs:
            text = clean_text(p.text)
            if len(text) > 50:  # Filter out short snippets
                content['main_content'].append(text)
        return content
        


    except Exception as e:
        print(f"Error: {e}")
        return None



def web_search(query, num_results=5):
    """
    Perform web search using DuckDuckGo
    """
    try:


        results = DDGS().text(query, max_results=num_results)
        print (results)
        return results
    

    except Exception as e:
        print(f"Search Error: {e}")
        return None


def process_content_for_llm(content,depth = 5):
    """Format crawler content for LLM"""

    return(str(content))

    # try:
    #     return f"""
    #     Title: {content['title']}
    #     Main Content : {' '.join(content['main_content'][:])}
    #     Key Sections:{' '.join(content['headings'])}
    #     """
    # except:
    #     try:
    #         return f"""
    #         Main Content:{' '.join(content['main_content'][:])}

    #         key Sections:{' '.join(content['headings'])}"""
    #     except:
    #         try : 
    #             return str(content)
    #         except:
    #             return ""
    


def query_with_embeddings(content, question,depth = 5, model_name="mxbai-embed-large", llm_model="llama3.2:3b"):
    if isinstance(content, dict):
        content_ = process_content_for_llm(content,depth)
    else:
        content_ = content
        print(content_)
    vector_store = embedding.get_inmemory_vector_store(model_name)
    llm = embedding.get_chat_ollama(llm_model)
    split_doc = embedding.split_document(content_)
    _ = vector_store.add_texts(split_doc)
    # prompt = hub.pull("rlm/rag-prompt")
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        Context: {context}
        
        Question: {question}
        
        Answer: condense the information to some only importatant bulletpoints and facts.
        """
    )
    retrieved_docs = vector_store.similarity_search(question)
    str_doc = '\n\n'.join([doc.page_content for doc in retrieved_docs])
    message = prompt.invoke({"question": question,"context": str_doc})
    response = llm.invoke(message)
    return response

def analyze_webpage_with_embeddings(url, question, depth = 5):
    content = crawler(url)
    if content:
        return query_with_embeddings(content, question, depth=depth)
    return None


def query_with_langchain(content, question, llm_model="llama3.2:3b"):
    """Query Ollama through LangChain"""
    # Initialize Ollama
    llm = ChatOllama(model=llm_model)
    
    # Create prompt template
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        Context: {context}
        
        Question: {question}
        
        Answer: condense the information to some only importatant bulletpoints and facts.
        """
    )
    
    # Create chain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Process content
    if (not(isinstance(content,str))):
        context = process_content_for_llm(content)
    else:
        context = content

    
    # Execute chain
    response = chain.run(context=context, question=question)
    return response

def analyze_webpage(url, question):
    """Combine crawler with LangChain query"""
    content = crawler(url)
    if content:
        return query_with_langchain(content, question)
    return None



def run():
    while (True):
        query = input("Enter your query: ")
        results = web_search(query)
        
        url = []
        #display results
        for result in results:
            print(f"Title: {result['title']}")
            print(f"URL: {result['href']}")
            url.append(result['href'])
            # print(f"Snippet: {result['snippet']}\n")
        
        print("\n\n\n",url)
        sum_of_all = []
        for i in url:    
            response = analyze_webpage_with_embeddings(i, query)
            try:
                sum_of_all.append(response.content)
                print(f"Answer: {response.content}\n")
            except:
                continue
        
        sum_of_all = '\n'.join(sum_of_all)
        print("The summary of it all is :", sum_of_all)

        response = query_with_langchain(sum_of_all, query)
        print(response)

        cont = input("Do you want to continue? (y/n): ")
        if cont.lower() != 'y':
            break



if (__name__ == "__main__"):
    run()
