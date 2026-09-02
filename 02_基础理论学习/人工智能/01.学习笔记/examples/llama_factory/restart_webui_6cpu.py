"""
重启 WebUI，带 OMP_NUM_THREADS=6 和 MKL_NUM_THREADS=6 环境变量。
这样从 WebUI 启动的训练进程会自动继承这些环境变量，PyTorch 能用上多核。
"""
import subprocess, os, time

LLAMACLI = r'D:\PythonVenv\global312\Scripts\llamafactory-cli.exe'
LOG_DIR = r'C:\Users\Administrator\AppData\Local\Temp\opencode'
WORK_DIR = r'D:\Working\writing\CS_StudyNotes\02_基础理论学习\人工智能\01.学习笔记\examples\llama_factory'

env = dict(os.environ)
env['OMP_NUM_THREADS'] = '6'
env['MKL_NUM_THREADS'] = '6'
env['CUDA_VISIBLE_DEVICES'] = ''
env['ASCEND_RT_VISIBLE_DEVICES'] = ''
env['PYTHONIOENCODING'] = 'utf-8'

log_out = open(os.path.join(LOG_DIR, 'webui3.out'), 'w', encoding='utf-8')
log_err = open(os.path.join(LOG_DIR, 'webui3.err'), 'w', encoding='utf-8')

p = subprocess.Popen([LLAMACLI, 'webui'], cwd=WORK_DIR, env=env,
                     stdout=log_out, stderr=log_err, stdin=subprocess.DEVNULL)
print(f'WebUI 已启动，PID={p.pid}')
print(f'OMP_NUM_THREADS=6, MKL_NUM_THREADS=6')
print(f'日志: {LOG_DIR}\\webui3.out / webui3.err')