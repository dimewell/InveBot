# InveBot on Render

### 🚀 Deploy Instructions

1. Push this project to GitHub.
2. Go to [Render.com](https://render.com).
3. Click **New + → Web Service** and connect your repo.
4. Build Command: leave empty.
5. Start Command: `python app/main.py`
6. Add environment variables in **Settings → Environment**:
   - `TELEGRAM_TOKEN`
   - `OPENAI_API_KEY`
   - `DATABASE_URL`
   - `ADMIN_ID`
7. Click **Deploy Web Service**.
