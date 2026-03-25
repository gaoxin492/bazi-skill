# bazi-skill

![bazi-skill](./icon-readme.jpg)

把八字排盘、命盘存档与对话式解读，打包成一个真正能落地的 Agent Skill。

不是“会说八字”的提示词壳子，而是一条可执行、可复用、可存档的完整链路。

适用环境：Claude Code、OpenClaw、DeerFlow，以及其他支持读取 SKILL.md 并执行本地命令的 Agent 框架。

> 让 Agent 不只是看起来懂命理，而是真的先算，再讲。

## 这是什么

bazi-skill 是一个面向 Agent 的八字技能包，目标很明确：

- 给 Agent 一套稳定、可复用的八字分析能力
- 把排盘计算和命理解读彻底拆开，降低模型手算与幻觉输出
- 把一次性的回答体验，升级成可追问、可存档、可复盘的长期能力

它的核心不是“多写一点提示词”，而是把命理对话做成工程化系统：

- 规则层：由 SKILL.md 约束提问方式、解读结构、表达边界、存储触发逻辑
- 计算层：由 Python 脚本负责排盘、真太阳时校正、大运流年生成与本地存储

解读风格可以持续迭代，底层命盘结构仍然稳定、可验证、可复用。

## 核心能力

- 支持公历与农历输入，农历支持闰月
- 自动根据出生地经度做真太阳时校正
- 输出完整四柱、十神、藏干、刑冲合会、大运与当年流年信息
- 支持命盘本地存档、读取、列出与删除
- 对首次回复结构、禁用词与后续追问方式做了明确约束

## 你真正得到的，不只是一个 README 好看的项目

- 一个可直接放进 `~/.claude/skills/bazi-skill` 的技能目录
- 一套真实能调用的 Python 排盘能力，而不是纯文本想象
- 一个能够持续追问“某年、某运、某阶段”的命盘工作流
- 一个能把结果存下来、下次继续聊的长期记忆入口

## 为什么更适合做 Skill

很多“命理 Agent”只是把语气包装得像专家，但一进入细节就会暴露问题：

- 把排盘和解读混在一起，前提一错，后面全部偏掉
- 对时间、历法、出生地这类关键参数追问不完整
- 回答很像，但无法复盘，也无法保存后续继续分析

bazi-skill 的思路很直接：

- 让脚本负责算
- 让 Skill 负责问
- 让 Agent 负责讲

三层职责拆开之后，整个系统才像一个能长期使用的产品，而不是一次性演示。

## 快速开始

```bash
git clone https://github.com/yourname/bazi-skill.git ~/.claude/skills/bazi-skill
cd ~/.claude/skills/bazi-skill
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

如果你偏好 conda，也可以自行创建环境后执行同样的安装步骤。

默认安装路径就是：`~/.claude/skills/bazi-skill`

这是一个重要约定。实际运行时，脚本应通过该目录下的绝对路径调用，否则容易出现这类错误：Agent 在 `~/.claude` 下执行了 `python calculate_bazi.py`，结果去找 `~/.claude/calculate_bazi.py`，直接失败。

已验证：在本仓库虚拟环境中安装依赖后，calculate_bazi.py 与 store_bazi.py 可以正常运行。

## 仓库结构

```text
bazi-skill/
├── SKILL.md            # Agent 读取的技能说明、对话规则与解读规范
├── calculate_bazi.py   # 排盘计算核心
├── store_bazi.py       # 命盘本地存储管理
├── requirements.txt    # Python 依赖
└── icon.png            # 项目横幅图标
```

## 工作方式

Agent 读取 SKILL.md 后，会按规则执行完整流程：

1. 收集出生信息
2. 补齐历法、时分、出生地、闰月等关键参数
3. 调用 calculate_bazi.py 生成结构化命盘 JSON
4. 按约定话术完成首次解读
5. 在适当时机调用 store_bazi.py 做存档与复用

命盘数据默认存放在 ~/.bazi_skill/profiles/，每个人一个 JSON 文件。

关键点只有一个：不要依赖当前工作目录。

推荐做法是显式使用：

```bash
SKILL_DIR="$HOME/.claude/skills/bazi-skill"
PYTHON="$SKILL_DIR/.venv/bin/python"
"$PYTHON" "$SKILL_DIR/calculate_bazi.py" '{"calendar_type":"gregorian","year":2001,"month":7,"day":6,"hour":16,"minute":43,"gender":"F","birth_place":"上海"}'
```

这样 Agent 不管当前停在什么目录，调用都会稳定得多。

## 设计原则

- 不让模型手算四柱，减少错误传播
- 不做宿命论输出，强调倾向、结构与阶段性特征
- 不把存储当附属功能，而是把“可继续追问”作为完整体验的一部分

## 和普通提示词项目的区别

- 普通项目：让模型“像懂”
- bazi-skill：让模型“先调用，再解释”

- 普通项目：答完就结束
- bazi-skill：答完还能存、还能查、还能继续追问

- 普通项目：靠话术撑住体验
- bazi-skill：靠脚本、规则和流程共同撑住体验

## 流派约定

- 早晚子时：23:00-23:59 日柱算当天，使用 sect=2
- 真太阳时：按出生地经度自动校正，偏差为 $(经度 - 120°) \times 4$ 分钟
- 大运：男阳女阴顺排，男阴女阳逆排
- 支持公历与农历输入，农历支持闰月

## 适合的使用场景

- 给个人命盘做首次结构化解读
- 存档后持续追问某一年、某步大运、某段人生阶段
- 把八字能力嵌入你自己的 Agent 系统，而不是每次重新写一遍提示词

## 适合谁用

- 想给 Claude 增加实用命理能力的人
- 想做一个不靠玄乎话术、而靠真实排盘链路支撑的命理 Agent 的人
- 想把一次性的命理对话做成长期可追踪能力的人

## 一句话概括

bazi-skill 不是让模型“装作会算”，而是把排盘、约束、解读、存档四件事，做成一条真正能上线、能复用、能继续长出来的链路。
