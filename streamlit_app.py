"""
认知功能障碍预测系统 - Streamlit版本
部署到MiniMax Space平台
"""

import streamlit as st
import pandas as pd
import subprocess
import os

# 页面配置
st.set_page_config(
    page_title="认知功能障碍预测系统",
    page_icon="🧠",
    layout="wide"
)

# 特征信息
FEATURE_INFO = {
    'caffeine': {'name': '咖啡因', 'unit': '毫克', 'min': 0, 'max': 1720.5, 'mean': 137.06},
    'alpha_tocopherol': {'name': 'α-生育酚', 'unit': '毫克', 'min': 0.22, 'max': 66.08, 'mean': 7.87},
    'total_fat': {'name': '总脂肪', 'unit': '克', 'min': 2.57, 'max': 258.43, 'mean': 68.41},
    'poly_fat': {'name': '多不饱和脂肪酸', 'unit': '克', 'min': 0.86, 'max': 70.06, 'mean': 16.44},
    'income_poverty': {'name': '家庭收入贫困比', 'unit': '', 'min': 0, 'max': 5, 'mean': 2.51},
    'sbp': {'name': '收缩压', 'unit': 'mmHg', 'min': 72, 'max': 238, 'mean': 134.27},
    'hdl': {'name': '高密度脂蛋白', 'unit': 'mg/dL', 'min': 16, 'max': 156, 'mean': 53.85},
    'tc': {'name': '总胆固醇', 'unit': 'mg/dL', 'min': 75, 'max': 525, 'mean': 190.63},
    'education': {'name': '教育水平', 'unit': '', 'min': 1, 'max': 5, 'mean': 3.25},
    'computer_hours': {'name': '每天用电脑时长', 'unit': '小时', 'min': 0, 'max': 8, 'mean': 4.25},
    'gender': {'name': '性别', 'unit': '', 'min': 1, 'max': 2, 'mean': 1.52},
    'age': {'name': '年龄', 'unit': '岁', 'min': 60, 'max': 80, 'mean': 69.80}
}

EDUCATION_OPTIONS = {
    1: '小学及以下',
    2: '初中',
    3: '高中/中专',
    4: '大学/大专',
    5: '研究生及以上'
}

GENDER_OPTIONS = {
    1: '男 👨',
    2: '女 👩'
}

def predict_with_r(data_dict):
    """使用R模型进行预测"""
    model_path = os.path.join(os.path.dirname(__file__), 'GMD', 'superlearner_model.RData')
    model_path = model_path.replace(os.sep, '/')
    
    r_script = f'''
library(SuperLearner)
load("{model_path}")

new_data <- data.frame(
    caffeine = {data_dict.get('caffeine', 0)},
    alpha_tocopherol = {data_dict.get('alpha_tocopherol', 0)},
    total_fat = {data_dict.get('total_fat', 0)},
    poly_fat = {data_dict.get('poly_fat', 0)},
    income_poverty = {data_dict.get('income_poverty', 0)},
    sbp = {data_dict.get('sbp', 0)},
    hdl = {data_dict.get('hdl', 0)},
    tc = {data_dict.get('tc', 0)},
    education = {data_dict.get('education', 1)},
    computer_hours = {data_dict.get('computer_hours', 0)},
    gender = {data_dict.get('gender', 1)},
    age = {data_dict.get('age', 60)}
)

prediction <- predict(sl_final_model, newdata = new_data)$pred
cat(as.character(prediction))
'''
    
    try:
        result = subprocess.run(
            ['Rscript', '-e', r_script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return float(result.stdout.strip())
        else:
            st.error(f"R模型预测失败: {result.stderr}")
            return 0.35
    
    except FileNotFoundError:
        st.warning("R环境未安装，使用模拟预测结果")
        return 0.35
    except Exception as e:
        st.error(f"预测出错: {e}")
        return 0.35

def get_risk_info(prob):
    """获取风险等级信息"""
    if prob < 0.2:
        return ('低风险', '🟢', '#4CAF50', '风险较低。建议保持健康的生活方式。')
    elif prob < 0.4:
        return ('较低风险', '🟡', '#8BC34A', '风险较低，但仍需关注。建议定期体检，保持社交活动和脑力锻炼。')
    elif prob < 0.6:
        return ('中等风险', '🟠', '#FFC107', '风险中等。建议咨询医生进行进一步评估，并积极采取预防措施。')
    elif prob < 0.8:
        return ('较高风险', '🟠', '#FF9800', '风险较高，建议尽快就医进行专业评估和干预。')
    else:
        return ('高风险', '🔴', '#F44336', '风险很高，建议立即寻求专业医疗帮助。')

# 主界面
st.title("🧠 认知功能障碍预测系统")
st.markdown("---")
st.markdown("#### 基于Super Learner模型的智能风险评估")

# 创建两列布局
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📋 基本信息")
    age = st.slider("年龄 (岁)", 60, 80, 70, help="范围: 60-80岁")
    gender = st.radio("性别", options=[1, 2], format_func=lambda x: GENDER_OPTIONS[x], horizontal=True)
    education = st.selectbox("教育水平", options=list(EDUCATION_OPTIONS.keys()), format_func=lambda x: EDUCATION_OPTIONS[x])
    income_poverty = st.slider("家庭收入贫困比", 0.0, 5.0, 2.5, 0.1, help="范围: 0-5")

with col2:
    st.markdown("### 📊 生理指标")
    sbp = st.slider("收缩压 (mmHg)", 72, 238, 130, help="范围: 72-238 mmHg")
    hdl = st.slider("高密度脂蛋白 (mg/dL)", 16, 156, 50, help="范围: 16-156 mg/dL")
    tc = st.slider("总胆固醇 (mg/dL)", 75, 525, 180, help="范围: 75-525 mg/dL")

col3, col4 = st.columns([1, 1])

with col3:
    st.markdown("### 🍎 饮食因素")
    caffeine = st.slider("咖啡因 (毫克)", 0, 1720, 150, help="范围: 0-1720 mg")
    alpha_tocopherol = st.slider("α-生育酚 (毫克)", 0.0, 66.0, 10.0, 0.1, help="范围: 0.22-66 mg")
    total_fat = st.slider("总脂肪 (克)", 3, 258, 80, help="范围: 2.57-258 g")
    poly_fat = st.slider("多不饱和脂肪酸 (克)", 1, 70, 15, help="范围: 0.86-70 g")

with col4:
    st.markdown("### 💻 生活习惯")
    computer_hours = st.slider("每天用电脑时长 (小时)", 0.0, 8.0, 2.0, 0.5, help="范围: 0-8小时/天")

st.markdown("---")

# 预测按钮
if st.button("🎯 开始预测", type="primary", use_container_width=True):
    # 准备输入数据
    input_data = {
        'age': age,
        'gender': gender,
        'education': education,
        'income_poverty': income_poverty,
        'sbp': sbp,
        'hdl': hdl,
        'tc': tc,
        'caffeine': caffeine,
        'alpha_tocopherol': alpha_tocopherol,
        'total_fat': total_fat,
        'poly_fat': poly_fat,
        'computer_hours': computer_hours
    }
    
    with st.spinner("正在分析中..."):
        probability = predict_with_r(input_data)
        risk_level, emoji, color, interpretation = get_risk_info(probability)
    
    st.markdown("---")
    
    # 显示结果
    col_result1, col_result2 = st.columns([1, 2])
    
    with col_result1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color}22, {color}44);
            border: 2px solid {color};
            border-radius: 20px;
            padding: 30px;
            text-align: center;
        ">
            <h1 style="color: {color}; font-size: 4em; margin: 0;">{emoji}</h1>
            <h2 style="color: {color}; margin: 10px 0;">{risk_level}</h2>
            <h1 style="color: {color}; font-size: 3em; margin: 0;">{probability*100:.1f}%</h1>
            <p style="color: #888; margin-top: 10px;">预测概率</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_result2:
        st.markdown(f"""
        <div style="
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            height: 100%;
        ">
            <h3 style="color: #333;">📝 健康建议</h3>
            <p style="font-size: 1.1em; line-height: 1.8; color: #555;">{interpretation}</p>
        </div>
        """, unsafe_allow_html=True)

# 底部说明
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9em; padding: 20px;">
    <p>⚠️ 本预测结果仅供参考，不能替代专业医疗诊断</p>
    <p>如有疑虑，请咨询专业医生</p>
</div>
""", unsafe_allow_html=True)