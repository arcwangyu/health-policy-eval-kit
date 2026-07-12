# 卫生政策评价工具包

这是一个面向卫生政策与卫生服务研究的轻量、透明、可重复分析工具包。

首个版本聚焦面板中断时间序列分析，提供合成数据生成、面板结构检查、单位固定效应估计、单位层面聚类稳健标准误、示例代码、自动测试和方法学说明。

## 适用场景

- 公立医院改革评价
- DRG、DIP与医保支付政策评价
- 多机构政策实施前后趋势分析
- 准实验方法教学
- 可重复研究示范

## 安装

```bash
git clone https://github.com/arcwangyu/health-policy-eval-kit.git
cd health-policy-eval-kit
python -m pip install -e ".[dev]"
```

## 快速运行

```python
from health_policy_eval import simulate_panel_its, fit_panel_its

data = simulate_panel_its(
    n_units=30,
    n_periods=24,
    intervention_time=12,
    level_effect=-2.0,
    slope_effect=-0.15,
    seed=2026,
)

result = fit_panel_its(
    data=data,
    outcome="outcome",
    unit="unit",
    time="time",
    intervention_time=12,
)

print(result.effect_table())
```

## 方法边界

模型输出不能单独证明因果关系。研究者仍需论证政策时间点、共同干预、趋势设定、测量误差、样本量、序列相关和稳健性检验。涉及真实医疗数据时，不得将患者级可识别数据上传至公开仓库。
