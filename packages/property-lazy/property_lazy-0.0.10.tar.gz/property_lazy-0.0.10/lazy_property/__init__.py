__version__ = "0.0.10"
from functools import update_wrapper


class LazyProperty(property):
    def __init__(self, method, fget=None, fset=None, fdel=None, doc=None):
        self.method = method
        self._cache_name = "__cache_{}".format(self.method.__name__)

        doc = doc or method.__doc__
        super(LazyProperty, self).__init__(fget=fget, fset=fset, fdel=fdel, doc=doc)

        update_wrapper(self, method)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if hasattr(instance, self._cache_name):
            result = getattr(instance, self._cache_name)
        else:
            if self.fget is not None:
                result = self.fget(instance)
            else:
                result = self.method(instance)

            setattr(instance, self._cache_name, result)

        return result


class LazyGlobalProperty(LazyProperty):
    """
    基于LazyProperty实现的全局缓存版本
    所有实例共享相同的缓存结果
    """

    _GLOBAL_CACHE = {}

    def _get_top_class(self, cls):
        """获取继承链中最顶层的父类"""
        for base in cls.__bases__:
            if base.__name__ == "object":
                return cls
            return self._get_top_class(base)
        return cls

    def _get_cache_key(self, instance):
        """获取全局缓存键"""
        top_class = self._get_top_class(instance.__class__)
        return f"{top_class.__name__}.{self.method.__name__}"

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # 使用类名+方法名作为全局缓存键
        cache_key = self._get_cache_key(instance)

        if cache_key in self._GLOBAL_CACHE:
            return self._GLOBAL_CACHE[cache_key]

        # 计算结果并存入全局缓存
        if self.fget is not None:
            result = self.fget(instance)
        else:
            result = self.method(instance)

        self._GLOBAL_CACHE[cache_key] = result
        return result

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError

        cache_key = f"{instance.__class__.__name__}.{self.method.__name__}"
        if self.fset is None:
            self._GLOBAL_CACHE[cache_key] = value
        else:
            self.fset(instance, value)

    def __delete__(self, instance):
        if instance is None:
            raise AttributeError

        cache_key = f"{instance.__class__.__name__}.{self.method.__name__}"
        if self.fdel is None:
            self._GLOBAL_CACHE.pop(cache_key, None)
        else:
            self.fdel(instance)

    @classmethod
    def clear_cache(cls):
        """清空所有全局缓存"""
        cls._GLOBAL_CACHE.clear()


class LazyWritableProperty(LazyProperty):
    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError

        if self.fset is None:
            setattr(instance, self._cache_name, value)
        else:
            self.fset(instance, value)

    def __delete__(self, instance):
        if instance is None:
            raise AttributeError

        if self.fdel is None:
            delattr(instance, self._cache_name)
        else:
            self.fdel(self._cache_name)


class classproperty:
    """
    Decorator that converts a method with a single cls argument into a property
    that can be accessed directly from the class.
    """

    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def getter(self, method):
        self.fget = method
        return self


def lazy_property_reset(instance, *names):
    for name in names:
        cache_name = f"__cache_{name}"
        if hasattr(instance, cache_name):
            delattr(instance, cache_name)
