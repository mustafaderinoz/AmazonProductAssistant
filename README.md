# 🛒 Amazon Product Assistant

An AI-powered Amazon product search and evaluation application. It provides a modern UI built with **Streamlit**, collects data from **Amazon using Selenium**, and performs intelligent tasks such as keyword generation, best product selection, and user review summarization using the **Google Gemini 2.5 Flash API**.

---

## 🚀 Features

* 🔎 **Keyword generation (Gemini)** — Converts natural language user queries into short Amazon-compatible search keywords
* 🛒 **Amazon product scraping (Selenium)** — Extracts title, price, rating, review count, image, and product link
* 🧠 **Best product selection using Gemini 2.5 Flash API**
* ✨ **AI-powered review analysis and summarization**
* 🎨 **Modern Streamlit + CSS interface** (custom buttons, headers, inputs, layout styling)
* ⚠️ **Error/exception handling for Amazon scraping** + automatic chromedriver installation

---

## 🛠️ Technologies Used

| Technology                                                                                             | Description                           |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------- |
| <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white">          | Main programming language             |
| <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white">    | Web interface                         |
| <img src="https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=selenium&logoColor=white">      | Web scraping / automation             |
| <img src="https://img.shields.io/badge/chromedriver--autoinstaller-0A0A0A?style=flat">                 | Automatic chromedriver installation   |
| <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat&logo=google&logoColor=white"> | AI model (text generation & analysis) |
| <img src="https://img.shields.io/badge/python--dotenv-4E9A06?style=flat">                              | .env management (API keys)            |

---

## 📦 Project Structure

```
📦 amazon-assistant
│
├── main.py               # Streamlit UI and application flow
├── AmazonScraper.py      # Selenium-based Amazon scraping module
├── GeminiApi.py          # Google Gemini integration (keywords, selection, summary)
├── requirements.txt      # Required Python dependencies
├── .env                  # API keys (API_KEY)
├── screenshots/          # UI screenshots
└── README.md
```

---

## 🛠️ Installation & Setup

### 1️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

### 2️⃣ Activate the Virtual Environment

```bash
# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3️⃣ Install Required Libraries

If `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

If no requirements file is available, install the packages manually:

```bash
pip install streamlit selenium chromedriver-autoinstaller google-generativeai python-dotenv
```

> Note: `chromedriver-autoinstaller` automatically installs the correct ChromeDriver version. On servers/CI environments, headless mode and extra system dependencies (e.g., libnss, xvfb) may be required.

### 🔑 Add API Key

Create a file named `.env` in the project root directory and add:

```bash
API_KEY="YOUR_API_KEY"
```

This is your Google Gemini / Generative AI API key.

---

### ▶️ Run the Application

```bash
streamlit run main.py
```

---

## 📱 Screenshots

|                                |
| ------------------------------ |
| ![UI](screenshots/amazon1.png) |

---

|                                |
| ------------------------------ |
| ![UI](screenshots/amazon2.png) |

---
