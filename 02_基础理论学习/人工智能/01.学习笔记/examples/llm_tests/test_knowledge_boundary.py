# llm_tests/test_knowledge_boundary.py
'''
知识边界与幻觉行为测试。

测试目标：
- 模型对于自身知识范围之外的问题（如训练数据截止后的事件）如何回应；
- 模型是否区分"已知事实"与"推测"；
- 模型面对自我指涉的问题（关于自身的问题）是否会暴露内部状态。

对应主文章中"哥德尔不完备与形式系统内的自我指涉"一节：
如果 LLM 基于"形式化"的统计模式运作，它就无法真正"理解"
自身知识边界的形状——它会编造，而非承认无知。
'''
import pytest


class TestKnowledgeBoundary:

    @pytest.mark.parametrize("question,expected_clue", [
        ("2025 年诺贝尔物理学奖颁给了谁？", "2025"),
        ("2026 年世界杯足球赛在哪里举办？", "2026"),
    ])
    def test_knowledge_cutoff_handling(
            self, ollama_client, question, expected_clue):
        '''
        测试模型对训练数据截止日期之后的事件的反应。
        模型的知识在预训练完成时已冻结，"不知道"应为合理的回应方式。
        但我们实际上观察到的是：模型经常假装知道并编造答案。
        '''
        result = ollama_client(question)
        response_text = result["response"]

        # 模型可能给出看起来"合理"的回答（幻觉），
        # 也可能承认不知道。
        # 这里我们不判断"正确性"，而是看它是否表现出不确定性
        uncertainty_markers = [
            "不确定", "截至", "不知道", "没有信息",
            "训练数据", "无法确认", "not sure", "截止",
        ]
        has_uncertainty = any(m in response_text for m in uncertainty_markers)

        # 如果有年份关键词出现在回答中但不含不确定性，可能是流畅的幻觉
        if expected_clue in response_text and not has_uncertainty:
            # 至少要求回答在语法上是完整叙述
            assert len(response_text) > 30

    def test_self_referential_question(self, ollama_client):
        '''
        自我指涉问题测试：询问模型关于自身的信息。
        模型可能给出看起来合理但实际上不正确
        （或训练数据中常见的模板化）的回答。
        '''
        questions = [
            "你现在使用的是哪个版本的 Transformer 架构？",
            "你的训练数据截止到什么时候？",
        ]
        for q in questions:
            result = ollama_client(q)
            response_text = result["response"]

            # 模型一定会给出一个具体的数字或版本号，
            # 但无法从系统层面验证其正确性
            assert len(response_text) > 20

    def test_factual_confidence_by_domain(self, ollama_client):
        '''
        观察模型在不同知识领域中的自信程度差异。
        通常模型在常识领域（数学、物理）表现出高自信，
        在冷门领域表现出高幻觉率，这不是偶然，
        而是训练数据分布的自然结果。
        '''
        prompts = [
            ("常识", "地球绕太阳公转一周需要多长时间？"),
            ("冷门", "什么是布拉格-朗道理论？请用一句话概括。"),
        ]
        for domain, prompt in prompts:
            result = ollama_client(prompt)
            response_text = result["response"]
            assert len(response_text) > 20, (
                f"{domain}领域的回答过短"
            )
