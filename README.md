# unified-diff-apply

把统一 diff 应用到原文上，产出结果文本。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m patchkit apply --source a.txt --patch a.diff
python3 -m patchkit --sample=context|offset|len|work
```

## 口径

- **hunk 头**：`@@ -旧起点,旧长度 +新起点,新长度 @@`，两个长度都要读；实际给的行数与旧长度不符就是冲突。
- **上下文**：以空格开头的行必须与原文逐字一致，不一致报 `conflict`。
- **行号**：hunk 的旧行号都相对原始文件；前一个 hunk 增删过的行数要累计到后面 hunk 的落点上。
- **行为**：`-` 行删掉，`+` 行插入，` ` 行原样保留。

## 不变量

- 没有冲突时，结果的上下文行与原文一致。
- 多个 hunk 依次应用的结果与逐个单独应用一致。
- `scanned` 不随 hunk 数乘文件行数放大：一千个 hunk 的 `scanned` 不超过 9000。

## 输出契约

`apply` 打印结果文本；冲突时打印 `conflict: <原因>`。
`--sample=work` 只打印 `{"hunks": N, "scanned": N}`。
