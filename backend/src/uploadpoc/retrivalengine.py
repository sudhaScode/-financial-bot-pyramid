from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.uploadpoc.ragsystem import llm, machineIndex
from src.uploadpoc.prompttemplates import qandaprompttemplate, question_prompt, refine_prompt, summarizationprompttemplate  
from langchain.chains.summarize import load_summarize_chain





# Create chain to answer questions
NUMBER_OF_RESULTS = 5
SEARCH_DISTANCE_THRESHOLD = 0.6

# Expose index to the retriever
retriever = machineIndex.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": NUMBER_OF_RESULTS,
        "search_distance": SEARCH_DISTANCE_THRESHOLD,
    },
    filters=None,
)
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    verbose=True,
    chain_type_kwargs={
        "prompt": PromptTemplate(
            template=qandaprompttemplate,
            input_variables=["context", "question"],
        ),
    },
)

# Enable for troubleshooting
qa.combine_documents_chain.verbose = True
qa.combine_documents_chain.llm_chain.verbose = True
qa.combine_documents_chain.llm_chain.llm.verbose = True


def ask(
    query,
    qa=qa,
    k=NUMBER_OF_RESULTS,
    search_distance=SEARCH_DISTANCE_THRESHOLD,
    filters={},
):
    qa.retriever.search_kwargs["search_distance"] = search_distance
    qa.retriever.search_kwargs["k"] = k
    qa.retriever.search_kwargs["filters"] = filters
    result = qa({"query": query})
    return result['result']
 

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    verbose=True,
    chain_type_kwargs={
        "prompt": PromptTemplate(
            template=summarizationprompttemplate,

            input_variables=["context", "question"],
        ),
    },
)

def summarize(
    query,
    qa=qa,
    k=NUMBER_OF_RESULTS,
    search_distance=SEARCH_DISTANCE_THRESHOLD,
    filters={},
):
    qa.retriever.search_kwargs["search_distance"] = search_distance
    qa.retriever.search_kwargs["k"] = k
    qa.retriever.search_kwargs["filters"] = filters
    result = qa({"query": query})
    return result['result']