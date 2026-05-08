# 📚 PyTorch Cheatsheets Master Index

**Where to find what you need in your PyTorch cheatsheets collection**

---

## 🏗️ **ARCHITECTURES & MODEL BUILDING**

### **DNN (Dense Neural Networks)**
- **Basic DNN templates**: `full_DNN.md` (scenarios for binary/multi-class/regression)
- **Layer stacking explanation**: `stacking.md` (how neurons stack to form DNNs)
- **Single neuron learning**: `one_neuron.md` (watch a neuron learn step-by-step)
- **Complete DNN pipelines**: `complete_dnn_examples.md` (full preprocessing → training → deployment)

### **Essential Building Blocks**
- **Sequential, BatchNorm, Dropout**: `sequential_batchnorm_dropout.md` (modern neural network fundamentals)

### **CNN (Convolutional Neural Networks)**
- **CNN basics & architecture**: `CNN_guide.md` (kernels, pooling, channels, dimension flow)
- **Complete CNN pipelines**: `CNN_pipeline_examples.md` (MNIST, CIFAR-10, custom dataset examples)
- **Advanced CNN examples**: `complete_cnn_examples.md` (CIFAR-10 with modern techniques, Grad-CAM)
- **CNN vs DNN comparison**: `CNN_guide.md` (when to use each)

---

## ⚙️ **OPTIMIZERS & TRAINING**

### **Built-in Optimizers**
- **Adam, SGD, RMSprop tuning**: `optimizer_guide.md` (parameters, when to use each)
- **Activation + Loss + Optimizer combos**: `activation_loss_optimizer_examples.md` (complete examples)

### **From Scratch Implementations**
- **SGD, Adam, AdamW from scratch**: `optimizers_from_scratch_tutorial.md` (math + code)
- **Custom optimizer comparison**: `optimizers_from_scratch_tutorial.md` (convergence plots)

---

## 📊 **DATA PREPROCESSING**

### **Complete Pipeline**
- **CSV → PyTorch DataLoader**: `data_preprocessing_tutorial.md` (full workflow)
- **Dataset & DataLoader classes**: `data_preprocessing_tutorial.md` (custom implementations)
- **Train/test splitting**: `data_preprocessing_tutorial.md` (stratified, time series)

### **Dataset vs DataLoader**
- **Dataset vs DataLoader explained**: `dataset_vs_dataloader.md` (what each does, why both needed)

### **Data Cleaning**
- **Pandas preprocessing**: `data_preprocessing_tutorial.md` (nulls, duplicates, outliers)
- **Feature scaling/encoding**: `data_preprocessing_tutorial.md` (StandardScaler, OneHot)

---

## 📏 **TENSOR DIMENSIONS & DEBUGGING**

### **Dimension Conventions**
- **PyTorch tensor shapes**: `pytorch_dimensions_for_noobs.md` (batch first, channels first)
- **Layer input/output shapes**: `pytorch_dimensions_for_noobs.md` (Linear, Conv2d, Pool)
- **Common dimension mistakes**: `pytorch_dimensions_for_noobs.md` (fixes for errors)

### **Debugging Tools**
- **Shape checking/reshaping**: `pytorch_dimensions_for_noobs.md` (.view, .unsqueeze)
- **Complete network with shapes**: `pytorch_dimensions_for_noobs.md` (step-by-step tracking)

---

## 🔄 **ACTIVATIONS, LOSSES & TRAINING PATTERNS**

### **Activation Functions**
- **ReLU, Sigmoid, Tanh, etc.**: `full_DNN.md` (when to use each)
- **Activation + loss combos**: `activation_loss_optimizer_examples.md` (complete examples)

### **Loss Functions**
- **MSE, CrossEntropy, BCELoss**: `full_DNN.md` (regression vs classification)
- **Loss function decision tree**: `full_DNN.md` (which for which problem)

---

## 🎯 **PROBLEM-SPECIFIC GUIDES**

### **Classification Problems**
- **Binary classification**: `full_DNN.md` (Sigmoid + BCELoss)
- **Multiclass classification**: `full_DNN.md` (Softmax + CrossEntropyLoss)
- **Image classification**: `CNN_guide.md` + `CNN_pipeline_examples.md`
- **Complete binary classification**: `complete_dnn_examples.md` (loan default prediction)
- **Advanced image classification**: `complete_cnn_examples.md` (CIFAR-10 with Grad-CAM)

### **Regression Problems**
- **Continuous output prediction**: `full_DNN.md` (no activation + MSELoss)
- **Complete regression example**: `complete_dnn_examples.md` (house price prediction)

### **Image Processing**
- **CNN architectures**: `CNN_guide.md` (Small/Medium/Large CNNs)
- **Image data loading**: `CNN_pipeline_examples.md` (transforms, normalization)
- **Custom image datasets**: `CNN_pipeline_examples.md`
- **Advanced CNN techniques**: `complete_cnn_examples.md` (modern architecture, data augmentation)

---

## 🐛 **TROUBLESHOOTING & COMMON ISSUES**

### **Dimension Errors**
- **"size mismatch"**: `pytorch_dimensions_for_noobs.md` (batch dimension missing)
- **"mat1 and mat2 shapes"**: `pytorch_dimensions_for_noobs.md` (Linear input size wrong)
- **CNN channel errors**: `pytorch_dimensions_for_noobs.md` (channels first vs last)

### **Training Issues**
- **Loss not decreasing**: `optimizer_guide.md` (learning rate too high/low)
- **Overfitting**: `optimizer_guide.md` (weight_decay, early stopping)
- **Wrong activations/losses**: `full_DNN.md` (decision trees)

---

## 📋 **QUICK REFERENCE TABLES**

| Topic | File | Key Content |
|-------|------|-------------|
| **Model architectures** | `full_DNN.md` | Binary/multi-class/regression templates |
| **Sequential, BatchNorm, Dropout** | `sequential_batchnorm_dropout.md` | Modern neural network building blocks |
| **CNN building** | `CNN_guide.md` | Conv2d, pooling, channels explanation |
| **Data loading** | `data_preprocessing_tutorial.md` | Dataset → DataLoader pipeline |
| **Dataset vs DataLoader** | `dataset_vs_dataloader.md` | Core data pipeline concepts |
| **Optimizers** | `optimizer_guide.md` | Adam/SGD parameters & tuning |
| **Dimensions** | `pytorch_dimensions_for_noobs.md` | Shape conventions & debugging |
| **Complete examples** | `CNN_pipeline_examples.md` | End-to-end CNN pipelines |
| **Advanced DNN examples** | `complete_dnn_examples.md` | Full binary/multi-class/regression pipelines |
| **Advanced CNN examples** | `complete_cnn_examples.md` | Modern CNN with Grad-CAM, deployment |
| **From scratch code** | `optimizers_from_scratch_tutorial.md` | SGD/Adam implementations |

---

## 🚀 **LEARNING PATH**

**Start here if you're new:**
1. `one_neuron.md` → Understand single neuron learning
2. `stacking.md` → How layers stack to form DNNs
3. `pytorch_dimensions_for_noobs.md` → Master tensor shapes
4. `full_DNN.md` → Build your first complete DNN
5. `data_preprocessing_tutorial.md` → Learn data loading
6. `CNN_guide.md` → Move to CNNs for images
7. `optimizer_guide.md` → Tune training performance

**For specific problems:**
- **Images?** → `CNN_guide.md` + `CNN_pipeline_examples.md`
- **Tabular data?** → `full_DNN.md` + `data_preprocessing_tutorial.md`
- **Custom optimizers?** → `optimizers_from_scratch_tutorial.md`
- **Dimension issues?** → `pytorch_dimensions_for_noobs.md`

---

## 🔍 **SEARCH BY KEYWORD**

**Keywords → Files:**
- `fc1, fc2, fc3` → `pytorch_dimensions_for_noobs.md` (layer naming)
- `batch_size, channels, height, width` → `pytorch_dimensions_for_noobs.md`
- `Conv2d, MaxPool2d` → `CNN_guide.md`
- `Sequential, BatchNorm, Dropout` → `sequential_batchnorm_dropout.md`
- `Adam, SGD, momentum` → `optimizer_guide.md` or `optimizers_from_scratch_tutorial.md`
- `ReLU, Sigmoid, CrossEntropyLoss` → `full_DNN.md` or `activation_loss_optimizer_examples.md`
- `train_test_split, StandardScaler` → `data_preprocessing_tutorial.md`
- `view(), unsqueeze(), squeeze()` → `pytorch_dimensions_for_noobs.md`
- `MNIST, CIFAR-10` → `CNN_pipeline_examples.md` or `complete_cnn_examples.md`
- `weight_decay, learning rate` → `optimizer_guide.md`
- `loan default, binary classification` → `complete_dnn_examples.md`
- `Grad-CAM, model interpretation` → `complete_cnn_examples.md`
- `complete pipeline, end-to-end` → `complete_dnn_examples.md` or `complete_cnn_examples.md`

---

**Total files: 14 | Topics covered: 60+ | Your complete PyTorch knowledge base! 🎯**</content>
<parameter name="filePath">/mnt/Data/3-2/330 (ML lab)/Online 2/cheatsheets/cheatsheets_master_index.md