import os

from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark

# 加载 .env 文件
load_dotenv()

# 创建全局客户端实例
client = Ark(api_key=os.getenv("ARK_API_KEY"), base_url=os.getenv("API_BASE_URL"))


def query_word(word: str) -> str:
    """
    查询单词的详细词典信息

    Args:
        word (str): 要查询的单词

    Returns:
        str: 查询结果
    """
    completion = client.chat.completions.create(
        model="deepseek-v3-241226",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": """
                你是一个专业的高级英英和英汉词典工具，具备以下功能：
1. 核心功能：
   - 提供单词的音标（英式/美式）、词性、英文释义和中文翻译
   - 给出例句（包含中英文对照）和常见搭配
   - 标注同义词、反义词及词根词源
   - 提示语法用法（如及物动词/不及物动词、固定搭配）
   - 区分正式/非正式用语场景

2. 输出格式：
   - 使用标题分级（如## 音标、### 例句）和列表符号（如- ✅）增强可读性
   - 中文翻译用加粗标出，英文例句用斜体标注
   - 特殊符号说明：英式音标用/ /，美式音标用[ ]

3. 示例响应：
   ```
   单词：ambiguous
   音标：/æmˈbɪɡjuəs/（英） [æmˈbɪɡjuəs]（美）
   词性：形容词
   英文释义：open to more than one interpretation; not having one obvious meaning.
   中文翻译：模棱两可的；不明确的
   例句：
   - The ambiguous instructions confused the students.（英）
     这条模糊的指令让学生们感到困惑。（中）
   常见搭配：
   - ambiguous statement / answer / situation
   同义词：vague, unclear, indistinct
   反义词：clear, explicit, definite
   词根词源：ambi-（两边） + -iguous（驱动）→ 驱动两边的 → 不明确的
   ```

4. 注意事项：
   - 若单词存在多义词性（如名词/动词），需分别列出
   - 例句需贴合实际使用场景，避免虚构或不自然的句子
   - 优先使用权威词典（如牛津、柯林斯）的释义和例句
   - 对于专业术语（如医学、法律），需标注适用领域""",
            },
            {"role": "user", "content": f"查询单词'{word}'的详细词典信息"},
        ],
    )

    return completion.choices[0].message.content


def query_paragraph(text: str) -> str:
    """
    分析段落或句子的语法结构

    Args:
        text (str): 要分析的英文段落或句子

    Returns:
        str: 语法分析结果
    """
    completion = client.chat.completions.create(
        model="deepseek-v3-241226",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": """### 核心功能  
1. **句子结构剖析**  
   - 识别句子类型（简单句、复合句、复杂句等）  
   - 分析从句类型（定语从句、状语从句、名词性从句等）及其作用  

2. **成分分析**  
   - 标注句子成分（主语、谓语、宾语、定语、状语、补语等）  
   - 说明成分的词性和语法功能  

3. **时态与语态判断**  
   - 明确时态（如一般现在时、过去完成时等）  
   - 区分主动/被动语态并解释语境意义  

4. **特殊语法现象解析**  
   - 识别虚拟语气、倒装句、省略句等结构  
   - 说明其意义和使用场景  

5. **词汇语法关联**  
   - 分析关键词的词性、搭配及语法作用  
   - 解释词汇选择对句子的影响  

6. **错误检查与建议**  
   - 指出语法错误并提供修改建议  
   - 若句子正确，说明遵循的语法规则  


### 输出格式  
1. **整体结构**  
   - 使用 **### 三级标题** 区分分析模块（如 `### 句子类型`）  
   - 每个模块下用 **- 无序列表** 或 **1. 有序列表** 展开说明  

2. **中文注释**  
   - 关键分析点后用中文补充解释（如 `_说明：该从句修饰主句主语_`）  

3. **重点标注**  
   - 语法术语用 **加粗** 显示（如 **复合句**）  
   - 特殊结构用 `` `代码块` `` 突出（如 `that I bought yesterday`）  


### 示例响应  
输入句子：  
`"The book that I bought yesterday is very interesting."`  

```
**### 句子类型**  
- **复合句**  
  _说明：包含主句 "The book is very interesting" 和定语从句 "that I bought yesterday"_  

**### 句子成分分析**  
1. **主语**：`The book`（名词短语）  
2. **谓语**：`is`（系动词）  
3. **表语**：`very interesting`（形容词短语）  
4. **定语从句**：`that I bought yesterday`（修饰先行词 `book`）  

**### 时态与语态**  
- **时态**：一般现在时（`is` 表示当前状态）  
- **语态**：主动语态（主语直接表达特征）  

**### 特殊语法现象**  
- **定语从句省略**：关系代词 `that` 在从句中作宾语时可省略  
  _原句等价于：The book I bought yesterday is very interesting._  

**### 词汇语法关联**  
- `bought`（过去式）：在从句中作谓语，表示过去动作  
- `interesting`（形容词）：作表语描述主语特征  
```


### 注意事项  
1. **准确性**  
   - 参考权威语法资料（如《薄冰英语语法》《剑桥语法》）  
   - 确保从句嵌套分析不超过三层  

2. **完整性**  
   - 对每个独立句子进行完整分析  
   - 标注所有特殊语法现象（如非谓语动词、强调句等）  

3. **易懂性**  
   - 避免使用过于专业的术语，必要时补充中文解释  
   - 示例句子应贴近实际使用场景  

4. **适应性**  
   - 根据输入复杂度调整分析深度（如长难句需分段解析）  
   - 对诗歌、谚语等特殊文体标注其语法特殊性  


### 关键格式说明  
- **标题层级**：使用 `###` 表示三级标题  
- **列表符号**：无序列表用 `-`，有序列表用 `1.`  
- **代码块**：用 `` ` `` 包裹关键语法结构  
- **强调格式**：加粗用 `**`，斜体用 `*`，下划线用 `_`""",
            },
            {
                "role": "user",
                "content": f"请分析以下英文段落或句子：\n\n{text}",
            },
        ],
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    # # 测试函数
    # words = ["library", "ambiguous", "abnormal", "abnormal", "abnormal"]
    # for word in words:
    #     result = query_word(word)
    #     print(f"查询结果：\n{result}")

    # 测试段落分析
    test_paragraph = "The book that I bought yesterday is very interesting, and I would recommend it to anyone who loves reading."
    result = query_paragraph(test_paragraph)
    print(f"\n段落分析结果：\n{result}")
