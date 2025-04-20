import matplotlib.pyplot as plt
import seaborn as sns

def plot_r2_evolution(model_names, r2_scores, path="r2_evolution.png"):
    plt.figure(figsize=(12, 6))
    plt.plot(model_names, r2_scores, marker='o')
    plt.xticks(rotation=90)
    plt.title("R² Evolution")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def plot_heatmap(results_df, path="heatmap.png"):
    plt.figure(figsize=(10, 6))
    sns.heatmap(results_df, annot=True, fmt=".2f", cmap="YlGnBu")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def plot_barplot(results_df, metric="test_mae", path="bar_plot.png"):
    plt.figure(figsize=(14, 6))
    sns.barplot(x=results_df.index, y=results_df[metric], palette="viridis")
    plt.xticks(rotation=90)
    plt.title(f"{metric} - Bar Plot")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def plot_violin(results_df, metric="r2", path="violin_plot.png"):
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=results_df[[metric]], inner="point", color="skyblue")
    plt.title(f"{metric} Distribution - Violin Plot")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()