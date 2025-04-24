from openai import OpenAI
from typing import List, Dict
from flotorch_core.logger.global_logger import get_logger

logger = get_logger()

class GatewayRerank:
    def __init__(self, api_key: str, model_id, base_url):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model_id = model_id

    def rerank_documents(self, query: str, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Reranks a list of documents based on a query using Amazon Bedrock's reranking model.

        Args:
            input_prompt (str): The query for reranking.
            retrieved_documents (List[Dict[str, str]]): List of documents to be reranked.

        Returns:
            List[Dict[str, str]]: A list of reranked documents in order of relevance.
        """
        if not documents:
            logger.warning("No documents provided for reranking.")
            return []
        
        messages = self._construct_prompt(query, documents)
        
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages
        )
        
        ranked_indices = self._extract_ranking(response.choices[0].message.content, len(documents))
        reranked_documents = [documents[i] for i in ranked_indices]
        
        return reranked_documents

    def _construct_prompt(self, query: str, documents: List[Dict[str, str]]) -> str:
        doc_texts = "\n\n".join([f"Document {i+1}:\n{doc['text']}" for i, doc in enumerate(documents)])
        prompt = (
            "You are a document reranker. Given the user query and a list of documents, "
            "rank them in order of relevance to the query.\n\n"
            f"Query: {query}\n\n"
            f"Documents:\n{doc_texts}\n\n"
            "Respond with a comma-separated list of the most relevant document numbers in descending order of relevance."
        )
        return prompt

    def _extract_ranking(self, llm_output: str, num_documents: int) -> List[int]:
        try:
            ranked_indices = [int(num.strip()) - 1 for num in llm_output.split(",")]
            if all(0 <= idx < num_documents for idx in ranked_indices):
                return ranked_indices
        except Exception as e:
            logger.error(f"Error parsing reranking response: {e}")
            logger.error(f"LLM output: {llm_output}")
            logger.error("Reranking failed: No results in response.")
            return []
        
        return list(range(num_documents))


retrieved_docs = [
    {"text": "The Eiffel Tower is in Paris."},
    {"text": "Mount Everest is the tallest mountain."},
    {"text": "The capital of France is Paris."}
]

api_key = "flt_3cqiawdagpy75ae9yhah1nh2o2us53mco0h10e0ni58d49do"
base_url="https://fphcciizk3.us-east-1.awsapprunner.com/api/v1"
model_id = "bedrock/amazon.nova-pro-v1:0"

reranker = GatewayRerank(api_key=api_key, model_id=model_id, base_url=base_url)
reranked = reranker.rerank_documents("What is the capital of France?", retrieved_docs)

for doc in reranked:
    print(doc["text"])