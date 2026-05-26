# 🧠 认知功能障碍在线预测系统

基于Super Learner模型的认知功能障碍风险预测网站

## 📋 功能特点

- **12个预测变量**：涵盖人口统计学、血压血脂、饮食因素和生活方式
- **实时预测**：输入数据后立即获得预测结果
- **风险评估**：提供概率和风险等级
- **因素分析**：识别风险因素和保护因素
- **改善建议**：提供个性化的健康管理建议

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行网站

```bash
streamlit run app.py
```

### 3. 在浏览器中打开

打开 http://localhost:8501

## 📊 输入变量

| 变量 | 名称 | 单位 | 范围 |
|------|------|------|------|
| 年龄 | age | 岁 | 18-100 |
| 性别 | gender | - | 1=男, 2=女 |
| 教育水平 | education | 等级 | 1-5 |
| 家庭收入贫困比 | income_poverty | 比值 | 0-10 |
| 收缩压 | sbp | mmHg | 80-200 |
| 高密度脂蛋白 | hdl | mg/dL | 20-100 |
| 总胆固醇 | tc | mg/dL | 100-300 |
| 咖啡因 | caffeine | 毫克 | 0-500 |
| α-生育酚 | alpha_tocopherol | 毫克 | 0-50 |
| 总脂肪 | total_fat | 克 | 0-200 |
| 多不饱和脂肪酸 | poly_fat | 克 | 0-50 |
| 每天用电脑时长 | computer_hours | 小时 | 0-24 |

## ⚠️ 重要说明

1. **模型说明**：当前版本使用简化的预测逻辑进行演示
2. **医学声明**：预测结果仅供参考，不能替代专业医疗诊断
3. **数据安全**：所有输入数据仅在本地处理，不会上传到任何服务器

## 🔧 部署到云端

### 部署到 Streamlit Cloud

1. 将代码推送到 GitHub
2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
3. 连接 GitHub 仓库并部署

### 部署到 Heroku

1. 创建 `Procfile`: `web: streamlit run app.py --server.port $PORT`
2. 创建 `setup.sh`: `mkdir -p ~/.streamlit && echo "[server]\nport = $PORT\nenableCORS = false\nenableXsrfProtection = false" > ~/.streamlit/config.toml`
3. 部署到 Heroku

## 📁 文件结构

```
predict_website/
├── app.py              # 主应用文件
├── requirements.txt    # Python依赖
├── README.md          # 使用说明
└── templates/         # HTML模板（如有）
    └── index.html
```

## 🎨 界面预览

网站包含以下主要区域：
- **侧边栏**：模型信息和使用说明
- **主内容区**：
  - 输入表单（两列布局）
  - 预测按钮
  - 预测结果展示
  - 风险因素分析
  - 改善建议

## 📞 技术支持

如有问题，请联系开发团队。

## 📄 许可证

© 2026 All Rights Reserved
