import threading

class SingletonBase:
    """スレッドセーフなシングルトン基底クラス"""
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(*args, **kwargs)
            return cls._instance

# SingletonBaseを継承してシングルトンを実現
class SingletonClass(SingletonBase):
    def __init__(self):
        print("インスタンス生成")

# テストコード
def create_instance():
    instance = SingletonClass.get_instance()
    print(f"インスタンスID: {id(instance)}")

threads = [threading.Thread(target=create_instance) for _ in range(10)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()