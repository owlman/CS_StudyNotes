# llm_tests/test_latency.py
'''
响应延迟与吞吐量观察测试。

测试目标：
- LLM 的响应时间是否在可接受范围内（工程部署的关键约束）；
- 输出长度与延迟之间是否存在可预测的关系；
- 模型在多轮调用后是否出现性能衰减。

对应主文章中"有限理性"（Bounded Rationality）的概念——在任何实际系统中，
响应时间都是智能决策的硬约束。一个"正确但太慢"的模型在工程上是不可用的。
'''
import time
import statistics


class TestLatency:

    def test_llm_response_not_instant(self, ollama_client):
        '''
        验证 LLM 的推理是计算密集型操作，不会瞬时返回。
        这是区分"检索"与"生成"两种行为模式的基本观察。
        '''
        start = time.time()
        ollama_client("请简要说明 TCP 和 UDP 的区别。")
        elapsed = time.time() - start

        # 即使是最简单的推理也需要非零时间→生成不是查找
        assert elapsed > 0.5, (
            f"响应过快（{elapsed:.2f}s），可能未触发实际推理"
        )

    def test_latency_scales_with_output_length(self, ollama_client):
        '''
        验证输出长度与延迟的相关性。
        短指令应比长指令更快返回，如果差异不明显，
        说明瓶颈可能在输入处理（prefill）而非生成（decode）。
        这对于判断系统瓶颈所在有直接的工程参考价值。
        '''
        prompts = {
            "short": "什么是递归？请用一句话回答。",
            "medium": "请详细解释递归算法的原理，并给出至少三个不同领域的应用示例。",
        }
        latencies = {}

        for label, prompt in prompts.items():
            start = time.time()
            result = ollama_client(prompt)
            elapsed = time.time() - start
            latencies[label] = {
                "time": elapsed,
                "tokens": result.get("eval_count", 0),
            }

        # "medium" 通常应比 "short" 生成更多 token
        short_tokens = latencies["short"]["tokens"]
        medium_tokens = latencies["medium"]["tokens"]
        assert medium_tokens > short_tokens, (
            f"长指令生成的 token 数（{medium_tokens}）应大于短指令（{short_tokens}）"
        )

    def test_latency_consistency_across_calls(self, ollama_client):
        '''
        多轮调用的延迟稳定性。
        如果延迟波动过大（如第一轮远慢于后续轮次），可能涉及
        模型加载预热、缓存策略等工程因素，需要在生产设计中加以考虑。
        '''
        prompt = "请用一句话解释什么是操作系统。"
        timings = []

        for _ in range(3):
            start = time.time()
            ollama_client(prompt)
            timings.append(time.time() - start)

        # 计算变异系数（CV），度量延迟的相对离散程度
        mean_latency = statistics.mean(timings)
        stdev_latency = statistics.stdev(timings) if len(timings) > 1 else 0
        cv = stdev_latency / mean_latency if mean_latency > 0 else 0

        # 变异系数建议不超过 50%，如果超过说明延迟极不稳定
        assert cv < 0.5, (
            f"延迟变异系数 CV={cv:.2%}，波动过大，"
            f"各轮延迟分别为 {[f'{t:.2f}s' for t in timings]}"
        )
