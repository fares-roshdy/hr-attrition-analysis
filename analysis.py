"""HR Employee Attrition - exploratory data analysis.

Dataset: IBM HR Analytics Employee Attrition & Performance sample
(1,470 employees). Public dataset, source:
github.com/IBM/employee-attrition-aif360

Answers four questions:
1. Where is attrition concentrated (department, job role)?
2. Does overtime matter?
3. How does attrition move with age and income?
4. Which satisfaction scores separate leavers from stayers?
"""

import os

import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CHARTS = os.path.join(HERE, "charts")
os.makedirs(CHARTS, exist_ok=True)

plt.rcParams.update({"figure.dpi": 120, "axes.spines.top": False, "axes.spines.right": False})

df = pd.read_csv(os.path.join(HERE, "data", "WA_Fn-UseC_-HR-Employee-Attrition.csv"))
print("rows, cols:", df.shape)
df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)
overall = df["AttritionFlag"].mean()
print(f"overall attrition rate: {overall:.1%}")

# ---------- 1. attrition by job role ----------
role = df.groupby("JobRole")["AttritionFlag"].agg(["mean", "count"]).sort_values("mean")
print("\nattrition by job role:\n", role.assign(mean=(role["mean"] * 100).round(1)))

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(role.index, role["mean"] * 100, color="#2ca02c")
for i, v in enumerate(role["mean"] * 100):
    ax.text(v + 0.4, i, f"{v:.0f}%", va="center", fontsize=9)
ax.set_xlabel("Attrition rate (%)")
ax.set_title("Attrition rate by job role")
ax.set_xlim(0, max(role["mean"] * 100) * 1.2)
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "attrition_by_job_role.png"))
plt.close(fig)

# ---------- 2. overtime ----------
ot = df.groupby("OverTime")["AttritionFlag"].agg(["mean", "count"])
print("\nattrition by overtime:\n", ot.assign(mean=(ot["mean"] * 100).round(1)))

fig, ax = plt.subplots(figsize=(5.5, 4))
ax.bar(["No overtime", "Overtime"], ot["mean"] * 100, color=["#1f77b4", "#d62728"])
for i, v in enumerate(ot["mean"] * 100):
    ax.text(i, v + 0.6, f"{v:.0f}%", ha="center")
ax.set_ylabel("Attrition rate (%)")
ax.set_title("Overtime and attrition")
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "attrition_by_overtime.png"))
plt.close(fig)

# ---------- 3. age and income ----------
bins = [17, 25, 35, 45, 60]
labels = ["18-25", "26-35", "36-45", "46-60"]
df["AgeBand"] = pd.cut(df["Age"], bins=bins, labels=labels)
ab = df.groupby("AgeBand", observed=False)["AttritionFlag"].mean()

inc = df.groupby("Attrition")["MonthlyIncome"].median()
print("\nattrition by age band:\n", (ab * 100).round(1))
print("\nmedian monthly income by attrition:\n", inc)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].bar(labels, ab.values * 100, color="#ff7f0e")
for i, v in enumerate(ab.values * 100):
    axes[0].text(i, v + 0.5, f"{v:.0f}%", ha="center")
axes[0].set_ylabel("Attrition rate (%)")
axes[0].set_xlabel("Age band")
axes[0].set_title("Attrition by age band")
axes[1].hist(df.loc[df["AttritionFlag"] == 0, "MonthlyIncome"], bins=30, alpha=0.6,
             label="Stayed", color="#1f77b4")
axes[1].hist(df.loc[df["AttritionFlag"] == 1, "MonthlyIncome"], bins=30, alpha=0.6,
             label="Left", color="#d62728")
axes[1].set_xlabel("Monthly income ($)")
axes[1].set_ylabel("Employees")
axes[1].set_title("Income distribution")
axes[1].legend()
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "attrition_age_income.png"))
plt.close(fig)

# ---------- 4. satisfaction scores ----------
cols = ["JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction",
        "WorkLifeBalance"]
sat = df.groupby("Attrition")[cols].mean().T
print("\nmean satisfaction scores (1-4):\n", sat.round(2))

fig, ax = plt.subplots(figsize=(8, 4))
x = range(len(cols))
w = 0.35
ax.bar([i - w / 2 for i in x], sat["No"], width=w, label="Stayed", color="#1f77b4")
ax.bar([i + w / 2 for i in x], sat["Yes"], width=w, label="Left", color="#d62728")
ax.set_xticks(list(x), ["Job", "Environment", "Relationship", "Work-life balance"])
ax.set_ylabel("Mean score (1-4)")
ax.set_ylim(0, 4)
ax.set_title("Satisfaction scores: stayers vs leavers")
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "satisfaction_scores.png"))
plt.close(fig)

print("\ndone. charts in", CHARTS)
