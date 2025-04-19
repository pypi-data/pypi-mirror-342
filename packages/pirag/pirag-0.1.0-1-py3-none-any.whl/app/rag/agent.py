from langchain_openai.llms import OpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from pymilvus import MilvusClient

class Agent():
    def __init__(
        self,
        llm_base_url: str,
        llm_api_key: str,
        llm_model: str,
        embedding_base_url: str,
        embedding_api_key: str,
        embedding_model: str,
        milvus_host: str,
        milvus_database: str,
        milvus_collection: str,
    ):
        self.llm_base_url = llm_base_url
        self.llm_api_key = llm_api_key
        self.llm_model = llm_model
        self.embedding_base_url = embedding_base_url
        self.embedding_api_key = embedding_api_key
        self.embedding_model = embedding_model
        self.milvus_host = milvus_host
        self.milvus_database = milvus_database
        self.milvus_collection = milvus_collection
        
        self._llm_client: OpenAI = None
        self._embedding_client: OpenAIEmbeddings = None
        self._milvus_client: MilvusClient = None

    def retrieve_knowledge_base(self, query: str) -> str:
        llm_client = self._get_llm_client()
        embedding_client = self._get_embedding_client()
        milvus_client = self._get_milvus_client()
    
        
    def _get_llm_client(self) -> OpenAI:
        if self._llm_client is None:
            self._llm_client = OpenAI(
                base_url=self.llm_base_url,
                api_key=self.llm_api_key,
                model=self.llm_model,
            )
        return self._llm_client


    def _get_embedding_client(self) -> OpenAIEmbeddings:
        if self._embedding_client is None:
            self._embedding_client = OpenAIEmbeddings(
                base_url=self.embedding_base_url,
                api_key=self.embedding_api_key,
                model=self.embedding_model,
            )
        return self._embedding_client

    def _get_milvus_client(self) -> MilvusClient:
        if self._milvus_client is None:
            self._milvus_client = MilvusClient(
                host=self.milvus_host,
                database=self.milvus_database,
                collection=self.milvus_collection,
            )
        return self._milvus_client
