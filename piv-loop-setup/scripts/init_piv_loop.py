#!/usr/bin/env python3
"""
PIV Loop 工作流配置脚本

自动检测项目类型，生成 Claude Commands 配置。
"""

import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class PackageManager(Enum):
    UV = "uv"
    NPM = "npm"
    PNPM = "pnpm"
    YARN = "yarn"
    MAVEN = "maven"
    GRADLE = "gradle"
    CARGO = "cargo"


class TestFramework(Enum):
    PYTEST = "pytest"
    VITEST = "vitest"
    JEST = "jest"
    UNittest = "unittest"
    GO_TEST = "go test"


class Linter(Enum):
    RUFF = "ruff"
    ESLINT = "eslint"
    PRETTIER = "prettier"
    BLACK = "black"
    FLAKE8 = "flake8"


@dataclass
class ProjectConfig:
    """项目配置"""
    name: str
    package_manager: PackageManager
    test_framework: TestFramework
    linter: Linter
    language: str
    framework: Optional[str]
    commands: list[str]
    skip_reference: list[str]


class ProjectDetector:
    """项目类型检测器"""

    def __init__(self, project_root: Path):
        self.root = project_root
        self.files = self._list_files()

    def _list_files(self) -> set:
        """列出所有文件（不含 .git）"""
        files = set()
        for p in self.root.rglob("*"):
            if p.is_file() and ".git" not in p.parts:
                files.add(p.relative_to(self.root))
        return files

    def detect_package_manager(self) -> PackageManager:
        """检测包管理器"""
        indicators = {
            "uv.lock": PackageManager.UV,
            "package-lock.json": PackageManager.NPM,
            "pnpm-lock.yaml": PackageManager.PNPM,
            "yarn.lock": PackageManager.YARN,
            "pom.xml": PackageManager.MAVEN,
            "build.gradle": PackageManager.GRADLE,
            "Cargo.lock": PackageManager.CARGO,
        }
        for filename, pm in indicators.items():
            if any(f.name == filename for f in self.files):
                return pm
        return PackageManager.NPM  # 默认

    def detect_test_framework(self) -> TestFramework:
        """检测测试框架"""
        indicators = [
            (r"pytest\.ini|conftest\.py|pyproject\.toml", TestFramework.PYTEST),
            (r"vitest\.config\.|@vitest/", TestFramework.VITEST),
            (r"jest\.config\.|__tests__", TestFramework.JEST),
            (r"unittest\.py|test_.*\.py", TestFramework.unittest),
        ]
        for pattern, framework in indicators:
            if any(re.search(pattern, str(f)) for f in self.files):
                return framework
        return TestFramework.PYTEST  # 默认

    def detect_linter(self) -> Linter:
        """检测代码检查工具"""
        indicators = {
            "ruff.toml": Linter.RUFF,
            ".eslintrc": Linter.ESLINT,
            ".prettierrc": Linter.PRETTIER,
            "pyproject.toml": Linter.BLACK,  # 假设 Python
            ".flake8": Linter.FLAKE8,
        }
        for filename, linter in indicators.items():
            if any(f.name == filename for f in self.files):
                return linter
        return Linter.RUFF  # 默认

    def detect_language_and_framework(self) -> tuple[str, Optional[str]]:
        """检测语言和框架"""
        indicators = [
            # Python
            (r"pyproject\.toml|setup\.py", "python", "fastapi"),
            (r"requirements\.txt", "python", "flask"),
            # JavaScript/TypeScript
            (r"package\.json", "typescript", "react"),
            (r"tsconfig\.json", "typescript", None),
            # Java
            (r"pom\.xml|build\.gradle", "java", "spring"),
            # Go
            (r"go\.mod", "go", None),
            # Rust
            (r"Cargo\.toml", "rust", None),
        ]
        for pattern, lang, framework in indicators:
            if any(re.search(pattern, str(f)) for f in self.files):
                return lang, framework
        return "typescript", None  # 默认

    def detect(self) -> ProjectConfig:
        """执行完整检测"""
        return ProjectConfig(
            name=self.root.name,
            package_manager=self.detect_package_manager(),
            test_framework=self.detect_test_framework(),
            linter=self.detect_linter(),
            language=self.detect_language_and_framework()[0],
            framework=self.detect_language_and_framework()[1],
            commands=["core_piv_loop", "validation", "github_bug_fix", "commit"],
            skip_reference=[],
        )


class ConfigGenerator:
    """配置生成器"""

    # 模板替换映射
    REPLACEMENTS = {
        "pytest": {
            "test_command": "pytest -v",
            "test_coverage": "pytest --cov=app",
            "lint_command": "ruff check .",
            "format_command": "ruff format .",
        },
        "vitest": {
            "test_command": "vitest run",
            "test_coverage": "vitest run --coverage",
            "lint_command": "eslint .",
            "format_command": "prettier --write .",
        },
        "jest": {
            "test_command": "jest",
            "test_coverage": "jest --coverage",
            "lint_command": "eslint .",
            "format_command": "prettier --write .",
        },
    }

    PM_COMMANDS = {
        "uv": {
            "install": "uv sync",
            "run": "uv run",
            "dev_install": "uv pip install -e .",
        },
        "npm": {
            "install": "npm install",
            "run": "npm run",
            "dev_install": "npm install -D",
        },
        "pnpm": {
            "install": "pnpm install",
            "run": "pnpm",
            "dev_install": "pnpm add -D",
        },
        "yarn": {
            "install": "yarn install",
            "run": "yarn",
            "dev_install": "yarn add -D",
        },
    }

    def __init__(self, skill_path: Path, project_path: Path):
        self.skill_path = skill_path
        self.project_path = project_path
        self.templates_path = self.skill_path / "templates"

    def generate(self, config: ProjectConfig, override: Optional[dict] = None) -> None:
        """生成所有配置文件"""
        # 合并覆盖配置
        if override:
            config = self._merge_config(config, override)

        # 创建目录结构
        self._create_directories()

        # 复制并替换命令模板
        self._generate_commands(config)

        # 复制参考文档
        self._generate_references(config)

        # 生成 .agents/README.md
        self._generate_agents_readme(config)

        # 更新 CLAUDE.md
        self._update_claude_md(config)

        print(f"✓ PIV Loop 工作流已配置完成")
        print(f"  项目: {config.name}")
        print(f"  语言: {config.language}")
        print(f"  包管理器: {config.package_manager.value}")
        print(f"  测试框架: {config.test_framework.value}")
        print(f"  Linter: {config.linter.value}")

    def _merge_config(self, base: ProjectConfig, override: dict) -> ProjectConfig:
        """合并覆盖配置"""
        return ProjectConfig(
            name=override.get("name", base.name),
            package_manager=PackageManager(override.get("package_manager", base.package_manager.value)),
            test_framework=TestFramework(override.get("test_framework", base.test_framework.value)),
            linter=Linter(override.get("linter", base.linter.value)),
            language=override.get("language", base.language),
            framework=override.get("framework", base.framework),
            commands=override.get("commands", base.commands),
            skip_reference=override.get("skip_reference", base.skip_reference),
        )

    def _create_directories(self) -> None:
        """创建目录结构"""
        dirs = [
            ".claude/commands/core_piv_loop",
            ".claude/commands/validation",
            ".claude/commands/github_bug_fix",
            ".claude/commands/other",
            ".claude/reference",
            ".agents/plans",
            ".agents/code-reviews",
            ".agents/system-reviews",
        ]
        for d in dirs:
            (self.project_path / d).mkdir(parents=True, exist_ok=True)

    def _get_replacements(self, config: ProjectConfig) -> dict:
        """获取模板替换值"""
        # 测试框架替换
        tf = config.test_framework.value
        framework_replacements = self.REPLACEMENTS.get(tf, self.REPLACEMENTS["pytest"])

        # 包管理器替换
        pm = config.package_manager.value
        pm_commands = self.PM_COMMANDS.get(pm, self.PM_COMMANDS["npm"])

        return {
            **framework_replacements,
            **pm_commands,
            "language": config.language,
            "framework": config.framework or "",
            "project_name": config.name,
        }

    def _generate_commands(self, config: ProjectConfig) -> None:
        """生成命令文件"""
        templates_dir = self.skill_path / "templates" / "commands"
        replacements = self._get_replacements(config)

        if "core_piv_loop" in config.commands:
            self._process_template(templates_dir / "core_piv_loop", ".claude/commands/core_piv_loop", replacements)

        if "validation" in config.commands:
            self._process_template(templates_dir / "validation", ".claude/commands/validation", replacements)

        if "github_bug_fix" in config.commands:
            self._process_template(templates_dir / "github_bug_fix", ".claude/commands/github_bug_fix", replacements)

        # commit 命令
        self._copy_template(templates_dir / "commit.md", ".claude/commands/commit.md")

        # init-project 命令
        self._process_template(templates_dir / "init-project.md", ".claude/commands/init-project.md", replacements)

        # create-prd 命令
        self._copy_template(templates_dir / "create-prd.md", ".claude/commands/create-prd.md")

    def _generate_references(self, config: ProjectConfig) -> None:
        """生成参考文档"""
        templates_dir = self.skill_path / "templates" / "reference"
        lang = config.language

        # 根据语言选择参考文档
        ref_map = {
            "python": ["fastapi-best-practices.md", "sqlite-best-practices.md", "testing-and-logging.md"],
            "typescript": ["react-frontend-best-practices.md", "testing-and-logging.md"],
            "java": ["testing-and-logging.md"],
            "go": ["testing-and-logging.md"],
        }

        refs = ref_map.get(lang, ["testing-and-logging.md"])

        for ref in refs:
            if ref not in config.skip_reference:
                self._copy_template(templates_dir / ref, f".claude/reference/{ref}")

        # 部署最佳实践（通用）
        if "deployment-best-practices.md" not in config.skip_reference:
            self._copy_template(templates_dir / "deployment-best-practices.md", ".claude/reference/deployment-best-practices.md")

    def _generate_agents_readme(self, config: ProjectConfig) -> None:
        """生成 .agents/README.md"""
        template = self.skill_path / "assets" / "agents-readme-template.md"
        if template.exists():
            content = template.read_text()
            content = content.replace("{{project_name}}", config.name)
            content = content.replace("{{language}}", config.language)
            content = content.replace("{{test_framework}}", config.test_framework.value)
            content = content.replace("{{package_manager}}", config.package_manager.value)
            (self.project_path / ".agents" / "README.md").write_text(content)

    def _update_claude_md(self, config: ProjectConfig) -> None:
        """更新 CLAUDE.md"""
        claude_md = self.project_path / "CLAUDE.md"
        if claude_md.exists():
            content = claude_md.read_text()
        else:
            content = f"# {config.name}\n\n"

        # 添加 PIV Loop 工作流说明
        piv_section = """

## PIV Loop 工作流

本项目使用 PIV Loop AI 开发流程：

| 命令 | 描述 |
|------|------|
| `/core_piv_loop:prime` | 理解项目结构 |
| `/core_piv_loop:plan-feature` | 创建实施计划 |
| `/core_piv_loop:execute` | 执行计划 |
| `/validation:validate` | 运行验证 |
| `/commit` | 创建提交 |

详细说明见 [.agents/README.md](.agents/README.md)
"""
        if "## PIV Loop 工作流" not in content:
            content += piv_section
            claude_md.write_text(content)

    def _process_template(self, src_dir: Path, dst_dir: Path, replacements: dict) -> None:
        """处理模板目录"""
        if not src_dir.exists():
            return
        for src in src_dir.rglob("*.md"):
            rel = src.relative_to(src_dir)
            dst = dst_dir / rel
            self._process_file(src, dst, replacements)

    def _process_file(self, src: Path, dst: Path, replacements: dict) -> None:
        """处理单个模板文件"""
        content = src.read_text()
        for key, value in replacements.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(content)

    def _copy_template(self, src: Path, dst: Path) -> None:
        """复制模板文件"""
        if src.exists():
            shutil.copy2(src, dst)


def main():
    """主入口"""
    # 查找 skill 根目录
    skill_path = Path(__file__).parent.parent

    # 解析参数
    project_path = Path.cwd()
    debug = "--debug" in sys.argv

    # 查找覆盖配置
    config_file = project_path / "piv-config.json"
    override = None
    if config_file.exists():
        with open(config_file) as f:
            override = json.load(f)
        if debug:
            print(f"使用覆盖配置: {override}")

    # 检测项目类型
    detector = ProjectDetector(project_path)
    config = detector.detect()

    if debug:
        print(f"检测到的配置:")
        print(f"  语言: {config.language}")
        print(f"  包管理器: {config.package_manager}")
        print(f"  测试框架: {config.test_framework}")
        print(f"  Linter: {config.linter}")

    # 生成配置
    generator = ConfigGenerator(skill_path, project_path)
    generator.generate(config, override)


if __name__ == "__main__":
    main()
