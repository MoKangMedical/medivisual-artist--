"""
MediVisual Artist — 医学数据可视化引擎

用户视角：上传医学数据 → 自动选择最佳图表类型 → 生成发表级图表
"""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ChartSpec:
    """图表规格"""
    chart_type: str        # survival_curve/forest_plot/km_plot/bar_chart/heatmap
    title: str
    x_label: str
    y_label: str
    data_columns: List[str]
    style: Dict
    output_format: str = "png"


class MediVisualEngine:
    """医学可视化引擎"""
    
    # 数据类型→图表映射
    CHART_MAP = {
        "survival": ["km_plot", "survival_curve"],
        "comparison": ["bar_chart", "box_plot", "violin_plot"],
        "correlation": ["heatmap", "scatter_plot"],
        "trend": ["line_chart", "area_chart"],
        "distribution": ["histogram", "density_plot"],
        "proportion": ["pie_chart", "stacked_bar"],
        "forest": ["forest_plot"],
    }
    
    def recommend_chart(self, data_description: str, columns: List[str]) -> List[ChartSpec]:
        """推荐最佳图表类型"""
        desc_lower = data_description.lower()
        recommendations = []
        
        if any(w in desc_lower for w in ["生存", "survival", "死亡", "预后"]):
            recommendations.append(ChartSpec(
                chart_type="km_plot",
                title="Kaplan-Meier生存曲线",
                x_label="时间（月）",
                y_label="生存率",
                data_columns=["time", "event", "group"],
                style={"theme": "medical", "colors": ["#2196F3", "#F44336", "#4CAF50"]}
            ))
        
        if any(w in desc_lower for w in ["比较", "对比", "组间", "vs"]):
            recommendations.append(ChartSpec(
                chart_type="forest_plot",
                title="森林图",
                x_label="风险比 (95% CI)",
                y_label="亚组",
                data_columns=["group", "hr", "ci_lower", "ci_upper"],
                style={"theme": "medical", "null_line": True}
            ))
        
        if any(w in desc_lower for w in ["趋势", "变化", "年度", "趋势"]):
            recommendations.append(ChartSpec(
                chart_type="line_chart",
                title="趋势变化图",
                x_label="年份",
                y_label="率",
                data_columns=["year", "rate"],
                style={"theme": "medical", "confidence_band": True}
            ))
        
        # 默认推荐
        if not recommendations:
            recommendations.append(ChartSpec(
                chart_type="bar_chart",
                title="数据分布",
                x_label="类别",
                y_label="数值",
                data_columns=columns[:3],
                style={"theme": "medical"}
            ))
        
        return recommendations
    
    def generate_chart_config(self, spec: ChartSpec) -> Dict:
        """生成图表配置（支持matplotlib/plotly）"""
        return {
            "matplotlib": {
                "type": spec.chart_type,
                "title": spec.title,
                "xlabel": spec.x_label,
                "ylabel": spec.y_label,
                "style": "seaborn-v0_8-whitegrid",
                "figsize": [10, 6],
                "dpi": 300,
            },
            "plotly": {
                "type": spec.chart_type,
                "title": spec.title,
                "template": "plotly_white",
                "width": 800,
                "height": 500,
            },
            "columns": spec.data_columns,
            "output": f"output/{spec.chart_type}.{spec.output_format}"
        }
    
    def get_style_guide(self) -> Dict:
        """获取医学期刊图表样式指南"""
        return {
            "font": "Arial/Helvetica",
            "font_size": {"title": 14, "label": 12, "tick": 10, "legend": 10},
            "colors": {
                "primary": "#2196F3",
                "secondary": "#F44336",
                "tertiary": "#4CAF50",
                "neutral": "#9E9E9E",
            },
            "line_width": 1.5,
            "marker_size": 6,
            "dpi": 300,
            "format": "TIFF (Nature/Science) or PDF (others)",
        }


if __name__ == "__main__":
    engine = MediVisualEngine()
    charts = engine.recommend_chart("生存分析数据，比较两组患者的生存率", ["time", "event", "group"])
    for c in charts:
        print(f"📊 {c.chart_type}: {c.title}")
        print(json.dumps(engine.generate_chart_config(c), ensure_ascii=False, indent=2))
