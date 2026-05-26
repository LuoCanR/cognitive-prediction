# 认知功能障碍预测网站

基于Super Learner模型的认知功能障碍风险预测系统。

## 功能特点

- 12项健康指标输入
- 实时概率预测
- 风险等级评估
- 中文友好界面

## 目录结构

```
predict_website/
├── app.py              # Flask应用主文件
├── templates/
│   └── index.html      # 前端页面
├── static/             # 静态资源目录
└── requirements.txt    # Python依赖
```

## 依赖环境

### Python环境
- Python 3.8+
- Flask 3.0.0+
- pandas

### R环境（用于模型预测）
- R 4.0+
- SuperLearner包

## 安装步骤

### 1. 安装Python依赖
```bash
cd predict_website
pip install -r requirements.txt
```

### 2. 安装R（可选）
如果需要使用真实的Super Learner模型进行预测：
1. 安装R 4.0+: https://cran.r-project.org/
2. 安装SuperLearner包：
```r
install.packages("SuperLearner")
```

### 3. 运行网站
```bash
python app.py
```

然后在浏览器中打开: http://127.0.0.1:5000

## 输入变量说明

| 变量 | 说明 | 单位 | 范围 |
|------|------|------|------|
| age | 年龄 | 岁 | 60-80 |
| gender | 性别 | - | 1=男, 2=女 |
| education | 教育水平 | - | 1-5 |
| income_poverty | 家庭收入贫困比 | - | 0-5 |
| sbp | 收缩压 | mmHg | 72-238 |
| hdl | 高密度脂蛋白 | mg/dL | 16-156 |
| tc | 总胆固醇 | mg/dL | 75-525 |
| caffeine | 咖啡因 | 毫克 | 0-1720.5 |
| alpha_tocopherol | α-生育酚 | 毫克 | 0.22-66.08 |
| total_fat | 总脂肪 | 克 | 2.57-258.43 |
| poly_fat | 多不饱和脂肪酸 | 克 | 0.86-70.06 |
| computer_hours | 每天用电脑时长 | 小时 | 0-8 |

## 模型说明

- **模型类型**: Super Learner集成模型
- **基学习器**: GLM, Random Forest, GBM
- **交叉验证**: 10折
- **输出**: 认知功能障碍预测概率（0-1）

## 注意事项

⚠️ 本预测结果仅供参考，不能替代专业医疗诊断。

## 技术支持

如遇问题，请检查：
1. Python环境是否正确安装
2. R环境是否正确安装（如果使用真实模型）
3. 防火墙是否允许5000端口