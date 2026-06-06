# 📅 Notion Tasks → Apple Calendar

همگام‌سازی خودکار کارهای Notion با Apple Calendar — کاملاً رایگان

---

## راه‌اندازی (یک‌بار انجام میشه)

### مرحله ۱ — ساخت Notion Integration Token

1. برو به [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. روی **New integration** کلیک کن
3. یه اسم بده (مثلاً `calendar-sync`) و **Submit**
4. **Internal Integration Secret** رو کپی کن

### مرحله ۲ — دادن دسترسی به Database

1. در Notion، وارد صفحه‌ای که database "کارها" توشه بشو
2. بالا سمت راست: **...** → **Connections** → Integration خودت رو اضافه کن

### مرحله ۳ — ساخت Repository در GitHub

1. یه repo جدید بساز (مثلاً `notion-calendar`)
2. فایل‌های این پروژه رو آپلود کن:
   - `notion_to_ics.py` (در root)
   - `.github/workflows/sync.yml`
3. یه folder به اسم `docs` بساز و یه فایل خالی `docs/.gitkeep` بذار توش

### مرحله ۴ — اضافه کردن Secret

1. در GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**:
   - Name: `NOTION_TOKEN`
   - Secret: توکنی که از Notion کپی کردی

### مرحله ۵ — فعال کردن GitHub Pages

1. **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / folder: `/docs`
4. Save

بعد چند دقیقه آدرسی مثل این داری:
```
https://USERNAME.github.io/notion-calendar/tasks.ics
```

### مرحله ۶ — Subscribe در Apple Calendar

**روی iPhone/iPad:**
1. Settings → Calendar → Accounts → Add Account → Other
2. **Add Subscribed Calendar**
3. آدرس `.ics` بالا رو paste کن
4. هر چقدر میخوای refresh interval بذار

**روی Mac:**
1. Calendar → File → New Calendar Subscription
2. آدرس `.ics` رو وارد کن
3. Auto-refresh: Every 15 minutes

---

## چطور کار میکنه؟

```
هر ۱۵ دقیقه:
GitHub Actions → Notion API → tasks.ics → GitHub Pages → Apple Calendar
```

- فقط کارهایی sync میشن که **انجام‌نشده** و **تاریخ** دارن
- ایموجی‌ها: 💼 کسب‌وکار | 🎓 University | 👤 شخصی | 🐍 Python
- Apple Calendar هر بار که باز کنی یا طبق schedule، sync میشه

---

## هزینه

**صفر** — GitHub Free Plan شامل ۲۰۰۰ دقیقه Actions در ماهه که خیلی بیشتر از نیازته.
