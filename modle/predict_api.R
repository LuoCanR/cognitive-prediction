# ============================================================
# Super Learner 预测API脚本
# 用于在线预测网站的后端调用
# ============================================================

# 加载必要的包
library(SuperLearner)

# ------------------------------------------------------------
# 函数: 加载模型
# ------------------------------------------------------------
load_model <- function() {
  load("superlearner_model.RData")
  return(sl_final_model)
}

# ------------------------------------------------------------
# 函数: 获取特征名称
# ------------------------------------------------------------
get_feature_names <- function() {
  features <- readLines("feature_names.txt")
  return(features)
}

# ------------------------------------------------------------
# 函数: 获取变量映射
# ------------------------------------------------------------
get_variable_mapping <- function() {
  mapping <- read.csv("variable_mapping.csv", stringsAsFactors = FALSE)
  colnames(mapping) <- c("中文名称", "英文名称")
  return(mapping)
}

# ------------------------------------------------------------
# 函数: 获取特征统计信息
# ------------------------------------------------------------
get_feature_stats <- function() {
  stats <- read.csv("feature_stats.csv", stringsAsFactors = FALSE)
  return(stats)
}

# ------------------------------------------------------------
# 函数: 预测单个样本
# ------------------------------------------------------------
# 参数: 
#   input_data: data.frame或list，包含所有特征
#   model: 可选，已加载的模型对象
# 返回:
#   预测概率（0-1之间）
# ------------------------------------------------------------
predict_single <- function(input_data, model = NULL) {
  # 如果没有提供模型，加载模型
  if (is.null(model)) {
    model <- load_model()
  }
  
  # 确保输入数据是data.frame格式
  if (!is.data.frame(input_data)) {
    input_data <- as.data.frame(input_data)
  }
  
  # 获取特征名称
  features <- get_feature_names()
  
  # 检查输入是否包含所有必要的特征
  missing_features <- setdiff(features, colnames(input_data))
  if (length(missing_features) > 0) {
    stop(paste("缺少必要的特征:", paste(missing_features, collapse = ", ")))
  }
  
  # 按正确顺序选择特征
  input_data <- input_data[, features, drop = FALSE]
  
  # 预测
  prediction <- predict(model, newdata = input_data)$pred
  
  return(prediction)
}

# ------------------------------------------------------------
# 函数: 预测多个样本
# ------------------------------------------------------------
# 参数: 
#   input_data: data.frame，每行一个样本
#   model: 可选，已加载的模型对象
# 返回:
#   预测概率向量
# ------------------------------------------------------------
predict_batch <- function(input_data, model = NULL) {
  return(predict_single(input_data, model))
}

# ------------------------------------------------------------
# 示例使用
# ------------------------------------------------------------
# 如果你想测试这个API，可以取消注释下面的代码
# 
# # 加载模型
# model <- load_model()
# 
# # 获取特征信息
# features <- get_feature_names()
# mapping <- get_variable_mapping()
# stats <- get_feature_stats()
# 
# # 创建一个测试样本
# test_sample <- data.frame(
#   caffeine = 150,          # 咖啡因（毫克）
#   alpha_tocopherol = 10,   # α-生育酚（毫克）
#   total_fat = 80,          # 总脂肪（克）
#   poly_fat = 15,           # 多不饱和脂肪酸（克）
#   income_poverty = 2.5,    # 家庭收入贫困比
#   sbp = 130,               # 收缩压
#   hdl = 50,                # 高密度脂蛋白
#   tc = 180,                # 总胆固醇
#   education = 3,           # 教育水平
#   computer_hours = 2,      # 每天用电脑时长
#   gender = 1,              # 性别（1=男, 2=女）
#   age = 70                 # 年龄（岁）
# )
# 
# # 预测
# prob <- predict_single(test_sample, model)
# cat("预测概率:", prob, "\n")

# ------------------------------------------------------------
# API说明
# ------------------------------------------------------------
# 1. 加载模型: model <- load_model()
# 2. 准备输入: data.frame格式，列名必须与feature_names.txt一致
# 3. 调用预测: predict_single(input_data, model)
# 4. 返回值: 认知功能障碍的预测概率
# ------------------------------------------------------------
