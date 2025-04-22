# serializer.py
from datetime import datetime, date, time
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel
from typing import Any, Dict, List, Union, Set

from sthg_common_base.utils.log_util import Logger

class EnhancedJSONSerializer:
    """增强型JSON序列化处理器"""
    _custom_serializers: List[tuple] = []
    """增加跳过的类"""
    _excluded_classes: Set[type] = set()
    OBJECT_ID_TYPE: Any = None
    @classmethod
    def register_excluded_class(cls, target_class: type):
        cls._excluded_classes.add(target_class)

    @classmethod
    def register_serializer(cls, check_type: type, serializer: callable):
        """注册自定义序列化处理器"""
        cls._custom_serializers.append((check_type, serializer))

    @classmethod
    def json_serializer(cls, obj: Any) -> Any:
        """核心序列化方法"""
        # 处理自定义注册类型
        try:

            for check_type, serializer in cls._custom_serializers:
                if isinstance(obj, check_type):
                    return serializer(obj)

            if type(obj) in cls._excluded_classes:
                return f"<Excluded Class: {type(obj).__name__}>"

            if cls._is_sqlalchemy_internal_object(cls,obj):
                return f"<SQLAlchemy Internal Object: {type(obj).__name__}>"

            if isinstance(obj, str):
                return obj.encode('utf-8').decode('unicode_escape')

            # 基础类型处理
            if isinstance(obj, (datetime, date, time)):
                return obj.isoformat()

            # 数值类型处理
            if isinstance(obj, Decimal):
                return float(obj)

            # 数据库相关类型
            if cls._is_object_id(obj):
                return str(obj)

            # UUID处理
            if isinstance(obj, UUID):
                return str(obj)

            # Pydantic模型
            if isinstance(obj, BaseModel):
                return obj.dict()

            # SQLAlchemy模型
            if cls._is_sqlalchemy_model(obj):
                return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

            # Numpy类型
            numpy_data = cls._handle_numpy(obj)
            if numpy_data is not None:
                return numpy_data

            # 自定义对象的字典表示
            if hasattr(obj, '__dict__'):
                return cls.deep_serialize(obj.__dict__)
        except Exception as e:
            Logger.error_log(f"序列化单步失败:{e}")
            return None

        # 最后兜底处理
        try:
            return str(obj)
        except Exception as e:
            Logger.error_log(f"序列化兜底失败:{e}")
            return None

    @staticmethod
    def _is_sqlalchemy_internal_object(cls,obj: Any) -> bool:
        """通过模块路径识别 SQLAlchemy 内部对象"""
        try:
            module = type(obj).__module__
            return (
                    module.startswith("sqlalchemy.")
                    and not cls._is_sqlalchemy_model(obj)
            )
        except AttributeError as er:
            Logger.error_log(f"_is_sqlalchemy_internal_object失败:{er}")
            return False

    @staticmethod
    def _is_sqlalchemy_model(cls,obj: Any) -> bool:
        """精确匹配用户定义的模型"""
        return hasattr(obj, '__table__') and not cls._is_sqlalchemy_internal_object(obj)

    @classmethod
    def deep_serialize(cls, data: Any) -> Any:
        """递归序列化嵌套结构"""
        if isinstance(data, (str, int, float, bool, type(None))):
            return data
        if isinstance(data, dict):
            return {k: cls.deep_serialize(v) for k, v in data.items()}
        if isinstance(data, (list, tuple, set)):
            return [cls.deep_serialize(item) for item in data]
        return cls.json_serializer(data)

    @staticmethod
    def _is_object_id(obj: Any) -> bool:
        """安全判断 ObjectId 类型（无 pymongo 依赖）"""
        if EnhancedJSONSerializer.OBJECT_ID_TYPE is None:
            try:
                from bson import ObjectId
                EnhancedJSONSerializer.OBJECT_ID_TYPE = ObjectId
            except ImportError:
                # 若未安装 pymongo，标记为不可用
                EnhancedJSONSerializer.OBJECT_ID_TYPE = False

        if EnhancedJSONSerializer.OBJECT_ID_TYPE:
            return isinstance(obj, EnhancedJSONSerializer.OBJECT_ID_TYPE)
        return False

    @staticmethod
    def _is_sqlalchemy_model(obj: Any) -> bool:
        """判断SQLAlchemy模型"""
        return hasattr(obj, '__table__')

    @staticmethod
    def _handle_numpy(obj: Any) -> Union[None, int, float, bool, list]:
        """处理Numpy数据类型"""
        try:
            import numpy as np
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                                np.int16, np.int32, np.int64, np.uint8,
                                np.uint16, np.uint32, np.uint64)):
                return int(obj)
            if isinstance(obj, (np.float_, np.float16, np.float32,
                                np.float64)):
                return float(obj)
            if isinstance(obj, np.bool_):
                return bool(obj)
        except ImportError as er:
            Logger.error_log(f"_handle_numpy失败:{er}")
            pass
        return None