from typing import Dict
from typing import List
import uuid

import yaml
from openai_redis_vectorstore.base import RedisVectorStore

from django.db import models
from django.utils.safestring import mark_safe

from .schemas import VSPage
from .settings import VECTORSTORE_INDEX_NAME

__all__ = [
    "WithVectorStoreIndex",
]


class WithVectorStoreIndex(models.Model):
    vectorstore_updated = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="已更新向量数据库",
        help_text="None：表示待处理。<br />True：表示索引成功。<br />False：表示索引失败。",
    )
    vectorstore_uids_data = models.TextField(
        null=True,
        blank=True,
        verbose_name="向量数据库记录编号",
        help_text=mark_safe(
            "添加至向量数据库后返回的编号。用于后续向量数据库的数据维护。"
        ),
    )

    class Meta:
        abstract = True

    def update_vectorstore_index(self, save=True):
        # 对象已经触发了索引，则不能再次触发。
        # 需要重新从数据库查询生成新的实例才能再次触发索引。
        if self.get_enable_vectorstore_index_flag():
            self.upsert_index(save=False)
        else:
            self.delete_index(save=False)
        self.vectorstore_updated = True
        if save:
            self.save()

    #  vectorstore_uids属性处理
    def get_vectorstore_uids(self):
        if not self.vectorstore_uids_data:
            return []
        else:
            return yaml.safe_load(self.vectorstore_uids_data)

    def set_vectorstore_uids(self, value):
        if not value:
            self.vectorstore_uids_data = None
        else:
            self.vectorstore_uids_data = yaml.safe_dump(value)

    vectorstore_uids = property(get_vectorstore_uids, set_vectorstore_uids)

    def get_enable_vectorstore_index_flag(self) -> bool:
        """判断是否需要创建索引"""
        # 一般来说数据记录中应该有enabled或deleted等字段
        # 表示是否启用索引
        raise NotImplementedError()

    def get_vectorstore_index_pages(self) -> List[VSPage]:
        pages = []
        index_names = self.get_vectorstore_index_names()
        if isinstance(index_names, str):
            index_names = [index_names]
        for index_name in index_names:
            contents = self.get_vectorstore_index_contents()
            metadatas = self.get_vectorstore_index_metadatas()
            for content, metadata in zip(contents, metadatas):
                page = VSPage.model_validate(
                    {
                        "index_name": index_name,
                        "content": content,
                        "metadata": metadata,
                        "kb_id": self.get_kb_id(),
                        "doc_id": self.get_doc_id(),
                        "page_id": self.get_page_id(),
                        "category": self.get_category(),
                    }
                )
                pages.append(page)
        return pages

    def get_vectorstore_index_names(self) -> List[str]:
        # 如果有多个index_name表示：
        # 本数据记录需要在多个向量数据库中建立索引
        if hasattr(self, "vectorstore_index_names"):
            return getattr(self, "vectorstore_index_names")
        if hasattr(self, "vectorstore_index_name"):
            return [getattr(self, "vectorstore_index_name")]
        if VECTORSTORE_INDEX_NAME:
            return [VECTORSTORE_INDEX_NAME]
        raise RuntimeError(500, "VectorStore index name NOT configed.")

    def get_vectorstore_index_contents(self) -> List[str]:
        # 向量数据库有索引长度的限制
        # 所以一般文档内容需要分片后进行索引
        # 这里返回分片列表
        raise NotImplementedError()

    def get_kb_id(self):
        return "default"

    def get_doc_id(self):
        return "default"

    def get_page_id(self):
        return str(uuid.uuid4())

    def get_category(self):
        return "default"

    def get_vectorstore_index_metadatas(self, contents=None) -> List[Dict[str, str]]:
        if contents is None:
            contents = self.get_vectorstore_index_contents()
        meta = self.get_vectorstore_index_metadata()
        return [meta] * len(contents)

    def get_vectorstore_index_metadata(self) -> Dict[str, str]:
        return {
            "app_label": self._meta.app_label,
            "model_name": self._meta.model_name,
            "id": self.id,
        }

    def delete_index(self, save=False):
        if self.vectorstore_uids:
            vs = RedisVectorStore()
            vs.delete_many(self.vectorstore_uids)
            self.vectorstore_uids = None
            if save:
                self.save()

    def upsert_index(self, save=False):
        vs = RedisVectorStore()
        # 先删除
        self.delete_index(save=False)
        # 后添加
        uids = []
        for page in self.get_vectorstore_index_pages():
            uid = vs.insert(
                index_name=page.index_name,
                text=page.content,
                metadata=page.metadata,
                page_id=page.page_id,
                kb_id=page.kb_id,
                doc_id=page.doc_id,
                category=page.category,
            )
            uids.append(uid)
        # 更新数据库记录
        self.vectorstore_uids = uids
        if save:
            self.save()

    def get_vectorstore_instance(self):
        return RedisVectorStore()
