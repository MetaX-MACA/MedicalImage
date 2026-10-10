# 沐曦GPU加速医学影像智能分析

本文件夹汇集了多个可用于**沐曦（MetaX）GPU**的**人工智能医学影像**解决方案。我们专注于提供高性能、易适配的AI算力支撑，助力您在影像分割、辅助诊断、三维重建、智能标注等领域的科研与临床转化工作。

---

## 📂 项目结构与说明

本文件夹以**聚合分发**方式提供多个相互独立的开源项目与适配方案，各项目作为独立程序分别置于各自子目录中，我方仅将其聚合打包传输，并未将其组合为单一作品。各项目分别受其自带许可证约束，您在使用或分发任一项目前，须遵守该项目对应许可证的条款。如各项目内另附有我方提供的Patch文件或适配文件，系针对相应开源项目的修改或组合，此文件的许可证放置于对应文件夹中。

当前包含以下独立子项目：

| 子目录 | 项目简介 | 主要领域 |
|---|---|---|
| **[MONAI](https://github.com/MetaX-MACA/MedicalImage/tree/main/MONAI)** | MONAI核心框架的沐曦GPU适配版本，提供医学影像专用的数据处理、变换方法与网络架构。 | 影像分割、分类、配准、生成建模 |
| **[MedSAM](https://github.com/Metax-MACA/MedicalImage/tree/main/segmentation/MedSAM)**|专为医学图像分割设计的 Segment Anything 模型变体。| 影像分割 |
| **[MedSAM2](https://github.com/Metax-MACA/MedicalImage/tree/main/segmentation/MedSAM2)**|面向3D图像与视频分割的可提示分割基础模型。| 影像分割 |
| **[nnInteractive](https://github.com/Metax-MACA/MedicalImage/tree/main/segmentation/nnInteractive)**|三维交互式分割模型，支持点、涂抹、边界框以及套索等多种提示方式。。| 影像分割 |
| **[nnUNet](https://github.com/Metax-MACA/MedicalImage/tree/main/segmentation/nnUNet)**|针对特定数据集自动适配流程的语义分割框架。自动配置最合适的`U-Net`变体，并提供从数据预处理、模型训练、模型筛选到推理预测的一站式端到端解决方案。| 影像分割 |
| **[SAM-Med3D](https://github.com/Metax-MACA/MedicalImage/tree/main/segmentation/SAM-Med3D)**|面向三维医学图像的通用分割模型。| 影像分割 |
| **[TotalSegmentatorV2](https://github.com/Metax-MACA/MedicalImage/tree/main/segmentation/TotalSegmentatorV2)**|基于**nnUNet**模型的CT图像分割工具。| 影像分割 |
| **[vista3d](https://github.com/Metax-MACA/MedicalImage/tree/main/segmentation/vista3d)**|三维医学影像分割基础模型。| 影像分割 |
| **[prov-gigapath](https://github.com/Metax-MACA/MedicalImage/tree/main/pathology/prov-gigapath)** | 全切片病理基础模型 | 病理学 |
| **[Hibou](https://github.com/Metax-MACA/MedicalImage/tree/main/pathology/hibou)** | 面向数字病理图像的基础视觉 Transformer，可提取 CLS embedding、patch token 和中间层表示。 | 病理学 |
| **[nv-generate-ct-rflow](https://github.com/Metax-MACA/MedicalImage/tree/main/generative/nv-generate-ct-rflow)** | 基于 MAISI 的三维医学影像 latent diffusion 生成项目，支持合成 CT、解剖标签图、条件 CT 以及 CT/标签配对生成。 | 影像生成 |
| **[nv-generate-mr](https://github.com/Metax-MACA/MedicalImage/tree/main/generative/nv-generate-mr)** | 基于 `rflow-mr` 的三维 MRI 生成模型，按体素间距和 MRI 模态条件生成合成影像。 | 影像生成 |
| **[nv-generate-mr-brain](https://github.com/Metax-MACA/MedicalImage/tree/main/generative/nv-generate-mr-brain)** | 基于 `rflow-mr-brain` 的三维脑部 MRI 生成模型，从随机噪声生成脑部合成影像。 | 影像生成 |
| **[Plastimatch](https://github.com/Metax-MACA/MedicalImage/tree/main/registration/plastimatch)** | 三维医学影像处理工具集，覆盖刚性/B-spline 配准、DRR 投影和 FDK 锥束 CT 重建。 | 影像配准、重建 |
| **[uniGradICON](https://github.com/Metax-MACA/MedicalImage/tree/main/registration/unigradicon)** | 基于 GradICON 梯度逆一致性约束的三维医学影像基础模型，用于估计 CT、MRI 等影像的稠密可变形映射。 | 影像配准 |
| **[BiomedCLIP](https://github.com/Metax-MACA/MedicalImage/tree/main/vlm/BiomedCLIP)** | 基于 PubMedBERT 和 ViT 的生物医学视觉语言模型，支持零样本分类与图文跨模态检索。 | 视觉语言、图文检索 |
| **[Lingshu-7B](https://github.com/Metax-MACA/MedicalImage/tree/main/vlm/lingshu)** | 医学多模态理解与推理模型，支持医学图像问答、描述和报告生成。 | 医学视觉语言 |
| **[M3D-LaMed](https://github.com/Metax-MACA/MedicalImage/tree/main/vlm/m3d)** | 三维医学图像多模态大语言模型，支持图像描述、视觉问答、目标定位和器官分割。 | 三维视觉语言 |
| **[MedCLIP](https://github.com/Metax-MACA/MedicalImage/tree/main/vlm/medclip)** | 医学图像与报告文本的对比学习模型，支持图文相似度和 CheXpert 提示分类。 | 视觉语言、影像理解 |
| **[Merlin](https://github.com/Metax-MACA/MedicalImage/tree/main/vlm/merlin)** | 面向三维 CT 表征与医学推理的模型，支持图文/图像嵌入、表型预测、疾病风险预测和放射学报告生成。 | 三维视觉语言 |
| **[NV-Reason-CXR](https://github.com/Metax-MACA/MedicalImage/tree/main/vlm/nv-reason-cxr)** | 面向正位胸部 X 光的视觉语言推理模型，支持异常分析、鉴别考虑、随访相关性和结构化报告任务。 | 胸片理解、视觉语言 |
| **[RadFM](https://github.com/Metax-MACA/MedicalImage/tree/main/vlm/radfm)** | 面向放射学的视觉语言基础模型，支持 2D/3D、多图像输入、视觉问答和报告生成。 | 放射学视觉语言 |



> 更多模型和应用正在持续适配与添加中，敬请关注。

---

## 🔧 环境与依赖

- **硬件**：需具备沐曦（MetaX）GPU（曦云C系列、曦思N系列等）。
- **基础软件**：Linux操作系统，沐曦GPU运行时环境。
- **核心依赖**：Python 3.8+，PyTorch（适配沐曦GPU版本），以及各子项目特定的依赖库。
- **加速库支撑**：基于MXMACA异构计算平台，沐曦GPU提供包括深度神经网络加速库、基础线性代数库、稀疏矩阵计算库、傅里叶变换加速库及多卡集合通信库在内的完整加速栈，为MONAI框架提供从底层算子到上层框架的全链路性能优化。

具体安装与使用步骤，请参阅各子项目文件夹内的独立指南（如`README.md`或`UserGuide`）。


---

## ⚠️ 合规与许可证声明

在使用本仓库中的任何资源前，请仔细阅读并遵守以下声明：

1. **独立项目**：本仓库中的每个子项目均为独立的开源项目，保留其原有的许可证和版权声明。MONAI 1.5.2遵循Apache 2.0许可证。我方仅提供聚合分发服务，不对这些项目的功能、安全性或合规性做额外担保。
2. **使用责任**：您有责任理解并遵守每个子项目自带的许可证条款。在使用或分发任何子项目时，请确保完全符合其许可证要求。
3. **修改与组合**：如子项目内包含由我方提供的Patch文件或适配文件，这些特定文件的许可证将放置于对应的子文件夹中，请在使用时一并遵循。

---

## 📝 更新日志

- **2026-09-30**: 增加影像生成、病理学、医学视觉、影像配准等模型。
- **2026-08-20**: 增加segmentation。
- **2026-07-23**：初始版本，基于MONAI 1.5.2版本完成沐曦GPU适配，提供Core、Label、Deploy三大核心模块支持。

---

## 🤝 贡献与反馈

欢迎通过GitHub Issues或Pull Requests提出建议、报告问题或贡献新的适配模型。沐曦正积极构建"算力+模型+应用"三层医疗健康生态体系，期待与开发者共同推动AI在医学影像领域的革新！

---

**感谢您对沐曦GPU生态及AI4S发展的关注与支持！**