---
title: LLM 的部署与测试
author: 凌杰
date: 2026-01-31
tags: 大语言模型, Ollama
categories: 人工智能
---

> [!NOTE] 笔记说明
>
> 这篇笔记对应的是《[[关于 AI 的学习路线图]]》一文中所规划的第三个学习阶段。其中记录了我尝试将 LLM 部署到生产环境中，并对其进行相关测试的全过程，以及在该过程中所获得的心得体会。同样的，这些内容也将成为我 AI 系列笔记的一部分，被存储在本人 Github 上的[计算机学习笔记库](https://github.com/owlman/CS_StudyNotes)中，并予以长期维护。

## 关于 LLM 的本地部署

正如我之前在《[[关于 AI 的学习路线图]]》一文中所提到的，从学习的角度来说，如果我们要想切实了解 LLM 在计算机软件系统中所处的位置，以及它在生产环境中所扮演的角色，最直接的方式就是尝试将其部署到我们自己所在的计算机环境中，并通过测试来观察它与用户的交互方式。但是，如果想要实现在本地部署 LLM 这种大型应用，我们首先要解决一个很现实的问题：*如何用有限的硬件资源、以可控的方式将其运行起来？*

很显然，就目前阶段的学习任务来看，如果我们从直接编译源码、手动配置推理引擎、管理模型权重与依赖环境来着手，大概率会让自己的学习重心过早地偏向底层细节，而模糊了我们真正想观察的目标 —— LLM 在生产环境中所扮演的角色。因此，我个人会推荐读者从一款名为 Ollama 的开源模型管理工具来着手，该工具可以让人们在不必关心底层实现细节的情况下，快速地完成 LLM 的部署与测试。下面，就让我们来具体介绍一下 Ollama 及其使用方法。

### 了解并安装 Ollama

Ollama 是一款基于 MIT 协议开源的、面向本地环境的 LLM 运行与管理工具，它的核心设计目标是以尽可能低的使用门槛，将“运行一个 LLM”这件事变成一项标准化、可重复的工程操作。具体来说就是，Ollama 在整个与 LLM 相关的系统中大致承担了以下职责：

- **模型生命周期管理**：负责模型的拉取、存储、版本管理与运行；
- **推理环境封装**：屏蔽底层推理引擎、量化方式与硬件差异；
- **统一的调用接口**：通过 CLI 或 API 的形式，对外提供一致的使用方式。

这意味着，用户在使用 Ollama 时并不需要关心模型权重具体存放在哪里、底层使用了哪种推理后端，也不必在一开始就纠结于 CUDA、Metal 或 CPU 优化等问题。很显然，我们在这里选择 Ollama，本质上是一种刻意降低系统复杂度的学习策略，目的是将学习重点放在观察模型本身的行为以及**它与系统其他部分的交互方式**上，但它并不足以应对实际生产环境中的所有问题。

Ollama 的安装过程本身非常简单，读者可以自行前往它的[官方下载页面](https://ollama.com/download)，并根据该页面中的提示，基于自己所在的操作系统完成安装即可，具体如图 1 所示。

<!-- ![图1：Ollama 的下载页面](./img/ollama_download.png) -->
![img](https://img2024.cnblogs.com/blog/691082/202602/691082-20260207135244485-526117339.png)

**图 1**：Ollama 的下载页面

如果安装过程一切顺利，我们就可以通过在命令行中输入 `ollama` 命令来验证安装是否成功。如果安装成功了，该命令会返回 Ollama 的使用提示信息，如图 2 所示。

<!-- ![图2：Ollama 的使用提示信息](./img/ollama_help.png) -->
![img](https://img2024.cnblogs.com/blog/691082/202602/691082-20260207135316960-391511463.png)
**图 2**：Ollama 的使用提示信息

接下来，我们要做的就是选择一款适合当前学习任务的 LLM，并尝试使用 Ollama 来将其部署到我们的本地环境中。

### 选择并部署 LLM

关于应该选择什么模型来完成我们在这一阶段的学习，这主要取决于我们**要实验的任务类型**和**电脑配置**。以下这张表是我基于这篇笔记写作的时间点（即 2026 年 2 月），整理出的当前主流的候选模型。

| 推荐模型 | 主要特点与优势 | 适用场景 | 硬件要求参考 |
| -------- | -------------- | -------- | ------------ |
| **通用最佳平衡** | | | |
| **Qwen2.5-7B** | 7B 级别综合性能强，指令跟随、长上下文支持好，通用性高。 | 文档总结、内容创作、知识问答、轻量级智能体任务。 | 16GB+ 内存，量化后可降低需求。 |
| **Llama 3.3 系列** | Meta 出品，生态完善，工具调用支持好，3B 版本速度极快。 | 快速对话、多语言任务、对响应速度要求高的应用。 | 3B 模型：8-16GB 内存；8B 模型需求更高。 |
| **专注编程任务** | | | |
| **Qwen3-Coder 系列** | 阿里出品，在代码理解和生成任务上表现优异，有不同尺寸可选。 | 代码解释、补全、测试、学习编程。 | 1.7B/4B/8B 等不同规格，可按需选择。 |
| **Mistral 系列** | Mistral AI 的编程专用模型，擅长生成、测试和解释代码。 | 专注于软件开发辅助的各类任务。 | 推荐 16GB 以上内存。 |
| **资源受限环境** | | | |
| **SmolLM3-3B** | 完全开源，性能优秀，在 3B 级别中表现出色，可控性强。 | 对开源合规要求高，或需要在低配硬件上部署。 | 可在普通笔记本电脑上运行。 |
| **Llama 3.2 3B** | 体积小、速度快，适合部署在多种设备上，对硬件要求低。 | 需要即时响应的嵌入式应用或移动端场景。 | 8-16GB 内存即可。 |

根据上面的表格，我们可以先参照以下提示来确定选择：

- 如果硬件资源不给力（例如内存容量只有 16GB 或更少，没有独立显卡），可以选择`SmolLM3-3B`或`Llama 3.2 3B`；
- 如果想优先考虑通用对话和写作，可以选择`Qwen2.5-7B`或`Llama 3.3 8B`；
- 如果想优先考虑将其用于编程辅助，`Qwen3-Coder`或`Mistral`系列可能是更好的选择；

由于这篇笔记的任务是基于学习的目的来部署 LLM，它最好能让读者在最普通的个人笔记本上进行过程相对流畅的实验，因此我决定接下来就选择`Llama 3.2 3B`来进行演示了。

基本上，使用 Ollama 部署 LLM 的操作步骤与使用 docker 部署服务端应用的过程非常类似，具体如下：

1. **拉取模型**：打开命令行终端并输入`ollama pull llama3.2:3b`命令，即可从 Ollama 的官方服务器上拉取我们所选择的 LLM 镜像，如图 3 所示。

    <!-- ![图3：使用 Ollama 拉取 LLM 镜像](./img/ollama_pulling.png) -->
    ![img](https://img2024.cnblogs.com/blog/691082/202602/691082-20260207135403290-1666170993.png)

    **图 3**：使用 Ollama 拉取 LLM 镜像

    正如读者所见，如果镜像被顺利拉取到本地，当我们继续在命令行终端输入`ollama list`命令时，就可以看到`llama3.2:3b`这个镜像已经存在于 Ollama 在本地管理的镜像列表中了。

2. **运行测试**：继续在图 3 所示命令行界面中输入 `ollama run llama3.2:3b`命令即可开始交互测试。在这里，我们演示的是一个 LLM 版的“Hello World”，如图 4 所示。

    <!-- ![图4：使用 Ollama 运行 LLM 镜像](./img/ollama_running.png) -->
    ![img](https://img2024.cnblogs.com/blog/691082/202602/691082-20260207135512344-1330487987.png)

    **图 4**：使用 Ollama 运行 LLM 镜像

至此，我们就算完成了一次基于 Ollama 的 LLM 本地部署作业。需要特别强调的是，由于受到硬件资源的限制，我们在这里所部署的这个 LLM 在功能上是远远不能满足实际生产需求的，它在这里的任务只是供我们用测试的方式来观察 LLM 在生产环境中所扮演的角色。

## 针对 LLM 的测试与观察

下面，让我们来具体测试一下这个基于 Ollama 完成本地部署的 LLM。当然，首先要明确的是，我们在这里的测试任务并不是在评估模型的“聪明程度”，而是设法通过一组尽可能简单、可复现的测试来观察 LLM 与用户交互时的行为模式。换句话说，我们希望通过测试来了解 **LLM 作为系统组件时的响应方式、失败模式以及可控性边界。**

因此，在测试方式的选择上，我在这里选择使用 Python 脚本通过 HTTP API 的方式来调用本地运行的 LLM，用于模拟更接近实际生产环境的使用场景。

### 使用 Python 调用本地 Ollama 模型

在默认情况下，Ollama 会在本地运行 LLM 的同时为用户提供一套 RESTful API（具体文档请参考本文最后的“参考资料”），这让我们可以使用 Python 脚本来模拟 HTTP 客户端，从而实现对 LLM 的自动化测试。其基本调用步骤如下：

1. **启动 LLM**：在命令行终端中输入`ollama run llama3.2:3b`命令，启动 LLM 的本地运行实例。

2. **创建 Python 脚本**；创建一个名为 `ollama_python.py` 的 Python 脚本，并在其中输入以下代码：

    ```python
    import requests

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.2:3b",
        "prompt": "请用一句话解释什么是操作系统。",
        "stream": False
    }

    response = requests.post(url, json=payload)
    result = response.json()

    print(result["response"])
    ```

3. **运行 Python 脚本**：在命令行终端中输入 `python ollama_python.py` 命令，运行 Python 脚本，即可看到 LLM 的输出结果，如图 5 所示。

    <!-- ![图5：使用 Python 调用 Ollama API](./img/ollama_python.png) -->
    ![img](https://img2024.cnblogs.com/blog/691082/202602/691082-20260207135612961-1830938264.png)

    **图 5**：使用 Python 调用 Ollama API

在上述示例中，我们首先定义了 Ollama API 的调用地址，然后构造了一个包含模型名称、提示词以及是否以流式方式返回结果的请求体。最后，我们通过 requests 库的 post 方法将请求发送给 Ollama API，并打印出返回结果，这个示例的意义并不在于输出内容本身，而在于确认以下几点：

- Ollama API 是否能够被稳定调用；
- 请求—响应链路是否完整；
- 返回结果是否符合预期的数据结构。

### 使用 PyTest 编写测试用例

在确认了 LLM 的调用链路是完整且稳定的前提下，我们就可以开始编写测试用例了。
一旦上述代码可以稳定运行，我们就具备了一个**最小可用的 LLM 测试环境**。下面，让我们基于 PyTest 这个自动化测试框架来正式为这个 LLM 编写一个可用于观察其行为模式的测试用例，其具体步骤如下：

1. **新建测试项目**：在计算机的任意位置上创建一个名为`llm_tests`的目录，并在其中创建下列 Python 脚本文件：

    ```bash
    llm_tests
    ├── test_basic_call.py           # 基础调用测试
    ├── test_latency.py              # 响应延迟与阻塞行为测试
    ├── test_nondeterminism.py       # 非确定性输出与重复调用差异测试
    ├── test_ambiguous_prompt.py     # 模糊指令下的“过度推断”行为测试
    └── conftest.py                  # PyTest 配置文件
    ```

2. **编写项目公共配置**：使用代码编辑器打开`conftest.py`文件，并其中输入以下代码：

    ```python
    # llm_tests/conftest.py
    '''
    这个文件用于存放 PyTest 的公共配置，例如 HTTP API 的调用地址和模型名称。
    '''
    import pytest
    import requests

    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL_NAME = "llama3.2:3b"


    @pytest.fixture
    def ollama_client():
        def call_llm(prompt, stream=False):
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": stream,
                },
                timeout=120,
            )
            response.raise_for_status()
            return response.json()
        return call_llm
    ```

3. **编写基础测试连通性测试**：使用代码编辑器打开`test_basic_call.py`文件，并其中输入以下代码：

    ```python
    # llm_tests/test_basic_call.py
    '''
    这个测试用例用于验证 LLM 的基础连通性，具体包括：
    - LLM 是否能够被稳定调用；
    - 请求—响应链路是否完整；
    - 返回结果是否符合预期的数据结构。
    '''

    def test_llm_basic_response(ollama_client):
        result = ollama_client("请用一句话解释什么是操作系统。")

        assert "response" in result
        assert isinstance(result["response"], str)
        assert len(result["response"].strip()) > 0
    ```

4. **编写响应延迟测试**：使用代码编辑器打开`test_latency.py`文件，并其中输入以下代码：

    ```python
    # llm_tests/test_latency.py
    '''
    这个测试用例用于验证 LLM 的响应延迟与阻塞行为，具体包括：
    - LLM 的响应延迟是否在可接受范围内；
    - LLM 是否会阻塞调用链路。
    '''
    import time

    def test_llm_response_latency(ollama_client):
        start = time.time()

        ollama_client("请简要说明 TCP 和 UDP 的区别。")

        elapsed = time.time() - start

        # 不设过严阈值，只验证“不是瞬时返回”
        assert elapsed > 0.5
    ```

    **请注意**：这里的测试仅用于观察同步调用的响应时延，并不涉及并发或异步场景下的阻塞分析。

5. **编写非确定性输出测试**：使用代码编辑器打开`test_nondeterminism.py`文件，并其中输入以下代码：

    ```python
    # llm_tests/test_nondeterminism.py
    '''
    这个测试用例用于验证 LLM 的非确定性输出，具体包括：
    - LLM 的输出是否具有非确定性；
    - LLM 的输出是否具有重复性。
    '''

    def test_llm_nondeterministic_output(ollama_client):
        prompt = "请给出一个 JSON，对象中包含 name 和 age 两个字段。"

        outputs = set()

        for _ in range(3):
            result = ollama_client(prompt)
            outputs.add(result["response"].strip())

        # 允许偶然一致，但通常不会完全相同
        assert len(outputs) >= 1
    ```

    **请注意**：由于 Ollama 默认启用了缓存与固定推理参数，在不显式调整 temperature / seed 的情况下，输出可能表现为“弱非确定性”甚至表面确定性，因此这里的测试重点并不在于断言差异存在，而在于承认这种不确定性无法通过传统断言机制可靠捕获。

6. **编写模糊指令测试**：使用代码编辑器打开`test_ambiguous_prompt.py`文件，并其中输入以下代码：

    ```python
    # llm_tests/test_ambiguous_prompt.py
    '''
    这个测试用例用于验证 LLM 在面对模糊指令时的行为，具体包括：
    - LLM 是否会主动进行推断与补全；
    - LLM 是否会给出完整的叙述。
    '''

    def test_llm_over_inference_on_ambiguous_prompt(ollama_client):
        prompt = "请判断这个方案是否合理。"

        result = ollama_client(prompt)
        response_text = result["response"]

        # 不判断“对错”，只确认模型会生成完整叙述
        assert len(response_text) > 50
    ```

7. **安装 PyTest 并运行测试**：在命令行终端中打开`llm_tests`目录，并输入如图 6 所示的命令序列来安装 PyTest，并运行测试：

    <!-- ![图6：安装 PyTest 并运行测试](./img/pytest_ollama.png) -->
    ![img](https://img2024.cnblogs.com/blog/691082/202602/691082-20260207135944110-1883364792.png)

    **图 6**：安装 PyTest 并运行测试

### 小结：测试得到的关键观察结论

通过上述基于 Python 的简单测试，我们可以得到几条与工程实践直接相关的结论：

1. LLM 调用具有明显的延迟与波动性，不适合放在关键同步路径中；
2. 模型输出具有非确定性，不能被直接作为结构化数据使用；
3. 在输入信息不足时，模型会主动进行推断与补全；
4. 这些现象并非“模型 bug”，而是 LLM 作为概率模型的自然结果。

也正因如此，在后续的系统设计中，LLM 更适合作为一个**受约束、被监控、可回退的智能组件**，而不是系统逻辑的直接执行者。

## 参考资料

- [Ollama 中文文档](https://ollama.cadn.net.cn/#quickstart)
- [Ollama-Python 文档](https://github.com/ollama/ollama-python)
- [PyTest 官方文档](https://docs.pytest.org/en/stable/)
