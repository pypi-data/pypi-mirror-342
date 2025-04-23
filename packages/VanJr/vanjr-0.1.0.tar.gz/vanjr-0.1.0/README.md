# VanJr 📊🔥

**VanJr** is a Python library designed to simplify and accelerate data preprocessing, exploratory data analysis (EDA), and machine learning model development. Whether you're a beginner or an experienced data scientist, VanJr brings a clean, intuitive interface for working with datasets from start to finish.

---

## 🚀 Key Features

- 🧾 **Data Collection**: Load datasets from CSV, Excel, or URLs.
- 🔍 **EDA (Exploratory Data Analysis)**: Quick insights and visualizations.
- 🧹 **Data Cleaning**: Handle missing values, duplicates, and outliers.
- ⚙️ **Data Transformation**: Type conversion, encoding, scaling.
- 🧠 **Modeling**: Train/test split, train models, evaluate performance.
- ⚖️ **Balancing**: Fix imbalanced datasets with ease.
- 💾 **Save Results**: Export cleaned data to CSV or database.

---

## 🛠️ Installation

```bash
pip install VanJr


## Usage
```python
from VanJr import VanJr

vj = VanJr("your_dataset.csv")
vj.inspect()
vj.preprocess()
vj.train_model()
vj.evaluate_model()