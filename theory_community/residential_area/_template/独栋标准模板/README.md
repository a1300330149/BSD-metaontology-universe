# 独栋标准模板说明

**模板路径**：`residential_area/_template/独栋标准模板/`

---

## 模板用途

新建子系统时，直接复制本模板目录，修改以下文件：

1. `facade.json` - 修改subsystem_name、belong_district
2. `living_room.md` - 填写核心定位与职责范围
3. `sub_index.md` - 更新子系统信息
4. `power_record.log` - 初始化算力记录

---

## 模板文件清单

| 文件 | 功能 | 必须修改 |
|------|------|---------|
| facade.json | 外墙边界配置 | ✓ |
| pipeline_config.json | 入户管线配置 | 可选 |
| living_room.md | 主功能区说明 | ✓ |
| sub_index.md | 内部索引 | ✓ |
| power_record.log | 分户电表记录 | 自动 |
| theories/ | 专属理论库 | 自动创建 |
| agents/ | 专属子智能体 | 自动创建 |

---

## 使用步骤

```
1. 复制模板目录到目标小区
2. 重命名目录为新子系统名称
3. 修改facade.json中的subsystem_name
4. 修改living_room.md中的核心定位
5. 更新sub_index.md
6. 开始推演
```

---

**—— 独栋标准模板说明 ——**