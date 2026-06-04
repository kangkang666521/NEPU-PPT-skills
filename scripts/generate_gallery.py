#!/usr/bin/env python3
"""Generate gallery reference slides using NepuSlideBuilder.

Produces a demo PPTX under assets/gallery/slides/ showing
positive examples of NEPU slide layouts (not just charts).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add parent to path so we can import the builder
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.slide_builder import NepuSlideBuilder  # noqa: E402


def main() -> None:
    out_dir = Path(__file__).resolve().parents[1] / "assets" / "gallery" / "slides"
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / "nepu-layout-reference.pptx"

    # ── petro-blue: academic standard ──
    b = NepuSlideBuilder(theme="petro-blue")

    # Cover
    b.add_cover("碳捕集技术研究进展", subtitle="Recent Advances in Carbon Capture Technology")

    # Section divider
    b.add_section("研究背景与意义")

    # Claim-led slide
    b.add_claim_slide(
        "全球每年排放 CO₂ 超过 360 亿吨，碳捕集是实现碳中和的关键技术路径之一",
        bullets=[
            "2023 年全球大气 CO₂ 浓度突破 420 ppm",
            "现有碳捕集成本 $40-120/ton CO₂",
            "新型固体吸附剂可将成本降低 30%-50%",
        ],
    )

    # Figure-dominant: asymmetric 70/30
    b.add_claim_slide(
        "胺基功能化 MOF 材料在低压下表现优异",
        bullets=["示例画廊不使用虚构或缺失的科研图", "实际任务中应插入可追溯的真实证据图"],
    )

    # Comparison matrix
    b.add_matrix_slide(
        headers=["材料", "吸附量\n(mmol/g)", "再生温度\n(°C)", "循环稳定性", "成本\n($/kg)"],
        rows=[
            ["MOF-74-Mg", "8.2", "120", ">100 cycles", "85"],
            ["Zeolite 13X", "4.1", "200", ">500 cycles", "12"],
            ["PEI/SiO₂", "3.8", "110", "~50 cycles", "45"],
            ["Activated Carbon", "2.5", "80", ">1000 cycles", "3"],
        ],
        title="主流固体吸附材料性能对比",
    )

    # Bullet slides
    b.add_bullet_slide(
        "技术创新点",
        [
            "首次将机器学习用于 MOF 材料高通量筛选",
            "开发了低温再生工艺（<100°C）",
            "建立了中试规模（10 kg/day）连续捕集装置",
            "全生命周期评估显示碳负效益",
        ],
        two_column=True,
    )

    # Conclusion
    b.add_conclusion(
        ["MOF 基碳捕集材料具有规模化应用前景", "低温再生工艺可显著降低运营成本", "下一步将推进工业级中试验证"],
    )

    b.save(output, overwrite=True)
    print(f"Gallery reference PPTX saved to: {output}")

    # ── Clean-white variant for text-heavy academic ──
    b2 = NepuSlideBuilder(theme="clean-white")
    b2.add_cover("文献综述：非常规油气开发中的\n水力压裂技术环境影响", subtitle="Environmental Impact of Hydraulic Fracturing — A Systematic Review")
    b2.add_bullet_slide(
        "主要发现",
        [
            "2000-2024 年发表的 847 篇相关文献中，62% 关注水资源影响",
            "微地震监测是最常用的影响评估手段（占 41%）",
            "45% 的研究来自北美非常规盆地，仅 12% 来自亚洲",
            "缺乏统一的跨区域对比方法论是主要知识缺口",
        ],
    )
    b2.add_matrix_slide(
        headers=["研究区域", "样本量", "主要方法", "关键结论", "置信度"],
        rows=[
            ["Marcellus (US)", "n=357", "微地震+水化学", "地震风险可控", "高"],
            ["Sichuan (CN)", "n=89", "水化学+数值模拟", "浅层水风险低", "中"],
            ["Vaca Muerta (AR)", "n=52", "遥感+地表变形", "地表沉降显著", "中"],
            ["Cooper Basin (AU)", "n=31", "微地震+DFN", "断层再激活风险", "高"],
        ],
        title="全球主要非常规盆地环境影响研究对比",
    )
    b2.add_conclusion(
        ["非常规油气水力压裂的环境影响具有强区域依赖性", "亟需建立标准化的跨区域对比方法体系", "中国四川盆地研究深度显著落后于北美"],
    )
    output2 = out_dir / "nepu-clean-white-reference.pptx"
    b2.save(output2, overwrite=True)
    print(f"Gallery reference PPTX saved to: {output2}")


if __name__ == "__main__":
    main()
