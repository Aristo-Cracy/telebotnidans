import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from io import BytesIO

TOKEN = "7786966143:AAHyWWfnc37KMeva8QEmVC4NIZUYjrX8AqY"

ALLOWED_USERS = [5218536687, 1624943836, 5191716250]  # Replace with real Telegram user IDs

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ Access denied.")
        return
    await update.message.reply_text("Send me a 9 or 10-digit Test ID (NID) to get the answer key.")

async def handle_nid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ You are not authorized to use this bot.")
        return

    nid = update.message.text.strip()
    if not nid.isdigit() or not (9 <= len(nid) <= 10):
        await update.message.reply_text("❌ Please send a valid 9 or 10-digit Test ID.")
        return

    await update.message.reply_text("⏳ Fetching data...")
    try:
        q_meta = requests.get(f"https://learn.aakashitutor.com/api/getquestionsforquiz?nid={nid}&noredirect=true").json()
        q_url = q_meta["url"].replace("\u0026", "&").replace("\", "")
        questions = requests.get(q_url).json()
        sols = requests.get(f"https://learn.aakashitutor.com/api/getquizresults?quiz_id={nid}").json()

        solutions = []
        for item in sols:
            for key in item:
                res = item[key].get("question_result")
                if res:
                    solutions.append({"nid": res["nid"], "answer": res["answer"]})

        rows = []
        count = 0
        for sol in solutions:
            if count >= 180:
                break
            q = next((x for x in questions if x["nid"] == sol["nid"]), None)
            if not q:
                continue
            opt, ans = "N/A", "Answer not found"
            if isinstance(q.get("alternatives"), list):
                alt = next((a for a in q["alternatives"] if a["id"] in sol["answer"]), None)
                if alt:
                    opt = f"{q['alternatives'].index(alt) + 1})"
                    ans = alt["answer"]
            else:
                ans = ", ".join(sol["answer"]) if isinstance(sol["answer"], list) else sol["answer"]
            rows.append(f"<tr><td>Q{count + 1}</td><td>{opt}</td><td>{ans}</td></tr>")
            count += 1

        html = f"""<html><head><title>Answer Key</title></head>
        <body style='font-family: Arial; text-align:center;'><h1>AESL Answer Key</h1>
        <table border='1' style='margin:auto; border-collapse:collapse;'>
        <tr><th>Q. No</th><th>Correct Option</th><th>Correct Answer</th></tr>
        {''.join(rows)}
        </table></body></html>"""

        file_bytes = BytesIO(html.encode("utf-8"))
        file_bytes.name = f"{nid}_answer_key.html"
        await update.message.reply_document(document=file_bytes)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_nid))
    app.run_polling()
