import os
import time
import logging
import asyncio
from typing import Union, Literal
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import netCDF4 as nc

logger = logging.getLogger(__name__)

def smart_wait(
    path: str,
    timeout: Union[int, float] = 300,
    mode: Literal['auto', 'watchdog', 'polling', 'async'] = 'auto',
    debug: bool = False
) -> bool:
    """
    智能文件等待方案（自动选择最优策略）
    
    Args:
        path: 要监控的文件路径
        timeout: 最大等待时间（秒）
        mode: 运行模式，可选：
            - 'auto'：自动选择（默认）
            - 'watchdog'：文件系统事件监听
            - 'polling'：指数退避轮询
            - 'async'：异步协程模式
        debug: 调试模式（立即返回当前状态）
    
    Returns:
        bool: 文件是否存在且有效
        
    Raises:
        ValueError: 当输入参数无效时
    """
    # 参数验证
    if timeout <= 0:
        raise ValueError("Timeout must be positive")
    
    if debug:
        return _immediate_check(path)
    
    # 模式自动选择逻辑
    if mode == 'auto':
        mode = 'watchdog' if timeout > 60 else 'polling'
    
    try:
        if mode == 'watchdog':
            return _watchdog_wait(path, timeout)
        elif mode == 'async':
            return asyncio.run(_async_wait(path, timeout))
        elif mode == 'polling':
            return _polling_wait(path, timeout)
        else:
            raise ValueError(f"Invalid mode: {mode}")
    except Exception as e:
        logger.error(f"Smart wait failed: {str(e)}")
        return False

def _immediate_check(path: str) -> bool:
    """调试模式下的立即检查"""
    if not os.path.exists(path):
        logger.debug(f"[DEBUG] File not exists: {path}")
        return False
    
    try:
        if path.lower().endswith('.nc'):
            with nc.Dataset(path) as ds:
                if not ds.variables:
                    logger.debug(f"[DEBUG] Empty NetCDF: {path}")
                    return False
        logger.debug(f"[DEBUG] File valid: {path}")
        return True
    except Exception as e:
        logger.debug(f"[DEBUG] Invalid file {path}: {str(e)}")
        return False

def _watchdog_wait(path: str, timeout: Union[int, float]) -> bool:
    """基于文件系统事件的等待"""
    class FileHandler(FileSystemEventHandler):
        def __init__(self, callback):
            self.callback = callback
        
        def on_created(self, event):
            if event.src_path == os.path.abspath(path):
                self.callback()

    result = False
    event = threading.Event()
    
    def on_file_ready():
        nonlocal result
        try:
            if path.lower().endswith('.nc'):
                with nc.Dataset(path) as ds:
                    if ds.variables:
                        result = True
            else:
                result = True
        finally:
            event.set()

    handler = FileHandler(on_file_ready)
    observer = Observer()
    observer.schedule(handler, os.path.dirname(path) or '.')
    observer.start()
    
    try:
        event.wait(timeout)
    finally:
        observer.stop()
        observer.join()
    
    return result

async def _async_wait(path: str, timeout: Union[int, float]) -> bool:
    """异步协程等待实现"""
    async def _check():
        while True:
            if os.path.exists(path):
                try:
                    if path.lower().endswith('.nc'):
                        with nc.Dataset(path) as ds:
                            if ds.variables:
                                return True
                    else:
                        return True
                except Exception:
                    pass
            await asyncio.sleep(1)
    
    try:
        return await asyncio.wait_for(_check(), timeout)
    except asyncio.TimeoutError:
        return False

def _polling_wait(path: str, timeout: Union[int, float]) -> bool:
    """指数退避轮询实现"""
    wait_sec = 1
    start_time = time.time()
    
    while (time.time() - start_time) < timeout:
        if os.path.exists(path):
            try:
                if path.lower().endswith('.nc'):
                    with nc.Dataset(path) as ds:
                        if ds.variables:
                            return True
                else:
                    return True
            except Exception as e:
                logger.warning(f"File validation failed: {str(e)}")
        
        elapsed = time.time() - start_time
        remaining = timeout - elapsed
        next_wait = min(wait_sec, remaining)
        
        if next_wait <= 0:
            break
            
        time.sleep(next_wait)
        wait_sec = min(wait_sec * 2, 60)  # 上限60秒
    
    return False

"""
# 基本用法（自动选择最佳模式）
success = smart_wait("/data/sample.nc", timeout=120)

# 强制使用watchdog模式
success = smart_wait("/data/sample.nc", mode='watchdog')

# 调试模式
print(smart_wait("/data/sample.nc", debug=True))

"""