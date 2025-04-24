# aiccm

> 用于分析和处理角膜共聚焦显微镜角膜神经图像的Python软件包

## About

官方网站: www.aiccm.fun

如果对你的研究有帮助，请引用我们的论文：

```
Qiao Q, Cao J, Xue W, et al. Deep learning-based automated tool for diagnosing diabetic peripheral neuropathy. Digit Health. 2024;10:20552076241307573. Published 2024 Dec 25. doi:10.1177/20552076241307573
```

## Setup
```shell
pip install aiccm
```
or
```shell
conda create -n aiccm python=3.10
conda activate aiccm
pip install -r requirements.txt
```

## Use
### 1. 获取二值化/骨架化图像
```shell
import aiccm

# 读取你的CCM图像
# 支持的图像分辨率为应该为384*384或384*484，读取后统一转换为384*384
image = aiccm.load_ccm_image('test.jpg')  

binary = aiccm.get_binary(image)  # 二值化图像
skeleton = aiccm.get_skeleton(binary)  # 骨架化图像

aiccm.show_image(binary)
aiccm.show_image(skeleton)
```

### 2. AiCCMetrics功能
```shell
import aiccm
import os


image = aiccm.load_ccm_image('test.jpg')

metrics_result = aiccm.get_metrics(image)
print(metrics_result)
aiccm.show_image(aiccm.get_bone_image(image))
aiccm.show_image(aiccm.get_body_image(image))
```
