import os
from .importhooks import ImportHooks
from .paths import base_dir, cache_dir

def site_init():
    "initialization, called from sitecustomize"
    # set up torchinductor cache
    if 'TORCHINDUCTOR_CACHE_DIR' not in os.environ:
        ti_cache = cache_dir / 'torchinductor'
        os.environ['TORCHINDUCTOR_CACHE_DIR'] = str(ti_cache)

    # 8 processes is probably a more reasonable default
    if 'TORCHINDUCTOR_COMPILE_THREADS' not in os.environ:
        if hasattr(os, 'sched_getaffinity'):
            allowed_threads = len(os.sched_getaffinity(0))
        else:
            allowed_threads = os.cpu_count()

        max_threads = 8
        if 'TORCHINDUCTOR_COMPILE_MAX_THREADS' in os.environ:
            max_threads = int(os.environ['TORCHINDUCTOR_COMPILE_MAX_THREADS'])

        allowed_threads = min(max_threads, allowed_threads)
        os.environ['TORCHINDUCTOR_COMPILE_THREADS'] = str(allowed_threads)

    # initialize import hooks
    importhooks = ImportHooks.register()

    @importhooks.hook_after_load('torch.cuda')
    def _torch_cuda_disable_spinwait(module):
        if not module.is_available() or os.environ.get('MLCOMMON_CUDA_ALLOW_SPINWAIT') == 1:
            return

        import ctypes
        try:
            cudart = ctypes.CDLL('libcudart.so')
            # cudaDeviceScheduleBlockingSync = 0x04
            cudart.cudaSetDeviceFlags(4)
            # check if it worked
            # i = ctypes.c_uint()
            # cudart.cudaGetDeviceFlags(ctypes.byref(i))
            # print('cudaGetDeviceFlags():', i)
        except:
            # ignore
            pass
