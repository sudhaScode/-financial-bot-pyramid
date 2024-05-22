# Using LangChain for summarization and efficient context building.

from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.llms import VertexAI
from langchain import PromptTemplate, LLMChain
from IPython.display import display, Markdown

llm = VertexAI()

#stuff_chain = load_summarize_chain(vertex_llm, chain_type="stuff", prompt=prompt)

map_prompt_template = """
              You will be given a detailed description of a toy product.
              This description is enclosed in triple backticks (```).
              Using this description only, extract the name of the toy,
              the price of the toy and its features.

              ```{text}```
              SUMMARY:
              """
map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])

combine_prompt_template = """
                You will be given a detailed description different toy products
                enclosed in triple backticks (```) and a question enclosed in
                double backticks(``).
                Select one toy that is most relevant to answer the question.
                Using that selected toy description, answer the following
                question in as much detail as possible.
                You should only use the information in the description.
                Your answer should include the name of the toy, the price of the toy
                and its features. Your answer should be less than 200 words.
                Your answer should be in Markdown in a numbered list format.


                Description:
                ```{text}```


                Question:
                ``{user_query}``


                Answer:
                """
combine_prompt = PromptTemplate(
    template=combine_prompt_template, input_variables=["text", "user_query"]
)

docs = [Document(page_content=t) for t in matches]
chain = load_summarize_chain(
    llm, chain_type="map_reduce", map_prompt=map_prompt, combine_prompt=combine_prompt
)

llm_chain = LLMChain(prompt=prompt, llm=llm)
answer = llm_chain.run(
    {
        "context": "\n".join(matches),
        "creative_prompt": creative_prompt,
    }
)
answer = chain.run(
    {
        "input_documents": docs,
        "user_query": user_query,
    }
)


display(Markdown(answer))