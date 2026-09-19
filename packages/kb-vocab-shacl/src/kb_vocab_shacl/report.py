"""Human-readable inventory; absence is not a validation failure."""


def markdown(result: dict) -> str:
    lines = ["# 词表字段统计 (Vocabulary Field Inventory)", "",
             "只统计字段是否出现，不检查内容、类型和数量是否符合设计。空字符串算字段已出现，并另计空值。",
             "对象可属于多个资源类型，各组不能相加作为去重总数。", ""]
    if "run" in result:
        run = result["run"]
        lines += [f"输入：`{run['input']}`；读取与统计耗时：{run['elapsed_seconds']:.3f} 秒。", ""]
    lines += ["## 资源数量", "", "| 对象 | 数量 | 状态 |", "|---|---:|---|"]
    states = {"counted": "已统计", "no_objects": "对象不存在", "scope_required": "需指定对象范围"}
    for resource in result["resources"]:
        lines.append(f"| {resource['label']} | {resource['objects'] if resource['objects'] is not None else '—'} | {states[resource['status']]} |")
    lines += ["", f"未归类主体：{len(result['unclassified_subjects'])} 个；未声明 rdf:type 的主体：{len(result['untyped_subjects'])} 个。两项可能重叠，标识清单见 JSON。", ""]
    for resource in result["resources"]:
        lines += [f"## {resource['label']}字段", ""]
        if resource["status"] != "counted":
            lines += [states[resource["status"]] + "；字段仍列出，不能解释为字段已齐全。", ""]
        lines += ["| 字段 | 有字段 | 无字段 | 空值数 |", "|---|---:|---:|---:|"]
        for row in resource["fields"]:
            cells = ["—" if row[k] is None else f"{row[k]:,}" for k in ("present", "absent", "empty_values")]
            lines.append(f"| `{row['name']}` | " + " | ".join(cells) + " |")
    lines += ["", "## 全图字段", "", "包括辅助资源；有字段的主体数不同于该字段的值数量。", "",
              "| 字段 | 有字段的主体数 | 陈述数 |", "|---|---:|---:|"]
    for row in result["fields"]:
        lines.append(f"| `{row['name']}` | {row['present_subjects']:,} | {row['statements']:,} |")
    lines += ["", "## 条件规则", "",
              "以下规则只在明确的对象范围内适用。已指定范围也不代表本次执行了校验；inventory 只统计字段。", "",
              "| 条件要求 | 关联对象 | 范围状态 | 指定对象数 | 本次执行 |",
              "|---|---|---|---:|---|"]
    scope_states = {"unspecified": "未指定", "specified": "已指定", "deactivated": "规则已停用"}
    resource_labels = {r["type"]: r["label"] for r in result["resources"]}
    for condition in result["conditions"]:
        count = condition["selected_objects"]
        labels = "、".join(resource_labels[t] for t in condition["resource_types"])
        lines.append(f"| {condition['name']} | {labels} | {scope_states[condition['scope_status']]} | {count if count is not None else '—'} | 未执行校验 |")
    lines += ["", "## 统计边界", "",
              "可选字段缺省也计入无字段，不判为错误。独立说明没有通用类型，未提供对象范围时不推断其数量。",
              "名称登记、翻译任务、采纳及版本等配套管理记录不由本次 TTL 统计判断，不能将未统计写成缺失或已满足。",
              "设计中的适用条件及各字段对应的 Shape 保存在 JSON；统计没有执行 SHACL 校验。", ""]
    return "\n".join(lines)
