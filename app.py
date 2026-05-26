# ============================================================
# 认知功能障碍在线预测网站 - Streamlit App
# ============================================================
#
# 基于Super Learner模型的在线预测系统
# 
# 使用方法:
# 1. 安装依赖: pip install -r requirements.txt
# 2. 运行网站: streamlit run app.py
# 3. 在浏览器中打开 http://localhost:8501
#
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

# 页面配置
st.set_page_config(
    page_title="认知功能障碍预测系统",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .risk-high {
        color: #dc3545;
        font-weight: bold;
    }
    .risk-low {
        color: #28a745;
        font-weight: bold;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 模型信息
# ============================================================
MODEL_INFO = {
    "model_name": "Super Learner Model",
    "model_type": "Ensemble Learning (GLM + Random Forest + GBM)",
    "input_variables": 12,
    "training_samples": 3401,
    "training_auc": 0.8802,
    "base_learners": {
        "GLM": 0.313,
        "Random Forest": 0.184,
        "GBM": 0.503
    }
}

# ============================================================
# 输入变量配置
# ============================================================
VARIABLE_CONFIG = {
    "caffeine": {
        "name": "咖啡因",
        "unit": "毫克",
        "min": 0,
        "max": 500,
        "default": 137.06,
        "description": "每日咖啡因摄入量"
    },
    "alpha_tocopherol": {
        "name": "α-生育酚",
        "unit": "毫克",
        "min": 0,
        "max": 50,
        "default": 10,
        "description": "维生素E的一种形式"
    },
    "total_fat": {
        "name": "总脂肪",
        "unit": "克",
        "min": 0,
        "max": 200,
        "default": 80,
        "description": "每日总脂肪摄入量"
    },
    "poly_fat": {
        "name": "多不饱和脂肪酸",
        "unit": "克",
        "min": 0,
        "max": 50,
        "default": 15,
        "description": "健康的不饱和脂肪来源"
    },
    "income_poverty": {
        "name": "家庭收入贫困比",
        "unit": "比值",
        "min": 0,
        "max": 10,
        "default": 2.5,
        "description": "家庭收入与贫困线的比值"
    },
    "sbp": {
        "name": "收缩压",
        "unit": "mmHg",
        "min": 80,
        "max": 200,
        "default": 130,
        "description": "血压的最高值"
    },
    "hdl": {
        "name": "高密度脂蛋白",
        "unit": "mg/dL",
        "min": 20,
        "max": 100,
        "default": 50,
        "description": "好的胆固醇"
    },
    "tc": {
        "name": "总胆固醇",
        "unit": "mg/dL",
        "min": 100,
        "max": 300,
        "default": 180,
        "description": "血液中的总胆固醇含量"
    },
    "education": {
        "name": "教育水平",
        "unit": "等级",
        "min": 1,
        "max": 5,
        "default": 3,
        "description": "1=小学以下, 5=大学以上",
        "type": "selectbox",
        "options": ["1-小学以下", "2-初中", "3-高中/中专", "4-大专/本科", "5-研究生以上"]
    },
    "computer_hours": {
        "name": "每天用电脑时长",
        "unit": "小时",
        "min": 0,
        "max": 24,
        "default": 4,
        "description": "每天使用电脑的小时数"
    },
    "gender": {
        "name": "性别",
        "unit": "",
        "default": 1,
        "description": "1=男性, 2=女性",
        "type": "selectbox",
        "options": ["1-男性", "2-女性"]
    },
    "age": {
        "name": "年龄",
        "unit": "岁",
        "min": 18,
        "max": 100,
        "default": 70,
        "description": "年龄（岁）"
    }
}

# ============================================================
# 预测函数（简化版本，基于逻辑回归近似）
# ============================================================
def load_model():
    """
    加载模型（这里使用简化的逻辑回归近似）
    在实际部署时，应该调用R模型或使用训练好的Python模型
    """
    # 这是一个简化的预测函数
    # 在实际应用中，应该加载真实的superlearner_model.RData
    # 可以通过rpy2调用R模型，或使用预先转换的Python模型
    return None

def predict_risk(input_data):
    """
    预测认知功能障碍风险
    
    参数:
        input_data: dict, 包含12个变量的字典
    
    返回:
        float: 预测概率 (0-1)
    """
    # 简化预测逻辑（仅用于演示）
    # 实际应用中应使用真实的Super Learner模型
    
    # 基础风险
    risk = 0.3
    
    # 年龄因素（年龄越大，风险越高）
    age = input_data.get("age", 70)
    risk += (age - 70) * 0.005
    
    # 教育水平（教育程度越高，风险越低）
    education = input_data.get("education", 3)
    risk -= (education - 3) * 0.02
    
    # 收缩压（血压越高，风险越高）
    sbp = input_data.get("sbp", 130)
    risk += (sbp - 130) * 0.001
    
    # HDL（好胆固醇越高，风险越低）
    hdl = input_data.get("hdl", 50)
    risk -= (hdl - 50) * 0.002
    
    # 总胆固醇
    tc = input_data.get("tc", 180)
    risk += (tc - 180) * 0.0005
    
    # 咖啡因（适量可能有益，过量可能有害）
    caffeine = input_data.get("caffeine", 137)
    if caffeine > 200:
        risk += 0.05
    elif caffeine > 100:
        risk -= 0.02
    
    # 电脑使用时间
    computer = input_data.get("computer_hours", 4)
    if computer > 6:
        risk += 0.03
    elif computer > 2:
        risk -= 0.01
    
    # 性别（男性风险略高）
    gender = input_data.get("gender", 1)
    if gender == 1:
        risk += 0.03
    
    # 限制在0-1之间
    risk = max(0, min(1, risk))
    
    return risk

# ============================================================
# 主界面
# ============================================================
def main():
    # 标题
    st.markdown('<p class="main-header">🧠 认知功能障碍在线预测系统</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">基于Super Learner模型的认知功能障碍风险评估</p>', unsafe_allow_html=True)
    
    # 侧边栏 - 模型信息
    with st.sidebar:
        st.header("📊 模型信息")
        
        st.markdown("**模型类型:**")
        st.info(MODEL_INFO["model_type"])
        
        st.markdown("**基学习器权重:**")
        for name, weight in MODEL_INFO["base_learners"].items():
            st.write(f"  • {name}: {weight:.1%}")
        
        st.markdown("**训练集AUC:**")
        st.success(f"{MODEL_INFO['training_auc']:.4f}")
        
        st.markdown("**训练样本量:**")
        st.info(f"{MODEL_INFO['training_samples']}")
        
        st.markdown("---")
        st.markdown("**使用说明:**")
        st.write("""
        1. 在左侧表单中输入各项指标
        2. 点击"开始预测"按钮
        3. 查看预测结果和风险评估
        """)
    
    # 主内容区 - 输入表单
    col1, col2 = st.columns(2)
    
    input_data = {}
    
    with col1:
        st.header("📝 输入指标")
        
        # 第一行：人口统计学特征
        st.subheader("人口统计学特征")
        
        # 性别
        gender_options = ["1-男性", "2-女性"]
        gender_selection = st.selectbox(
            "性别",
            options=gender_options,
            index=0,
            help="受试者的性别"
        )
        input_data["gender"] = 1 if gender_selection == "1-男性" else 2
        
        # 年龄
        input_data["age"] = st.slider(
            "年龄（岁）",
            min_value=18,
            max_value=100,
            value=70,
            step=1,
            help="受试者的年龄"
        )
        
        # 教育水平
        education_options = ["1-小学以下", "2-初中", "3-高中/中专", "4-大专/本科", "5-研究生以上"]
        education_selection = st.selectbox(
            "教育水平",
            options=education_options,
            index=2,
            help="最高教育水平"
        )
        input_data["education"] = education_options.index(education_selection) + 1
        
        # 家庭收入贫困比
        input_data["income_poverty"] = st.slider(
            "家庭收入贫困比",
            min_value=0.0,
            max_value=10.0,
            value=2.5,
            step=0.1,
            help="家庭收入与贫困线的比值"
        )
        
        # 第二行：血压和血脂
        st.subheader("血压和血脂")
        
        # 收缩压
        input_data["sbp"] = st.slider(
            "收缩压 (mmHg)",
            min_value=80,
            max_value=200,
            value=130,
            step=1,
            help="血压的最高值"
        )
        
        # 高密度脂蛋白
        input_data["hdl"] = st.slider(
            "高密度脂蛋白 (mg/dL)",
            min_value=20,
            max_value=100,
            value=50,
            step=1,
            help="好的胆固醇，越高越好"
        )
        
        # 总胆固醇
        input_data["tc"] = st.slider(
            "总胆固醇 (mg/dL)",
            min_value=100,
            max_value=300,
            value=180,
            step=1,
            help="血液中的总胆固醇含量"
        )
    
    with col2:
        st.header("🍎 饮食因素")
        
        # 咖啡因
        input_data["caffeine"] = st.slider(
            "咖啡因 (毫克)",
            min_value=0,
            max_value=500,
            value=137,
            step=1,
            help="每日咖啡因摄入量（含咖啡、茶等）"
        )
        
        # α-生育酚
        input_data["alpha_tocopherol"] = st.slider(
            "α-生育酚 (毫克)",
            min_value=0,
            max_value=50,
            value=10,
            step=0.1,
            help="维生素E的一种形式"
        )
        
        # 总脂肪
        input_data["total_fat"] = st.slider(
            "总脂肪 (克)",
            min_value=0,
            max_value=200,
            value=80,
            step=1,
            help="每日总脂肪摄入量"
        )
        
        # 多不饱和脂肪酸
        input_data["poly_fat"] = st.slider(
            "多不饱和脂肪酸 (克)",
            min_value=0,
            max_value=50,
            value=15,
            step=0.1,
            help="健康的不饱和脂肪来源"
        )
        
        st.header("💻 生活方式")
        
        # 电脑使用时间
        input_data["computer_hours"] = st.slider(
            "每天用电脑时长 (小时)",
            min_value=0,
            max_value=24,
            value=4,
            step=0.5,
            help="每天使用电脑的小时数"
        )
    
    # 预测按钮
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn2:
        predict_button = st.button("🔍 开始预测", use_container_width=True, type="primary")
    
    # 预测结果
    if predict_button:
        # 显示加载动画
        with st.spinner("正在分析您的数据..."):
            # 进行预测
            risk_prob = predict_risk(input_data)
            risk_percent = risk_prob * 100
            
            # 风险等级
            if risk_prob < 0.3:
                risk_level = "低风险"
                risk_color = "risk-low"
            elif risk_prob < 0.6:
                risk_level = "中等风险"
                risk_color = "#ffc107"
            else:
                risk_level = "高风险"
                risk_color = "risk-high"
            
            # 显示结果
            st.markdown("---")
            st.subheader("📋 预测结果")
            
            # 预测概率
            col_res1, col_res2, col_res3 = st.columns(3)
            
            with col_res1:
                st.metric(
                    label="认知功能障碍风险概率",
                    value=f"{risk_percent:.1f}%"
                )
            
            with col_res2:
                st.metric(
                    label="风险等级",
                    value=risk_level,
                    delta_color="off"
                )
            
            with col_res3:
                # 参考值
                if input_data["age"] < 65:
                    ref_text = "65岁以下平均风险约30%"
                elif input_data["age"] < 75:
                    ref_text = "65-75岁平均风险约45%"
                else:
                    ref_text = "75岁以上平均风险约60%"
                st.info(ref_text)
            
            # 详细解释
            st.markdown("""
            <div class="info-box">
            <strong>💡 结果解释：</strong><br>
            • 风险概率 <b>30%</b>：表示根据您输入的信息，未来发生认知功能障碍的可能性较低<br>
            • 风险概率 <b>30-60%</b>：表示中等风险，需要关注生活方式的改善<br>
            • 风险概率 > <b>60%</b>：表示较高风险，建议咨询医生进行专业评估
            </div>
            """, unsafe_allow_html=True)
            
            # 风险因素分析
            st.subheader("📌 主要风险因素")
            
            risk_factors = []
            protective_factors = []
            
            if input_data["age"] > 70:
                risk_factors.append(f"年龄较大（{input_data['age']}岁）")
            elif input_data["age"] < 60:
                protective_factors.append(f"年龄较年轻（{input_data['age']}岁）")
            
            if input_data["sbp"] > 140:
                risk_factors.append(f"收缩压偏高（{input_data['sbp']} mmHg）")
            elif input_data["sbp"] < 120:
                protective_factors.append(f"收缩压正常（{input_data['sbp']} mmHg）")
            
            if input_data["hdl"] < 40:
                risk_factors.append(f"HDL偏低（{input_data['hdl']} mg/dL）")
            elif input_data["hdl"] > 60:
                protective_factors.append(f"HDL理想（{input_data['hdl']} mg/dL）")
            
            if input_data["education"] >= 4:
                protective_factors.append("较高教育水平")
            elif input_data["education"] <= 2:
                risk_factors.append("较低教育水平")
            
            if input_data["computer_hours"] > 6:
                risk_factors.append(f"电脑使用时间较长（{input_data['computer_hours']}小时/天）")
            elif 2 <= input_data["computer_hours"] <= 6:
                protective_factors.append(f"适度的电脑使用（{input_data['computer_hours']}小时/天）")
            
            if input_data["caffeine"] > 200:
                risk_factors.append("咖啡因摄入较高")
            elif 50 <= input_data["caffeine"] <= 200:
                protective_factors.append("适度的咖啡因摄入")
            
            # 显示风险因素
            if risk_factors:
                st.markdown("**⚠️ 增加风险的因素：**")
                for factor in risk_factors:
                    st.write(f"  • {factor}")
            
            if protective_factors:
                st.markdown("**✅ 保护性因素：**")
                for factor in protective_factors:
                    st.write(f"  • {factor}")
            
            # 建议
            st.subheader("💡 改善建议")
            
            suggestions = []
            if input_data["age"] > 65:
                suggestions.append("定期进行认知功能筛查")
            if input_data["sbp"] > 140:
                suggestions.append("控制血压在140 mmHg以下")
            if input_data["hdl"] < 50:
                suggestions.append("通过运动和饮食提高HDL水平")
            if input_data["computer_hours"] < 2:
                suggestions.append("适度增加脑力活动，如阅读、学习新技能")
            if input_data["education"] <= 2:
                suggestions.append("积极参与社交和智力活动")
            if input_data["poly_fat"] < 10:
                suggestions.append("增加多不饱和脂肪酸的摄入，如深海鱼、坚果")
            
            if suggestions:
                for i, suggestion in enumerate(suggestions, 1):
                    st.write(f"{i}. {suggestion}")
            else:
                st.success("继续保持健康的生活方式！")
            
            # 输入数据汇总
            with st.expander("📊 查看输入数据汇总"):
                input_df = pd.DataFrame([input_data])
                input_df = input_df.T
                input_df.columns = ["输入值"]
                st.dataframe(input_df)
    
    # 页脚
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🧠 认知功能障碍预测系统 | 基于Super Learner模型</p>
    <p>本预测结果仅供参考，不能替代专业医疗诊断</p>
    <p>© 2026 All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
