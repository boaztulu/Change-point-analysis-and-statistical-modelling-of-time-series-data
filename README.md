# 📈 Brent Oil Price Change Point Detection

Welcome to the **Brent Oil Price Change Point Detection** project!  
This project analyzes log returns of Brent oil prices over time and detects **structural changes** using classical statistical modeling in Python with `statsmodels`.

---

## 🧠 Overview

This project:
- Loads and preprocesses Brent Oil historical price data.
- Computes **log returns**.
- Uses a **residual sum of squares (RSS)** minimization method to detect a single most likely **change point** in the data.
- Visualizes both the **log return series** and the **price trend**, marking the detected change point.

---

## 🗂️ Folder Structure


---

## 📦 Dependencies

To run this project, make sure you have the following Python packages installed:

```bash
Make sure your CSV is structured like:

cs
Copy
Edit
Date,Price
2020-01-01,65.37
2020-01-02,66.02
...
⚙️ How It Works
Load and sort data by date

Compute log returns:

𝑟
𝑡
=
log
⁡
(
𝑃
𝑡
)
−
log
⁡
(
𝑃
𝑡
−
1
)
r 
t
​
 =log(P 
t
​
 )−log(P 
t−1
​
 )
Try every possible change point (except the edges), split data into two segments

Fit linear models (OLS) to both segments and calculate the total RSS

Choose the change point with the minimum total RSS

Plot log returns and price trends with the detected change point

📈 Example Output
🔴 Detected Change Point Index: best_tau

📅 Estimated Date: e.g., 2022-06-15

A vertical dashed red line will appear in the time series plot showing the point of structural change.

📌 Key Files
File	Description
BrentOilPrices.csv	Input dataset of daily Brent oil prices
analysis.ipynb	Main notebook performing data loading, modeling, and plotting
README.md	This documentation file

📸 Sample Plot

🚀 Getting Started
Clone the repo and start exploring:

bash
Copy
Edit
git clone https://github.com/your-username/brent-change-point.git
cd brent-change-point
Open the Jupyter Notebook:

bash
Copy
Edit
jupyter notebook notebook/analysis.ipynb
📬 Feedback & Contributions
Feel free to:

💬 Open issues for bugs or feature requests

🌱 Submit a pull request to improve or extend the model

📜 License
This project is licensed under the MIT License.
