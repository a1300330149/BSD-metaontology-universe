# theory_base 根目录文件批量分类归档脚本
# 将根目录下散落的 .md 文件按分类移动到对应目录

$baseDir = "C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\theory_base"

# 分类规则：模式 -> 目标目录
$categories = @(
    # 00 索引导航类
    @{ Pattern = "total_index"; Target = "00_index_navigation" },
    @{ Pattern = "知识库索引"; Target = "00_index_navigation" },
    @{ Pattern = "首页统一理论说明"; Target = "00_index_navigation" },
    @{ Pattern = "新四位一体3.0元本体本源知识库"; Target = "00_index_navigation" },
    @{ Pattern = "新四位一体3.0所有存档哈希"; Target = "00_index_navigation" },
    @{ Pattern = "全套源码说明"; Target = "00_index_navigation" },
    
    # 01 核心元本体理论分册
    @{ Pattern = "元本体理论分册"; Target = "01_core_ontology" },
    @{ Pattern = "意义大一统V2.0理论分册"; Target = "01_core_ontology" },
    @{ Pattern = "^大一统0元本体论"; Target = "01_core_ontology" },
    @{ Pattern = "^本源结构"; Target = "01_core_ontology" },
    @{ Pattern = "^0元本体论数理与多学科交叉验证"; Target = "01_core_ontology" },
    @{ Pattern = "基于宇宙本体结构的全域完整分层基底体系"; Target = "01_core_ontology" },
    @{ Pattern = "大一统验证理论"; Target = "01_core_ontology" },
    @{ Pattern = "AI验证理论大一统"; Target = "01_core_ontology" },
    @{ Pattern = "大一统理论落地实录"; Target = "01_core_ontology" },
    @{ Pattern = "配套全域数理模型"; Target = "01_core_ontology" },
    @{ Pattern = "第一层1到9模块大一统理论终极不可改基底"; Target = "01_core_ontology" },
    
    # 02 八层全域架构体系
    @{ Pattern = "^第一层1到9模块"; Target = "02_eight_layer_architecture" },
    @{ Pattern = "^第三层：全域稳态补丁"; Target = "02_eight_layer_architecture" },
    @{ Pattern = "^第四层：BSD四层统一场论"; Target = "02_eight_layer_architecture" },
    @{ Pattern = "^第五层全域22模块"; Target = "02_eight_layer_architecture" },
    @{ Pattern = "^第六层·全域文明稳态治理体系 总卷宗"; Target = "02_eight_layer_architecture" },
    @{ Pattern = "^第七层：全域数理工具"; Target = "02_eight_layer_architecture" },
    @{ Pattern = "^第八层：全域总根终审"; Target = "02_eight_layer_architecture" },
    
    # 03 四十卷宗系列
    @{ Pattern = "第一套主干40卷宗"; Target = "03_forty_volumes_series" },
    @{ Pattern = "第二套域外推演40卷宗"; Target = "03_forty_volumes_series" },
    @{ Pattern = "第三套.*元规则终审.*40卷宗"; Target = "03_forty_volumes_series" },
    @{ Pattern = "数理验证卷宗"; Target = "03_forty_volumes_series" },
    @{ Pattern = "多学科交叉验证卷宗"; Target = "03_forty_volumes_series" },
    
    # 04 文明治理
    @{ Pattern = "全域规范性伦理完整理论体系"; Target = "04_civilization_governance" },
    @{ Pattern = "全域文明法典"; Target = "04_civilization_governance" },
    @{ Pattern = "模块22：全域文明风控监测"; Target = "04_civilization_governance" },
    @{ Pattern = "模块23：全域文明运维中枢"; Target = "04_civilization_governance" },
    @{ Pattern = "模块24：全域文明稳态治理核心"; Target = "04_civilization_governance" },
    @{ Pattern = "模块25：全域文明法典"; Target = "04_civilization_governance" },
    @{ Pattern = "三态同源统摄与全域学科演化闭环"; Target = "04_civilization_governance" },
    @{ Pattern = "全域文明稳态治理体系.*主干40卷宗"; Target = "03_forty_volumes_series" },
    
    # 05 科研工程落地
    @{ Pattern = "科研闭环公理体系"; Target = "05_research_engineering" },
    @{ Pattern = "六阶自主科研架构论文"; Target = "05_research_engineering" },
    @{ Pattern = "七大公理专项论文"; Target = "05_research_engineering" },
    @{ Pattern = "通用科研系统"; Target = "05_research_engineering" },
    @{ Pattern = "AFAC工程落地分册"; Target = "05_research_engineering" },
    @{ Pattern = "第1、2重基底专项适配赛题"; Target = "05_research_engineering" },
    @{ Pattern = "阶段0.*元本体核心引擎.*OCE"; Target = "05_research_engineering" },
    @{ Pattern = "一阶实体拟合系统"; Target = "05_research_engineering" },
    @{ Pattern = "二阶分布纠偏系统"; Target = "05_research_engineering" },
    @{ Pattern = "三阶智能决策系统"; Target = "05_research_engineering" },
    @{ Pattern = "四阶跨域泛化系统"; Target = "05_research_engineering" },
    @{ Pattern = "五阶科研成果产出系统"; Target = "05_research_engineering" },
    @{ Pattern = "六阶自主科研闭环系统"; Target = "05_research_engineering" },
    @{ Pattern = "智能体AI集群实现大一统"; Target = "05_research_engineering" },
    @{ Pattern = "四阶跨域泛化系统"; Target = "05_research_engineering" },
    
    # 06 虚拟宇宙创世
    @{ Pattern = "虚拟宇宙学科创世模型"; Target = "06_virtual_creation" },
    @{ Pattern = "虚拟宇宙学AI游戏小说文学通用基底公理"; Target = "06_virtual_creation" },
    @{ Pattern = "全域架空体系AI虚拟创世系统"; Target = "06_virtual_creation" },
    @{ Pattern = "六系六维创世动力学"; Target = "06_virtual_creation" },
    @{ Pattern = "六系六维宇宙统一创世动力学"; Target = "06_virtual_creation" },
    
    # 07 学术论文与意识形态
    @{ Pattern = "实践哲学视域下"; Target = "07_academic_papers" },
    @{ Pattern = "全域元本体视角下马克思主义"; Target = "07_academic_papers" },
    @{ Pattern = "新时代具有强大凝聚力"; Target = "07_academic_papers" },
    @{ Pattern = "全方位推翻广义存在论"; Target = "07_academic_papers" },
    @{ Pattern = "五组核心议题系统论证局限"; Target = "07_academic_papers" },
    
    # 08 实验归档与代码base
    @{ Pattern = "^experiment_"; Target = "08_experiment_archive" },
    @{ Pattern = "^code_base_"; Target = "08_experiment_archive" }
)

# 获取根目录所有 .md 文件
$files = Get-ChildItem -Path $baseDir -Filter "*.md" -File

Write-Host "根目录待归档文件数: $($files.Count)"
Write-Host ""

$moved = 0
$unmatched = @()

foreach ($file in $files) {
    $targetDir = $null
    $fileName = $file.Name
    
    foreach ($cat in $categories) {
        if ($fileName -match $cat.Pattern) {
            $targetDir = $cat.Target
            break
        }
    }
    
    if ($targetDir) {
        $destPath = Join-Path $baseDir "$targetDir\$fileName"
        Move-Item -Path $file.FullName -Destination $destPath -Force
        Write-Host "  [$targetDir] $fileName"
        $moved++
    } else {
        $unmatched += $fileName
    }
}

Write-Host ""
Write-Host "=== 归档完成 ==="
Write-Host "已移动: $moved 个文件"
Write-Host "未匹配: $($unmatched.Count) 个文件"

if ($unmatched.Count -gt 0) {
    Write-Host ""
    Write-Host "未匹配文件列表:"
    foreach ($f in $unmatched) {
        Write-Host "  - $f"
    }
}
