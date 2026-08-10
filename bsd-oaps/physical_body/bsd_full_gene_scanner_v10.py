"""
BSD全量基因扫描器 V10.0
========================
保存全部69,882个基因的完整数据
用于生成全量基因配置
"""

import os
import json
import time
import platform
from datetime import datetime
from collections import defaultdict


# ============================================================================
# 第一部分：扫描配置（简化版，专注基因收集）
# ============================================================================

SCAN_CONFIG = {
    "target_drives": ["C:\\", "D:\\"],
    "max_depth": 5,
    "skip_dirs": [
        "C:\\Windows", "C:\\Users", "C:\\ProgramData",
        "C:\\$Recycle.Bin", "C:\\System Volume Information",
        "D:\\$RECYCLE.BIN", "D:\\System Volume Information",
    ],
    "priority_dirs": [
        "Program Files", "Program Files (x86)", 
        "Users", "Desktop", "Downloads",
        "Documents", "OneDrive",
        "TRAE SOLO CN",
    ],
    "file_extensions": [
        ".exe", ".dll", ".json", ".xml", ".config",
        ".ini", ".dat", ".db", ".md", ".txt",
        ".py", ".js", ".ts", ".html", ".css",
    ],
}


# ============================================================================
# 第二部分：六系分类器（简化版）
# ============================================================================

SYSTEM_CLASSIFIER = {
    "强化系": {
        "icon": "🔵",
        "axiom": "纯·个体性公理",
        "keywords": ["security", "defender", "antivirus", "protection", "firewall",
                     "backup", "recovery", "storage", "disk", "core",
                     "system", "foundation", "base", "platform",
                     "partition", "aomei", "partassistant", "partitionassistant",
                     "intel", "chipset", "motherboard", "安全", "防护", "存储"],
        "weight": 1.0,
    },
    "变身系": {
        "icon": "⚫",
        "axiom": "纯·变化性公理",
        "keywords": ["compiler", "interpreter", "runtime", "engine",
                     "animation", "media", "audio", "video", "graphics",
                     "editor", "ide", "debugger", "transform", "convert",
                     "sdk", "framework", "library",
                     "blender", "3d", "modeling", "rendering",
                     "darkest", "dungeon", "game", "stateofdecay",
                     "cloudmusic", "music", "sound",
                     "game", "gaming", "steam", "valve",
                     "ggbh", "mod", "modding",
                     "编译", "解释", "运行", "引擎", "游戏"],
        "weight": 0.9,
    },
    "社会系": {
        "icon": "🟢",
        "axiom": "纯·关系性公理",
        "keywords": ["network", "networking", "communication", "chat", "message",
                     "collaboration", "share", "sync", "protocol", "socket",
                     "server", "client", "api", "web", "cloud",
                     "browser", "email", "instant",
                     "wechat", "weixin", "wx", "qq", "wangwang",
                     "mail", "email", "outlook", "mailmaster",
                     "wps", "office", "document", "spreadsheet",
                     "thunder", "download", "xunlei",
                     "baidunetdisk", "baidunetdiskdownload", "baidusyncdisk",
                     "douyin", "tiktok", "抖音",
                     "network", "internet", "social",
                     "cloudmusic", "netease", "kugou",
                     "kimi", "kimidata",
                     "网络", "通信", "协作"],
        "weight": 0.8,
    },
    "天道系": {
        "icon": "🟣",
        "axiom": "关系性×变化性",
        "keywords": ["ai", "machinelearning", "deeplearning", "neural",
                     "ruleengine", "workflow", "automation", "bot", "agent",
                     "framework", "package", "module", "plugin",
                     "rules", "policy", "governance", "management",
                     "trae", "solo", "cn", "code", "coding",
                     "programming", "development", "ide",
                     "ai", "llm", "gpt", "model",
                     "intellij", "pycharm", "vscode",
                     "visual", "studio",
                     "智能", "学习", "规则", "工作流", "自动化",
                     "编程", "开发", "代码"],
        "weight": 1.2,
    },
    "自然系": {
        "icon": "🟠",
        "axiom": "变化性×个体性",
        "keywords": ["database", "sql", "nosql", "data", "file",
                     "filesystem", "physical", "simulation", "physics",
                     "compute", "gpu", "cpu", "processor",
                     "driver", "hardware", "device",
                     "datastore", "storage", "archive",
                     "map", "navigation", "gis",
                     "miktex", "latex", "tex",
                     "perfmon", "perf", "log",
                     "database", "db", "data",
                     "数据库", "物理", "模拟", "计算", "驱动",
                     "地图", "存储", "日志", "排版"],
        "weight": 1.1,
    },
    "具现系": {
        "icon": "🔴",
        "axiom": "个体性×关系性",
        "keywords": ["ui", "userinterface", "gui", "display", "render",
                     "theme", "style", "visual", "graphic", "design",
                     "layout", "component", "widget", "control",
                     "desktop", "window", "panel",
                     "界面", "显示", "渲染", "主题", "设计"],
        "weight": 0.85,
    },
}


# ============================================================================
# 第三部分：全量扫描器
# ============================================================================

class FullDiskScannerV10:
    """全量基因扫描器 V10.0 - 保存所有基因数据"""
    
    def __init__(self):
        self.scan_start_time = datetime.now().isoformat()
        self.all_genes = []  # 保存所有基因
        self.gene_id_counter = 0
        self.stats = {
            "total_dirs": 0,
            "total_files": 0,
            "total_size": 0,
            "by_drive": {"C:": {"dirs": 0, "files": 0, "size": 0}, 
                         "D:": {"dirs": 0, "files": 0, "size": 0}},
            "by_system": defaultdict(list),
        }
    
    def scan_all(self) -> dict:
        """扫描所有盘"""
        print("=" * 80)
        print("【BSD全量基因扫描器 V10.0】")
        print("保存全部基因数据，用于全量配置生成")
        print("=" * 80)
        
        for drive in SCAN_CONFIG["target_drives"]:
            if os.path.exists(drive):
                print(f"\n📁 扫描 {drive}")
                self._scan_drive(drive)
        
        # 生成报告
        return self._generate_report()
    
    def _scan_drive(self, drive_path: str):
        """扫描单个盘"""
        drive_key = drive_path[0] + ":"
        
        # 扫描优先目录
        for priority_dir in SCAN_CONFIG["priority_dirs"]:
            full_path = os.path.join(drive_path, priority_dir)
            if os.path.exists(full_path):
                self._scan_directory(full_path, drive_key, depth=0)
        
        # 扫描根目录
        try:
            root_items = os.listdir(drive_path)
            for item in root_items:
                item_path = os.path.join(drive_path, item)
                
                skip = False
                for skip_dir in SCAN_CONFIG["skip_dirs"]:
                    if item_path.startswith(skip_dir):
                        skip = True
                        break
                
                if skip:
                    continue
                
                if os.path.isdir(item_path):
                    self._scan_directory(item_path, drive_key, depth=0)
        except PermissionError:
            pass
    
    def _scan_directory(self, dir_path: str, drive_key: str, depth: int):
        """递归扫描目录"""
        if depth > SCAN_CONFIG["max_depth"]:
            return
        
        try:
            items = os.listdir(dir_path)
        except PermissionError:
            return
        except Exception:
            return
        
        for item in items:
            item_path = os.path.join(dir_path, item)
            
            try:
                if os.path.isdir(item_path):
                    self._identify_and_collect(item, item_path, drive_key, depth)
                    self._scan_directory(item_path, drive_key, depth + 1)
                elif os.path.isfile(item_path):
                    ext = os.path.splitext(item)[1].lower()
                    if ext in SCAN_CONFIG["file_extensions"]:
                        self._scan_file(item_path, drive_key)
            except (PermissionError, OSError):
                continue
    
    def _identify_and_collect(self, name: str, path: str, drive_key: str, depth: int = 0):
        """识别并收集目录为基因"""
        classification = self._classify_by_name(name, path)
        
        try:
            dir_size = self._calculate_dir_size(path)
        except:
            dir_size = 0
        
        self.gene_id_counter += 1
        gene_id = f"FULL-V10-{self.gene_id_counter:06d}"
        
        primary_system = classification["systems"][0] if classification["systems"] else "未分类"
        
        gene = {
            "gene_id": gene_id,
            "name": name,
            "path": path,
            "drive": drive_key,
            "six_system": primary_system,
            "all_systems": classification["systems"],
            "confidence": classification["confidence"],
            "category": classification["category"],
            "size_bytes": dir_size,
            "type": "directory",
            "depth": depth,
        }
        
        self.all_genes.append(gene)
        self.stats["total_dirs"] += 1
        self.stats["by_drive"][drive_key]["dirs"] += 1
        self.stats["by_drive"][drive_key]["size"] += dir_size
        self.stats["by_system"][primary_system].append(gene)
    
    def _classify_by_name(self, name: str, path: str) -> dict:
        """根据名称和路径分类"""
        combined = (name + " " + path).lower()
        
        system_scores = {}
        for system_name, classifier in SYSTEM_CLASSIFIER.items():
            score = 0
            for keyword in classifier["keywords"]:
                if keyword.lower() in combined:
                    score += 1
            weighted_score = score * classifier["weight"]
            if weighted_score > 0:
                system_scores[system_name] = weighted_score
        
        if not system_scores:
            return {"systems": ["未分类"], "category": "未分类", "confidence": 0.1}
        
        sorted_systems = sorted(system_scores.items(), key=lambda x: x[1], reverse=True)
        primary_system = sorted_systems[0][0]
        primary_score = sorted_systems[0][1]
        
        multi_systems = [primary_system]
        for system, score in sorted_systems[1:]:
            if score >= primary_score * 0.5:
                multi_systems.append(system)
        
        confidence = min(primary_score / 5.0, 1.0)
        
        return {
            "systems": multi_systems,
            "category": SYSTEM_CLASSIFIER[primary_system]["axiom"],
            "confidence": round(confidence, 2),
        }
    
    def _calculate_dir_size(self, path: str) -> int:
        """计算目录大小"""
        total_size = 0
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    try:
                        total_size += os.path.getsize(os.path.join(root, file))
                    except (PermissionError, OSError):
                        continue
        except (PermissionError, OSError):
            pass
        return total_size
    
    def _scan_file(self, file_path: str, drive_key: str):
        """扫描文件"""
        try:
            file_size = os.path.getsize(file_path)
            filename = os.path.basename(file_path)
            
            self.stats["total_files"] += 1
            self.stats["by_drive"][drive_key]["files"] += 1
            self.stats["total_size"] += file_size
        except (PermissionError, OSError):
            pass
    
    def _generate_report(self) -> dict:
        """生成报告"""
        by_system = {}
        for sys_name in SYSTEM_CLASSIFIER:
            genes = self.stats["by_system"].get(sys_name, [])
            by_system[sys_name] = {
                "icon": SYSTEM_CLASSIFIER[sys_name]["icon"],
                "axiom": SYSTEM_CLASSIFIER[sys_name]["axiom"],
                "count": len(genes),
                "total_size_gb": round(sum(g["size_bytes"] for g in genes) / (1024**3), 2),
                "genes": genes,  # 保存所有基因！
            }
        
        # 未分类
        unclassified_genes = self.stats["by_system"].get("未分类", [])
        by_system["未分类"] = {
            "icon": "❓",
            "axiom": "待识别",
            "count": len(unclassified_genes),
            "total_size_gb": round(sum(g["size_bytes"] for g in unclassified_genes) / (1024**3), 2),
            "genes": unclassified_genes,
        }
        
        return {
            "scan_start_time": self.scan_start_time,
            "scan_end_time": datetime.now().isoformat(),
            "total_genes": len(self.all_genes),
            "total_dirs_scanned": self.stats["total_dirs"],
            "total_files_scanned": self.stats["total_files"],
            "total_size_gb": round(self.stats["total_size"] / (1024**3), 2),
            "by_drive": {
                drive: {
                    "dirs": stats["dirs"],
                    "files": stats["files"],
                    "size_gb": round(stats["size"] / (1024**3), 2),
                }
                for drive, stats in self.stats["by_drive"].items()
            },
            "by_system": by_system,
            "unclassified_count": len(unclassified_genes),
            "platform_info": {
                "system": os.name,
                "platform": platform.platform(),
            },
            "status": "✅ 全量基因扫描完成（V10.0保存所有基因）",
        }


# ============================================================================
# 第四部分：主程序
# ============================================================================

def main():
    agent_path = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2"
    
    # 执行扫描
    scanner = FullDiskScannerV10()
    report = scanner.scan_all()
    
    # 保存报告（包含全部基因数据）
    print("\n💾 保存全量基因报告...")
    report_file = os.path.join(agent_path, "bsd_full_gene_report_V10.0.json")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"  ✅ 报告已保存: {report_file}")
    print(f"     总基因数: {report['total_genes']}")
    
    # 各系基因数
    print("\n📊 六系基因分布：")
    for sys_name, sys_info in report['by_system'].items():
        print(f"  {sys_name} {sys_info['icon']}: {sys_info['count']} 个基因")


if __name__ == "__main__":
    main()
