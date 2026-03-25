# bazi-skill

八字命理分析 Agent Skill。通过调用本地 Python 脚本完成排盘计算与命盘存储，由你负责解读。

默认安装目录固定为：`~/.claude/skills/bazi-skill`

## 脚本清单

| 脚本 | 用途 |
|------|------|
| `calculate_bazi.py` | 排盘计算，输出完整命盘 JSON |
| `store_bazi.py` | 命盘本地存储（保存 / 读取 / 列出 / 删除） |

---

## 初始化（首次使用时执行）

不要假设当前工作目录就是 skill 目录。统一使用下面两个变量：

```bash
SKILL_DIR="$HOME/.claude/skills/bazi-skill"
if [ -x "$SKILL_DIR/.venv/bin/python" ]; then
	PYTHON="$SKILL_DIR/.venv/bin/python"
else
	PYTHON=python3
fi
```

后续所有命令都基于 `$SKILL_DIR` 和 `$PYTHON` 执行，不要直接写相对路径 `calculate_bazi.py`，否则可能在 `~/.claude` 或其他目录下报找不到文件。

推荐初始化方式：

```bash
SKILL_DIR="$HOME/.claude/skills/bazi-skill"
if [ -x "$SKILL_DIR/.venv/bin/python" ]; then
	PYTHON="$SKILL_DIR/.venv/bin/python"
else
	PYTHON=python3
fi

$PYTHON -c "import lunar_python, timezonefinder, geopy, pytz" 2>/dev/null || \
$PYTHON -m pip install -r "$SKILL_DIR/requirements.txt" -q
```

如果仓库里没有 `requirements.txt`，则安装以下依赖：

```bash
$PYTHON -m pip install lunar-python timezonefinder geopy pytz -q
```

依赖安装成功后正常调用脚本。无需每次检查，只在首次或环境异常时执行。

---

## 调用规范

### calculate_bazi.py

```bash
$PYTHON "$SKILL_DIR/calculate_bazi.py" '<JSON参数>'
```

参数字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `calendar_type` | string | ✅ | `"gregorian"` 公历 / `"lunar"` 农历 |
| `year` | int | ✅ | 出生年份 |
| `month` | int | ✅ | 出生月份 1-12 |
| `day` | int | ✅ | 出生日 1-31 |
| `hour` | int | ✅ | 出生小时 0-23（当地时间） |
| `minute` | int | ✅ | 出生分钟 0-59，用于真太阳时校正 |
| `gender` | string | ✅ | `"M"` 男 / `"F"` 女 |
| `birth_place` | string | ✅ | 出生城市，如 `"四川成都"` |
| `is_leap_month` | bool | ❌ | 农历闰月时为 true，默认 false |

示例：
```bash
$PYTHON "$SKILL_DIR/calculate_bazi.py" '{"calendar_type":"gregorian","year":1990,"month":7,"day":15,"hour":14,"minute":30,"gender":"M","birth_place":"四川成都"}'
```

### store_bazi.py

```bash
# 保存
$PYTHON "$SKILL_DIR/store_bazi.py" save --name "张三" --slug "zhangsan" --data '<JSON>' --memo "备注"

# 读取
$PYTHON "$SKILL_DIR/store_bazi.py" load --slug "zhangsan"

# 列出所有
$PYTHON "$SKILL_DIR/store_bazi.py" list

# 删除
$PYTHON "$SKILL_DIR/store_bazi.py" delete --slug "zhangsan"
```

slug 是唯一标识符，建议用拼音，不含空格。

---

## 参数收集规则

调用 `calculate_bazi.py` 前必须收集齐所有必填参数。

必须追问的情况：
- 未区分公历/农历 → 明确询问
- 未提供出生时分 → "需要精确时分用于真太阳时校正，请告知出生的具体时间"
- 未提供出生城市 → "需要出生城市用于经度校正"
- 农历且月份可能是闰月 → 询问是否为闰月

边界处理：
- 用户说"午时"而非具体时分 → 默认午时中点 12:00，告知用户
- 用户不知道出生时间 → 告知无法排时柱，可仅排年月日，hour=0 minute=0，询问是否继续

---

## 存储触发规则

以下情况主动询问是否保存命盘：
- 排盘完成后，用户表示"这是我自己的"或提到了某人名字
- 用户说"下次还要用"、"记住这个人"等

保存时询问名字和备注（备注可跳过），slug 由你根据名字自动生成，无需用户输入。

读取时：用户说"帮我看看上次那个 XX 的命盘" → 先执行 `list`，找到对应 slug，再执行 `load`，用已存储数据直接进入解读，无需重新排盘。

---

## 解读规范

### 角色定位

客观的命理哲学咨询师。命理是描述人生特质与发展周期的工具，不做宿命论预测。

### 首次回复结构（严格按序）

1. **命盘确认**：回显四柱和日主，说明真太阳时校正结果
2. **原局特质**：分析日主强弱、核心十神格局、显著刑冲合会，写成 2-3 个自然段
3. **当下聚焦**：严格锚定 `system_context.current_year` 和当前大运，结合流年分析，给出 2-3 句建议
4. **收尾**：一句话告知完整大运已推演，可就任意阶段继续探讨

首次回复控制在 500 字以内，不列出一生所有大运。

### 十神现代解读方向

| 十神 | 解读方向 |
|------|---------|
| 比肩/劫财 | 独立意志、竞争意识、同侪关系 |
| 食神 | 表达欲、生活品质、创造力 |
| 伤官 | 才华外露、反叛性、对规则的挑战 |
| 正财/偏财 | 资源掌控、务实行动力、物质关系 |
| 正官/七杀 | 外部规范与压力、社会角色、执行力 |
| 正印/偏印 | 内省、学习力、庇护与依赖 |


### 后续追问处理

- 问未来某年/阶段 → 从 `da_yun_list` 按 `start_year`/`end_year` 定位，结合流年分析
- 问过去经历 → 回溯对应大运区间，说明周期背景
- 需要修改出生信息 → 重新调用 `calculate_bazi.py`，不手动推算

### 语气基调

平和客观。多用"倾向于"、"这一阶段的能量特征是"、"值得关注的是"，少用"会"、"必定"、"一定"。

---

## 流派约定（固定，不向用户暴露）

- 早晚子时：23:00–23:59 日柱算当天（sect=2）
- 真太阳时：脚本内部按经度自动校正，无需用户操作
- 大运：男阳/女阴顺排，男阴/女阳逆排
