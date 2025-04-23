# ot-grn

**Double Optimal Transport for Differential Gene Regulatory Network Inference with Unpaired Samples**

`ot-grn` is a Python library designed to infer differential gene regulatory networks (GRNs) from gene expression data using optimal transport (OT) theory, applicable to unpaired samples. The library implements a robust and scalable framework, named Double OT, that integrates OT at the gene and sample levels to reconstruct GRNs effectively.

---

## Features

- **Data Preparaion**: Generate simulated datasets; load real-world gastric cancer gene expression data.
- **Network Inference**: Use the Double OT method to align unpaired samples and infer regulatory relationships.
- **Evaluation and Interpretation**: Evaluate the inferred network using metrics like AUROC, AUPR, and early precision; extract key regulatory edges and genes from the inferred network.

---

## Installation

You can install the library via pip:

```bash
pip install ot-grn
```

To install from source:

```bash
git clone https://github.com/Mengyu8042/ot-grn.git
cd ot-grn
pip install .
```

---

## Quick Start

### 1. Simulation Studies

```python
from ot_grn import generate_simulated_data, double_ot, evaluate_grn_accuracy

# (i) Generate synthetic normal and tumor expression data
exp1, exp2, true_plan = generate_simulated_data(p=500, n=100, diffgene=0.2, indegree=5)

# (ii) Infer differential GRN using Double OT method
ot_plan = double_ot(exp1, exp2)

# (iii) Calculate evaluation metrics for the inferred GRN
auroc, aupr, ep = evaluate_grn_accuracy(true_plan, ot_plan)
print(f"AUROC: {auroc}, AUPR: {aupr}, Early Precision: {ep}")
```

### 2. Real Data Analyses

```python
from ot_grn import load_gastric_cancer_data, double_ot, extract_top_edges

# (i) Load normal and tumor expression data from gastric cancer patients
exp1, exp2 = load_gastric_cancer_data(same_source=True, paired=True)

# (ii) Infer differential GRN using Double OT method
ot_plan = double_ot(exp1, exp2)

# (iii) Extract top regulatory edges and key genes
gene_names = exp1.index.tolist()
top_edges, key_genes = extract_top_edges(ot_plan, gene_names, num=500)
print(top_edges)
print(key_genes)
```
---

## Documentation

### Core Functions

1. **`generate_simulated_data`**
   - Generates simulated datasets for testing GRN inference methods.
   - Parameters: 
       - `p`: Number of genes.
       - `n`: Number of samples.
       - `diffgene` (optional): Proportion of differentially expressed genes, by default 0.2.
       - `indegree` (optional): Expected number of parents for differential genes, by default 5.
       - `snr` (optional): Signal-to-noise ratio, by default 2.
       - `outlier_ratio` (optional): Proportion of outliers, by default 0.
   - Returns: Normal expression matrix, tumor expression matrix, and true regulatory relationships.

2. **`load_gastric_cancer_data`**
   - Loads gastric cancer gene expression data from the same or different sources.
   - Parameters: 
      - `same_source` (optional): If True, normal and tumor samples are from the same source, by default True.
      - `paired` (optional): Only relevant if `same_source` is True. If True, samples are paired, by default True. 
   - Returns: Normal and tumor expression matrices.

3. **`double_ot`**
   - Implements the Double OT method for differential GRN inference.
   - Parameters: 
      - `exp1`: Expression matrix for condition 1 (e.g., normal state).
      - `exp2`: Expression matrix for condition 2 (e.g., tumor state).
      - `paired` (optional): If True, assumes the samples are paired. If False, uses partial OT to align samples, by default True.
      - `reg_m` (optional): Marginal relaxation hyperparameter for robust OT, by default 0.05.
      - `reg` (optional): Entropy regularization hyperparameter for partial OT and robust OT; either a scalar or a tuple (reg_pot, reg_rot), by default (0.005, 0.05).
      - `s` (optional): Transport budget in partial OT, by default None (min(n_samples1, n_samples2)).
      - `n_components` (optional): Number of principal components for PCA in sample alignment, by default None (all components).
      - `return_alignment` (optional): If True and samples are unpaired (`paired=False`), returns the sample alignment result (sample-level OT plan), by default False.
   - Returns: Gene-level OT plan (and sample-level OT plan).


4. **`evaluate_grn_accuracy`**
   - Calculate performance metrics for the inferred GRN.
   - Parameters: 
      - `y_true`: Ground truth binary labels (genes x genes).
      - `y_score`: Predicted scores (genes x genes).
   - Returns: AUROC, AUPR, Early Precision.

5. **`extract_top_edges`**
   - Extracts top regulatory edges and associated genes from the inferred GRN.
   - Parameters: 
      - `y_score`: Predicted scores (genes x genes).
      - `gene_names`: List of gene names.
      - `num`: Number of top edges to extract.
   - Returns: DataFrame of top edges and a list of connected genes.
---

## Dependencies

- Python 3.7 or higher
- `numpy`
- `scipy`
- `pandas`
- `scikit-learn`
- `pot` (Python Optimal Transport library)

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For questions, bug reports, or feature requests, please read our [Contribution Guide](CONTRIBUTING.md). If your issue is not covered there, feel free to open a GitHub issue in the repository.