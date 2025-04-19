from typing import Optional
from typing import List
from typing import Any
import uuid
import logging
import uuid


import redis
from redis.exceptions import ResponseError
from openai import OpenAI
from langchain_redis.vectorstores import (
    RedisVectorStore as LangchainRedisVectorStoreBase,
)
from redisvl.schema import IndexSchema
from redisvl.query.filter import Tag
from openai_simple_embeddings.settings import OPENAI_EMBEDDINGS_API_KEY
from openai_simple_embeddings.settings import OPENAI_EMBEDDINGS_BASE_URL
from openai_simple_embeddings.settings import OPENAI_EMBEDDINGS_MODEL
from openai_simple_embeddings.settings import OPENAI_EMBEDDINGS_MAX_SIZE
from openai_simple_embeddings.langchain_embeddings import OpenAISimpleEmbeddings
from openai_simple_rerank.settings import OPENAI_RERANK_API_KEY
from openai_simple_rerank.settings import OPENAI_RERANK_BASE_URL
from openai_simple_rerank.settings import OPENAI_RERANK_MODEL
from openai_simple_rerank.settings import OPENAI_RERANK_MAX_SIZE
from openai_simple_rerank.base import get_rerank_scores
from zenutils import strutils

from .utils import Serializer
from .utils import YamlSerializer
from .schemas import Document
from .settings import OPENAI_REDIS_VECTORSTORE_REDIS_STACK_URL

__all__ = [
    "RedisVectorStore",
]
_logger = logging.getLogger(__name__)


class LangchainRedisVectorStore(LangchainRedisVectorStoreBase):

    @staticmethod
    def _strict_cosine_relevance_score_fn(distance: float) -> float:
        """Normalize the distance to a score on a scale [0, 1]."""
        value = 1.0 - distance
        if value >= 1.0:
            value = 1.0
        if value < 0:
            value = 0
        return value

    def _select_relevance_score_fn(self):
        return self._strict_cosine_relevance_score_fn


class RedisVectorStore(object):
    """基于redis-stack的向量数据库。"""

    def __init__(
        self,
        index_name: Optional[str] = None,
        redis_stack_url: Optional[str] = None,
        llm: Optional[OpenAI] = None,
        embeddings_llm: Optional[OpenAI] = None,
        rerank_llm: Optional[OpenAI] = None,
        embeddings_model: Optional[str] = None,
        rerank_model: Optional[str] = None,
        embeddings_max_size: Optional[int] = None,
        rerank_max_size: Optional[int] = None,
        embeddings_score_threshold: Optional[float] = None,
        rerank_score_threshold: Optional[float] = None,
        metadata_serializer: Optional[Serializer] = None,
        embeddings_dims: Optional[int] = 1024,
        vector_store_algorithm: Optional[str] = "hnsw",
        vector_store_distance_metric: Optional[str] = "cosine",
        vector_distance: Optional[str] = "float32",
        kb_id_field_name: Optional[str] = "vs_kb_id",  # 知识库唯一码
        doc_id_field_name: Optional[str] = "vs_doc_id",  # 文档唯一码
        page_id_field_name: Optional[str] = "vs_page_id",  # 文档分页唯一码
        category_field_name: Optional[str] = "vs_category",  # 文档分类
    ):
        self.index_name = index_name
        self.embeddings_dims = embeddings_dims
        self.vector_store_algorithm = vector_store_algorithm
        self.vector_store_distance_metric = vector_store_distance_metric
        self.embeddings_score_threshold = embeddings_score_threshold
        self.vector_distance = vector_distance
        self.vector_field_name = "embedding"  # 必须与langchain_redis保持一致
        self.content_field_name = "text"  # 必须与langchain_redis保持一致
        self.kb_id_field_name = kb_id_field_name
        self.doc_id_field_name = doc_id_field_name
        self.page_id_field_name = page_id_field_name
        self.category_field_name = category_field_name
        self.rerank_score_threshold = rerank_score_threshold
        self.redis_stack_url = (
            redis_stack_url or OPENAI_REDIS_VECTORSTORE_REDIS_STACK_URL
        )
        self.redis_instance = (
            self.redis_stack_url and redis.from_url(self.redis_stack_url) or None
        )
        self.embeddings_llm = (
            embeddings_llm
            or llm
            or OpenAI(
                api_key=OPENAI_EMBEDDINGS_API_KEY,
                base_url=OPENAI_EMBEDDINGS_BASE_URL,
            )
        )
        self.rerank_llm = (
            rerank_llm
            or llm
            or OpenAI(
                api_key=OPENAI_RERANK_API_KEY,
                base_url=OPENAI_RERANK_BASE_URL,
            )
        )
        self.embeddings_model = embeddings_model or OPENAI_EMBEDDINGS_MODEL
        self.embeddings_max_size = embeddings_max_size or OPENAI_EMBEDDINGS_MAX_SIZE
        self.rerank_model = rerank_model or OPENAI_RERANK_MODEL
        self.rerank_max_size = rerank_max_size or OPENAI_RERANK_MAX_SIZE
        self.metadata_serializer = metadata_serializer or YamlSerializer()
        self.vectorstores = {}

    def get_index_schema(self, index_name=None):
        index_name = self.get_index_name(index_name=index_name)
        index_schema_config = {
            "index": {
                "name": index_name,
                "prefix": index_name,
                "key_separator": ":",
            },
            "fields": [
                {"type": "tag", "name": self.kb_id_field_name},  # 知识库唯一码
                {"type": "tag", "name": self.doc_id_field_name},  # 文档唯一码
                {"type": "tag", "name": self.page_id_field_name},  # 分页唯一码
                {"type": "tag", "name": self.category_field_name},  # 文档类型
                {"type": "text", "name": self.content_field_name},
                {
                    "type": "vector",
                    "name": self.vector_field_name,
                    "attrs": {
                        "dims": self.embeddings_dims,
                        "algorithm": self.vector_store_algorithm,
                        "distance_metric": self.vector_store_distance_metric,
                        "vector_distance": self.vector_distance,
                    },
                },
            ],
        }
        return IndexSchema.from_dict(index_schema_config)

    def get_index_name(self, index_name: Optional[str] = None):
        return index_name or self.index_name or "default"

    def get_cached_vectorstore(
        self,
        index_name: Optional[str] = None,
        embeddings_model: Optional[str] = None,
        embeddings_max_size: Optional[int] = None,
        llm: Optional[OpenAI] = None,
    ) -> LangchainRedisVectorStore:
        # 参数处理，缺省参数取实例默认值
        index_name = self.get_index_name(index_name=index_name)
        embeddings_model = embeddings_model or self.embeddings_model
        embeddings_max_size = embeddings_max_size or self.embeddings_max_size
        llm = llm or self.embeddings_llm
        # 检查必要参数是否缺失
        if not self.redis_stack_url:
            raise RuntimeError(
                500,
                "Error: redis_stack_url not specified in instance initialization...",
            )
        if not index_name:
            raise RuntimeError(
                500,
                "Error: index_name not given and not specified in instance initialization...",
            )
        if not embeddings_model:
            raise RuntimeError(
                500,
                "Error: embeddings_model not given and not specified in instance initialization...",
            )
        # 计算缓存键
        cache_key = (
            f"{index_name}:{embeddings_model}:{llm.base_url}:{embeddings_max_size}"
        )
        # 如果已缓存，则取缓存实例
        if cache_key in self.vectorstores:
            return self.vectorstores[cache_key]
        # 创建新实例并缓存
        embeddings = OpenAISimpleEmbeddings(
            llm=llm,
            model=embeddings_model,
            max_size=embeddings_max_size,
        )
        self.vectorstores[cache_key] = LangchainRedisVectorStore(
            redis_url=self.redis_stack_url,
            index_name=index_name,
            key_prefix=index_name,
            index_schema=self.get_index_schema(index_name=index_name),
            embeddings=embeddings,
        )
        # 返回新建实例
        return self.vectorstores[cache_key]

    def get_serialized_metadata(self, metadata):
        serialized_metadata = {}
        for k, v in metadata.items():
            if k in [
                self.vector_field_name,
                self.content_field_name,
                self.kb_id_field_name,
                self.doc_id_field_name,
                self.page_id_field_name,
                self.category_field_name,
            ]:
                serialized_metadata[k] = metadata[k]
            else:
                serialized_metadata[k] = self.metadata_serializer.dumps(v)
        return serialized_metadata

    def get_unserialized_metadata(self, serialized_metadata):
        metadata = {}
        for k, v in serialized_metadata.items():
            k = strutils.TEXT(k)
            if k in [self.vector_field_name]:
                pass
            elif k in [
                self.content_field_name,
                self.kb_id_field_name,
                self.doc_id_field_name,
                self.page_id_field_name,
                self.category_field_name,
            ]:
                v = strutils.TEXT(v)
            else:
                try:
                    v = self.metadata_serializer.loads(v)
                except Exception:
                    pass
            metadata[k] = v
        return metadata

    def get_item(self, uid):
        serialized_metadata = self.redis_instance.hgetall(uid)
        metadata = self.get_unserialized_metadata(serialized_metadata)
        return metadata

    def fix_metadata(
        self,
        metadata: Optional[dict[str, str]] = None,
        kb_id: Optional[str] = None,
        doc_id: Optional[str] = None,
        page_id: Optional[str] = None,
        category: Optional[str] = None,
    ):
        # meta处理
        metadata = metadata or {}
        # 处理kb_id
        if kb_id:
            metadata[self.kb_id_field_name] = kb_id
        if not metadata.get(self.kb_id_field_name, None):
            metadata[self.kb_id_field_name] = "default"
        # 处理doc_id
        if doc_id:
            metadata[self.doc_id_field_name] = doc_id
        if not metadata.get(self.doc_id_field_name, None):
            metadata[self.doc_id_field_name] = "default"
        # 处理page_id
        if page_id:
            metadata[self.page_id_field_name] = page_id
        if not metadata.get(self.page_id_field_name, None):
            metadata[self.page_id_field_name] = str(uuid.uuid4())
        # 处理category
        if category:
            metadata[self.category_field_name] = category
        if not metadata.get(self.category_field_name, None):
            metadata[self.category_field_name] = "default"
        metadata = self.get_serialized_metadata(metadata)
        return metadata

    def insert(
        self,
        text: str,
        metadata: Optional[dict[str, str]] = None,
        page_id: Optional[str] = None,
        kb_id: Optional[str] = None,
        doc_id: Optional[str] = None,
        category: Optional[str] = None,
        index_name: Optional[str] = None,
        llm: Optional[OpenAI] = None,
        embeddings_model: Optional[str] = None,
        embeddings_max_size: Optional[int] = None,
    ):
        """把一段文本内容插入到向量数据库中。

        参数：
            - text: 要插入的文本内容
            - metadata: 文本内容相关的属性集
            - page_id: 文本段唯一码
            - kb_id: 知识库唯一码（支持过滤）
            - doc_id: 文本内容关联文档唯一码
            - category: 文本内容分类（支持过滤）
            - index_name: 向量数据库索引
            - llm: embeddings服务连接
            - embeddings_model: embeddings服务模型名称
            - embeddings_max_size: embeddings服务可支持的最大文本长度

        返回值：
            string类型，新插入的key值。一般为：<index_name>:<page_id>。
        """
        metadata = self.fix_metadata(
            metadata=metadata,
            kb_id=kb_id,
            doc_id=doc_id,
            page_id=page_id,
            category=category,
        )
        vs = self.get_cached_vectorstore(
            index_name=index_name,
            embeddings_model=embeddings_model,
            embeddings_max_size=embeddings_max_size,
            llm=llm,
        )
        uids = vs.add_texts(
            texts=[text],
            metadatas=[metadata],
            keys=[metadata[self.page_id_field_name]],
        )
        return uids[0]

    def insert_many(
        self,
        texts: List[str],
        metadatas: Optional[List[dict[str, str]]] = None,
        kb_id: Optional[str] = None,
        doc_id: Optional[str] = None,
        page_ids: Optional[List[str]] = None,
        category: Optional[str] = None,
        index_name: Optional[str] = None,
        llm: Optional[OpenAI] = None,
        embeddings_model: Optional[str] = None,
        embeddings_max_size: Optional[int] = None,
    ):
        index_name = self.get_index_name(index_name=index_name)
        if not metadatas:
            metadatas = []
            for _ in range(len(texts)):
                metadatas.append({})
        if page_ids:
            if len(page_ids) != len(texts):
                raise RuntimeError(
                    422,
                    "Error: RedisVectorStore.insert_many failed: len(page_ids) != len(texts)",
                )
            for index in range(len(metadatas)):
                metadatas[index][self.page_id_field_name] = page_ids[index]
        metadatas = [
            self.fix_metadata(
                metadata=metadata,
                kb_id=kb_id,
                doc_id=doc_id,
                category=category,
            )
            for metadata in metadatas
        ]
        vs = self.get_cached_vectorstore(
            index_name=index_name,
            embeddings_model=embeddings_model,
            embeddings_max_size=embeddings_max_size,
            llm=llm,
        )
        uids = vs.add_texts(
            texts=texts,
            metadatas=metadatas,
            keys=[metadata[self.page_id_field_name] for metadata in metadatas],
        )
        return uids

    def delete(self, uid):
        if not self.redis_instance:
            raise RuntimeError(
                500,
                "Error: redis_stack_url not specified in instance initialization...",
            )
        if uid:
            return self.redis_instance.delete(uid)
        else:
            return 0

    def delete_many(self, uids):
        if not self.redis_instance:
            raise RuntimeError(
                500,
                "Error: redis_stack_url not specified in instance initialization...",
            )
        if uids:
            return self.redis_instance.delete(*uids)
        else:
            return 0

    def similarity_search_with_relevance_scores(
        self,
        query,
        index_name: Optional[str] = None,
        index_names: Optional[List[str]] = None,
        kb_id: Optional[str] = None,
        kb_ids: Optional[List[str]] = None,
        category: Optional[str] = None,
        categories: Optional[List[str]] = None,
        document_schema: Document = Document,
        k=4,
        llm: Optional[OpenAI] = None,
        embeddings_model: Optional[str] = None,
        embeddings_max_size: Optional[int] = None,
        embeddings_score_threshold: Optional[float] = None,
        **kwargs,
    ):
        # 处理过滤条件
        kwargs = kwargs or {}
        # 处理过滤条件：score_threshold
        score_threshold = embeddings_score_threshold or self.embeddings_score_threshold
        if score_threshold:
            kwargs["score_threshold"] = score_threshold
        # 处理过滤条件：kb_id & kb_ids
        if (not kb_ids) and kb_id:
            kb_ids = [kb_id]
        if kb_ids:
            kb_id = kb_ids[0]
            kb_id_filter = Tag(self.kb_id_field_name) == kb_id
            for kb_id in kb_ids[1:]:
                kb_id_filter |= Tag(self.kb_id_field_name) == kb_id
            if "filter" in kwargs:
                kwargs["filter"] &= kb_id_filter
            else:
                kwargs["filter"] = kb_id_filter
        # 处理过滤条件：category & categories
        if (not categories) and category:
            categories = [category]
        if categories:
            category = categories[0]
            category_filter = Tag(self.category_field_name) == category
            for category in categories[1:]:
                category_filter |= Tag(self.category_field_name) == category
            if "filter" in kwargs:
                kwargs["filter"] &= category_filter
            else:
                kwargs["filter"] = category_filter
        # 处理index_names
        docs: List[self.document_schema] = []
        last_error = None
        index_name = self.get_index_name(index_name=index_name)
        if not index_names:
            index_names = [index_name]
        for index_name in index_names:
            vs = self.get_cached_vectorstore(
                index_name=index_name,
                embeddings_model=embeddings_model,
                embeddings_max_size=embeddings_max_size,
                llm=llm,
            )
            try:
                search_result = vs.similarity_search_with_relevance_scores(
                    query=query,
                    k=k,
                    **kwargs,
                )
            except ResponseError as error:
                # 如果搜索一个空知识库，则会执行一个`redis.exceptions.ResponseError: xxxx: no such index`异常
                # 这个实际上是一个正常的业务行为，只有返回结果为空即可
                # 其它异常，直接抛出即可
                if "no such index" in str(error):
                    _logger.warning(
                        "search on unindexed vector store: %s", vs.index_name
                    )
                    search_result = []
                else:
                    raise error
            for doc, vs_embeddings_score in search_result:
                vs_uid = index_name + ":" + doc.metadata[self.page_id_field_name]
                item = self.get_item(uid=vs_uid)
                item["vs_uid"] = vs_uid
                item["vs_page_content"] = doc.page_content
                item["vs_embedding"] = item[self.vector_field_name]
                item["vs_embeddings_score"] = vs_embeddings_score
                item["vs_rerank_score"] = None
                item["vs_index_name"] = index_name
                doc = document_schema.model_validate(item)
                docs.append(doc)
        if docs:
            docs.sort(key=lambda doc: -doc.vs_embeddings_score)
        docs = docs[:k]
        return docs

    def rerank(
        self,
        query: str,
        docs: List[Document],
        k: int = 4,
        llm: Optional[OpenAI] = None,
        rerank_model: Optional[str] = None,
        rerank_max_size: Optional[int] = None,
        rerank_score_threshold: Optional[float] = None,
    ):
        llm = llm or self.rerank_llm
        rerank_score_threshold = rerank_score_threshold or self.rerank_score_threshold
        scores = get_rerank_scores(
            query=query,
            documents=[doc.vs_page_content for doc in docs],
            llm=llm,
            model=rerank_model,
            max_size=rerank_max_size,
        )
        for score, doc in zip(scores, docs):
            doc.vs_rerank_score = score
        if rerank_score_threshold:
            docs = [
                doc for doc in docs if doc.vs_rerank_score >= rerank_score_threshold
            ]
        docs.sort(key=lambda doc: -doc.vs_rerank_score)
        return docs[:k]

    def similarity_search_and_rerank(
        self,
        query,
        index_name: Optional[str] = None,
        index_names: Optional[List[str]] = None,
        kb_id: Optional[str] = None,
        kb_ids: Optional[List[str]] = None,
        category: Optional[str] = None,
        categories: Optional[List[str]] = None,
        k: int = 4,
        scale: int = 2,
        document_schema: Document = Document,
        llm: Optional[OpenAI] = None,
        embeddings_llm: Optional[OpenAI] = None,
        rerank_llm: Optional[OpenAI] = None,
        embeddings_model: Optional[str] = None,
        embeddings_max_size: Optional[int] = None,
        embeddings_score_threshold: Optional[float] = None,
        rerank_model: Optional[str] = None,
        rerank_max_size: Optional[int] = None,
        rerank_score_threshold: Optional[float] = None,
        **kwargs,
    ):
        embeddings_llm = embeddings_llm or llm or self.embeddings_llm
        rerank_llm = rerank_llm or llm or self.rerank_llm
        docs = self.similarity_search_with_relevance_scores(
            query=query,
            index_name=index_name,
            index_names=index_names,
            kb_id=kb_id,
            kb_ids=kb_ids,
            category=category,
            categories=categories,
            k=k * scale,
            document_schema=document_schema,
            llm=embeddings_llm,
            embeddings_model=embeddings_model,
            embeddings_max_size=embeddings_max_size,
            embeddings_score_threshold=embeddings_score_threshold,
            **kwargs,
        )
        return self.rerank(
            query=query,
            docs=docs,
            k=k,
            llm=rerank_llm,
            rerank_model=rerank_model,
            rerank_max_size=rerank_max_size,
            rerank_score_threshold=rerank_score_threshold,
        )

    def flush(self, index_name: str = None):
        """清空指定索引。"""
        index_name = index_name or self.index_name

        if not index_name:
            raise RuntimeError(
                500,
                "Error: index_name not given and not specified in instance initialization...",
            )
        if not self.redis_instance:
            raise RuntimeError(
                500,
                "Error: redis_stack_url not specified in instance initialization...",
            )

        # 删除所有索引项
        keys = self.redis_instance.keys(index_name + ":*")
        if keys:
            self.redis_instance.delete(*keys)
        # 删除索引
        indexes = self.redis_instance.execute_command("FT._LIST")
        if indexes:
            indexes = [x.decode("utf-8") for x in indexes]
        if index_name in indexes:
            self.redis_instance.execute_command(f"FT.DROPINDEX {index_name}")
        return True
