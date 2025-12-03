# 📈 Financial Analysis with Nasdaq Data Link API

# 📌 Project Overview
This project explores financial analysis by integrating with the **Nasdaq Data Link API**. The primary focus is to extract and analyze data from the `MER/F1` data table, which contains detailed metrics including balance sheets, cash flow statements, and income statements.

The core objective is to calculate and compare the **Accrued Expenses Turnover** across a specific set of companies and regions to understand their financial performance and operational efficiency over time.

# 🎯 Key Objectives
* **API Integration:** Automate the retrieval of financial data using Python and the Nasdaq API.
* **Data Cleaning:** Process raw JSON/CSV data into structured Pandas DataFrames.
* **Financial Metric Analysis:** Calculate the "Accrued Expenses Turnover" ratio.
* **Comparative Analysis:** Explore how this efficiency ratio differs among various companies.

# 🧠 Key Concept: Accrued Expenses Turnover
This project focuses heavily on the **Accrued Expenses Turnover** ratio, a key indicator of financial efficiency.

> **Formula:** *Cost of Goods Sold (or Operating Expenses) / Average Accrued Expenses*

We use this metric to evaluate:
1.  **Cash Flow Management:** Indicates how well a company manages cash flow relative to short-term obligations.
2.  **Operational Efficiency:** Reflects how promptly a company settles short-term debts.
3.  **Financial Health:** A strong indicator of creditworthiness and stability.

# 🛠️ Technologies & Tools
* **Python 3.x**
* **Pandas:** For data manipulation and aggregation.
* **Requests:** For handling API calls to Nasdaq Data Link.
* **Matplotlib / Seaborn:** For visualizing trends and comparisons.
* **Nasdaq Data Link API:** Source of the `MER/F1` financial dataset.

# 2) 🚀 Getting Started
In order to access Nasdaq API, it is necesary to create an API Key associated with an account.
These are the steps to generate an API Key:

1) Create an Account [here](https://data.nasdaq.com/sign-up)
2) Fill in your details, including your first name, last name, and email address.

3) Once you have the account ready, you should be able to find the API key in your Account Settings under your profile.

4) To keep your API key secure, especially when sharing your Jupyter Notebooks, store it in a separate Python file ( e.g., `config.py`) and import this file into your notebook.

``` Python
import config
api_key = config.API_KEY
```

With your API key in hand, the next task is determining the appropriate API endpoint and the parameters needed to query the financial data. For guidance on constructing your query, refer to the [Nasdaq Data Link API documentation](https://docs.data.nasdaq.com/docs/in-depth-usage-1).

## 2.1 📂 Data Source: Mergent Global Fundamentals (MER/F1)

**Overview**
The analysis relies on the **Mergent Global Fundamentals (MF1)** data feed. It provides fundamental indicators on publicly traded companies covered by the Russell Global Index.
* **Coverage:** 15,000+ companies across 67 countries.
* **History:** Financial statements dating back to 2005.
* **Update Frequency:** Data is updated daily at 02:30 AM UTC.
* **Focus:** Primary focus on U.S. traded companies filing with the SEC, with a reporting lag varying from 5 to 75 days depending on the filing method.

You can download the full list of covered companies [here](https://static.quandl.com/mergent/mergent-companies.csv).

### 📖 Data Dictionary
Below is the detailed schema of the dataset used in this project.

<details>
<summary><strong>Click to expand the full Column Definitions Table</strong></summary>

| **Column Name** | **Description** | **Type** |
|:---|:---|:---|
| **compnumber** | Internal company identifier; permanent and unique per company. | `integer` |
| **reportid** | Unique report period identifier per company/mapcode/date. | `integer` |
| **mapcode** | Identifier of a financial account. Used to map indicators. | `integer` |
| **amount** | The actual indicator value associated with the mapcode. | `decimal` |
| **reportdate** | Date of the financial report period. | `date` |
| **reporttype** | Type of report (e.g., Annual, Quarterly). | `string` |
| **auditorstatus**| Code indicating the audit status of the report. | `string` |
| **currency** | ISO currency code of the report. | `string` |
| **consolidated** | Indicates whether the report is consolidated ('TRUE'/'FALSE'). | `string` |
| **longname** | Official company name. | `string` |
| **shortname** | Common or abbreviated company name. | `string` |
| **status** | Company operating status (Active/Inactive). | `string` |
| **countrycode** | ISO country code of incorporation. | `string` |
| **cik** | SEC Central Index Key (Permanent numeric identifier). | `integer` |
| **mic** | Mergent industry classification code. | `string` |
| **ticker** | Stock ticker for the primary listing. | `string` |
| **exchange**

## 2.2📡 Methodology: API Interaction

To ensure precise data extraction, this project interacts with the `MER/F1` endpoint using specific filter parameters.

### Query Structure
The data was retrieved using the standard Nasdaq Data Link API structure:
`https://data.nasdaq.com/api/v3/datatables/MER/F1.json`

Key parameters used to filter the huge dataset included:

| Parameter | Value (Example) | Purpose |
| :--- | :--- | :--- |
| **mapcode** | `-5370` | Selects specific financial metrics (e.g., Accrued Expenses). |
| **compnumber** | `39102` | Filters for specific companies (e.g., Nokia). |
| **reporttype** | `A` | Restricts results to **Annual** reports. |
| **qopts.columns**| `reportdate,amount` | Optimizes the payload by requesting only necessary columns. |

### ⚡ Performance & Rate Limits
To ensure the stability of the extraction process, the script adheres to Nasdaq's API rate limits for authenticated users.

* **Constraint:** The script is designed to handle the limit of **2,000 calls per 10 minutes** (standard for free authenticated accounts).
* **Optimization:** By using the `.json` format and filtering columns (`qopts.columns`), we reduce the bandwidth and processing time for each request.

> **Note:** If you are running this without an API Key (anonymous mode), the limit drops drastically to 20 calls per 10 minutes. Using the `config.py` setup is highly recommended.
