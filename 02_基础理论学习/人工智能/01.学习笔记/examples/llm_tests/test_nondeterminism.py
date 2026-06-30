# llm_tests/test_nondeterminism.py
'''
非确定性输出测试——LLM 的核心特性之一。

测试目标：
- 在默认参数（temperature>0）下，同一 prompt 的输出是否具有多样性；
- 在固定参数（temperature=0, seed=42）下，输出是否可复现；
- 非确定性是否影响关键信息的一致性（事实类回答偏差）。

对应主文章中"概率转向"的核心洞察：LLM 本质上是一个概率模型，
其输出是分布上的采样而非确定性计算。这一特性既是灵活性的来源，
也是工程可靠性的挑战。
'''


class TestNondeterminism:

    def test_default_output_is_diverse(self, ollama_client):
        '''
        在默认参数（temperature 未指定）下，多次调用同一 prompt，
        输出应大概率不同。这个测试直接验证 LLM 的"概率采样"本质。
        '''
        prompt = "请用一句诗形容秋天的黄昏。"
        outputs = []

        for _ in range(3):
            result = ollama_client(prompt)
            outputs.append(result["response"].strip())

        unique_outputs = set(outputs)
        # 三次调用至少应出现两种不同的回答
        assert len(unique_outputs) >= 2, (
            f"三次调用输出了完全相同的文本，说明采样机制可能未生效。"
        )

    def test_deterministic_output_is_repeatable(
            self, deterministic_client):
        '''
        在固定 temperature=0, seed=42 的条件下，
        多次调用应产生完全一致的输出。
        这对工程可复现性和调试至关重要。
        '''
        prompt = "请给出一个 JSON，对象中包含 name 和 age 两个字段。"
        outputs = []

        for _ in range(3):
            result = deterministic_client(prompt)
            outputs.append(result["response"].strip())

        # 固定参数下输出应完全一致
        assert all(o == outputs[0] for o in outputs), (
            "固定 temperature=0, seed=42 时输出仍不一致，"
            "可能涉及其他随机性来源（如采样后端、硬件浮点差异）"
        )

    def test_nondeterminism_affects_factual_consistency(self, ollama_client):
        '''
        非确定性对事实类回答的影响测试。
        即使 temperature 较低，模型在不同次调用中
        对已知事实的表述细节可能不同，
        但核心信息应保持一致。

        此测试不判定"对错"，而是观察偏差的类型和幅度。
        '''
        prompt = "光速大约是多少？请给出具体数值和单位。"
        responses = []

        for _ in range(3):
            result = ollama_client(prompt)
            responses.append(result["response"].strip())

        # 验证每次回答都包含"千米/秒"或"m/s"之类的单位关键词
        unit_keywords = ["千米/秒", "km/s", "米/秒", "m/s", "×10⁸"]
        for resp in responses:
            has_unit = any(kw in resp for kw in unit_keywords)
            assert has_unit, (
                f"回答缺少单位：{resp[:50]}..."
            )
