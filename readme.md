# Chat with Excel

A conversational Excel data analysis assistant that lets you upload Excel files (`.xlsx`), ask natural language questions about your data, and get insightful answers (including visualizations!).  
---


## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/Avinashbabue/Chat-with-Excel.git
   cd Chat-with-Excel
   ```

2. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Together API key**  
   Create a `.env` file:
   ```
   TOGETHER_API_KEY=your_together_api_key
   ```

---

## Run

```bash
streamlit run app.py
```

---

## Notes

- Your API key is required for LLM-powered answers.
---


