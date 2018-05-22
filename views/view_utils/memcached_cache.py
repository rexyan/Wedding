# encoding=utf8
import hashlib
import os
import time
__all__ = ['get', 'set', 'memorize', 'memcache_client']
import memcache
import settings
import redis

pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
memcache_client = redis.Redis(connection_pool=pool)

# 以前是memcached，现在改为redis，见上面
# memcache_client = memcache.Client(
    # ['%s:%s' % (settings.MEMCACHE_SERVER, str(settings.MEMCACHE_PORT))])

OBJ_DICT = {}
OBJ_DICT2 = {}
OBJ_EXPIRE_DICT = {}
OBJ_EXPIRE_DICT2 = {}
DEFAULT_EXPIRE_SECONDS = 300
DEFAULT_VERSION_EXPIRE_SECONDS = 60 * 60 * 24
MEMORY_CLEANER_PERIOD = 600
OBJ_VERSION_DICT = {}
def set(key, value, time=settings.MEMCACHE_EXPIRE_TIME):
    """time为过期时间，以秒为单位"""
    return memcache_client.set(str(key), value, time)
def get(key):
    return memcache_client.get(str(key))
def set_remote_obj_version(key, version):
    return memcache_client.set(str(key), version, DEFAULT_VERSION_EXPIRE_SECONDS)
def get_remote_obj_version(key):
    return memcache_client.get(str(key)) or 0
def set_local_obj_version(key, version):
    OBJ_VERSION_DICT[key] = version
def get_local_obj_version(key):
    return OBJ_VERSION_DICT.get(key) or 0
def version_expired(key):
    local_version = get_local_obj_version(key)
    remote_version = get_remote_obj_version(key)
    return local_version != remote_version
def delete_all():
    delete_list = []
    for key, value in OBJ_DICT.iteritems():
        delete_list.append(key)
    memcache_client.delete_multi(delete_list)
def start_memory_cleaner(count_down=MEMORY_CLEANER_PERIOD):
    while True:
        time.sleep(count_down)
        keys_to_remove = []
        for key, value in OBJ_EXPIRE_DICT.iteritems():
            if OBJ_EXPIRE_DICT[key] < int(round(time.time())):
                keys_to_remove.append(key)
        for key in keys_to_remove:
            try:
                del OBJ_DICT[key]
                del OBJ_EXPIRE_DICT[key]
                del OBJ_VERSION_DICT[key]
            except KeyError:
                pass
        for key, value in OBJ_EXPIRE_DICT2.iteritems():
            if OBJ_EXPIRE_DICT2[key] < int(round(time.time())):
                keys_to_remove.append(key)
        for key in keys_to_remove:
            try:
                del OBJ_DICT[key]
                del OBJ_EXPIRE_DICT2[key]
                del OBJ_VERSION_DICT[key]
            except KeyError:
                pass

memory_cleaner_thread_started = False
def start_memory_cleaner_thread():
    global memory_cleaner_thread_started
    import threading
    if not memory_cleaner_thread_started:
        threading.Thread(target=start_memory_cleaner, args=(),
                         name='memory_cleaner_thread').start()
        memory_cleaner_thread_started = True
def memorize(function):
    """内存缓存, 用于不定参数的函数
    Usage:
        def xxx(key1,key2,refresh=False)
            return instance
        def xxx(key1,key2,key2,x1=xx,x2=yyy)
            return instance
    """
    def helper(*args, **kwargs):
        refresh = False
        expire = None
        if 'refresh' in kwargs:
            refresh = kwargs['refresh']
        if 'expire' in kwargs:
            expire = kwargs['expire']
        # make cache key
        args_str = []
        for arg in args:
            if isinstance(arg, unicode):
                args_str.append(arg.encode('utf-8'))
            else:
                args_str.append(str(arg))
        key = function.__name__ + hashlib.md5('#'.join(args_str)).hexdigest()
        # end make cache key
        remote_version = get_remote_obj_version(key)
        ret_obj = None
        if refresh:
            # 1.
            remote_version += 1
            set_remote_obj_version(key, remote_version)
            # #当主动刷新时，直接调用；且主动更新本地缓存（可以不做，只是其他程序调用时进入#3段，重复调用一次再更新本地缓存）
            # ret_obj = function(*args, **kwargs)
            # OBJ_DICT[key] = ret_obj
            # set_local_obj_version(key, remote_version)
        else:
            if remote_version == 0:
                # 2
                ret_obj = function(*args, **kwargs)
                OBJ_DICT[key] = ret_obj
                set_remote_obj_version(key, 1)
                set_local_obj_version(key, 1)
            else:
                local_version = get_local_obj_version(key)
                if local_version != remote_version:
                    # 3
                    ret_obj = function(*args, **kwargs)
                    OBJ_DICT[key] = ret_obj
                    set_local_obj_version(key, remote_version)
                else:
                    # 4
                    if key in OBJ_DICT:
                        # 5
                        ret_obj = OBJ_DICT[key]
                    else:
                        ret_obj = function(*args, **kwargs)
                        OBJ_DICT[key] = ret_obj
        return ret_obj
    return helper

if __name__ == '__main__':
    pass