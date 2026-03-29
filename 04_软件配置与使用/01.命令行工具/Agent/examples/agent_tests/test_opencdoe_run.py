import subprocess

tasks = [
    "使用 Python 编写并执行一个 hello world 程序",
    "使用 Python 编写并执行一个计算斐波那契数列的程序",
    "使用 Python 编写并执行一个计算阶乘的程序",
    "使用 Python 编写并执行一个计算素数的程序",
    "使用 Python 编写并执行一个计算回文数的程序",
]

for task in tasks:
    try:
        result = subprocess.run(
            ["opencode", "run", task],
            capture_output=True,
            text=True,
            check=True,
            timeout=120
        )
        print(f"任务成功: {task}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"任务失败: {task}")
        print(e.stderr)
    except subprocess.TimeoutExpired:
        print(f"任务超时: {task}")
