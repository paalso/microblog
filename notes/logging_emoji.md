# Emoji Logging Reference Guide


## 📘 Contents

- [General Tips](#general-tips)
- [CRUD Operations](#crud-operations)
- [Authentication & Security](#authentication--security)
- [Database Events](#database-events)
- [Requests & Routing](#requests--routing)
- [System & Application Lifecycle](#system--application-lifecycle)
- [Background Tasks & Workers](#background-tasks--workers)
- [Warnings & Errors](#warnings--errors)
- [Performance & Monitoring](#performance--monitoring)
- [Misc Useful Emojis](#misc-useful-emojis)
- [Example Log Messages](#example-log-messages)
- [Recommended Usage Patterns](#recommended-usage-patterns)

---

## General Tips

✔ Emojis should be placed *before* the message  
✔ Keep the rest of the text clean and structured  
✔ Use emojis consistently per category  
✔ Prefer simple, monochrome emojis for production logs

Example:

```python
app.logger.info(f"🆕 User created: {user.username}")
```

### [CRUD Operations](#crud-operations)

| Operation | Emoji     | Description                     |
| --------- | --------- | ------------------------------- |
| Create    | 🆕 ✨ 🟢   | New record / resource created   |
| Read      | 📄 📘     | Reading object, showing details |
| Update    | ✏️ 📝 🔧  | Updated fields or config        |
| Delete    | 🗑 🗑️‍💥 | Removed object                  |
| List      | 📋 📜     | Listing items                   |

### [Authentication & Security](#authentication--security)

| Event             | Emoji  | Description                    |
| ----------------- | ------ | ------------------------------ |
| Login             | 🔐 🔑  | Successful login               |
| Logout            | 🔓     | Logout event                   |
| Token issued      | 🪙 🔏  | JWT or session token generated |
| Invalid token     | 🚫🔑   | Failed token validation        |
| Permission denied | 🔒 🚫  | Missing rights                 |
| Auth warning      | 🛑 ⚠️  | Suspicious auth behavior       |
| Security alert    | 🛡️ 🚨 | High-severity event            |

### [Database Events](#database-events)

| Event                | Emoji | Description         |
| -------------------- | ----- | ------------------- |
| Query executed       | 💽 🔍 | DB query started    |
| Data saved           | 💾 🗄 | Commit successful   |
| Transaction rollback | 🔁 ⛔  | Rollback            |
| Slow query           | 🐌 ⏱  | Query took too long |
| Connection issue     | 🧯 🚨 | DB errors           |

### [Requests & Routing](#requests--routing)

| Event           | Emoji        | Description           |
| --------------- | ------------ | --------------------- |
| Request started | 📥 🌍        | Incoming HTTP request |
| Response sent   | 📤 📨        | Completed response    |
| Routing info    | 🧭           | Route called          |
| Redirect        | 🔀 ➡️        | Redirection occurred  |
| Client error    | 🚫 4️⃣0️⃣4️⃣ | 404, 403, bad input   |
| Server error    | 💥 5️⃣0️⃣0️⃣ | Internal failure      |


## [System & Application Lifecycle](#system--application-lifecycle)

| Event              | Emoji | Description          |
| ------------------ | ----- | -------------------- |
| App started        | 🟢 🚀 | Application boot     |
| App shutting down  | 🛑 🔻 | Graceful shutdown    |
| Hot reload         | ♻️    | Code reload (debug)  |
| Config loaded      | ⚙️ 🧩 | Settings initialized |
| Migration executed | 🧱 🔨 | Database migrations  |


### [Background Tasks & Workers](#background-tasks--workers)

| Event          | Emoji | Description           |
| -------------- | ----- | --------------------- |
| Task started   | ⏳     | Background job queued |
| Task finished  | ✅ ✔️  | Finished successfully |
| Worker started | ⚙️ 🏭 | Worker online         |
| Worker stopped | 🔻 🛑 | Worker shutdown       |
| Retry          | 🔁    | Retrying task         |
| Task failed    | 💥 🚫 | Job crashed           |

#### [Warnings & Errors](#warnings--errors)

| Level    | Emoji    | Description          |
| -------- | -------- | -------------------- |
| Debug    | 🐞 🔧    | Debug-level messages |
| Info     | ℹ️ 🛈    | Informational        |
| Warning  | ⚠️ 🔶    | Non-critical issue   |
| Error    | ❌ 🚫     | Recoverable error    |
| Critical | 💥 🔥 🚨 | Severe failure       |

### [Performance & Monitoring](#performance--monitoring)

| Event        | Emoji | Description         |
| ------------ | ----- | ------------------- |
| Latency      | ⏱     | Slow response       |
| Memory issue | 🧠⚠️  | Memory usage high   |
| CPU load     | 🧮🔥  | CPU spike           |
| Cache hit    | 🟩 📦 | Cache success       |
| Cache miss   | 🟥 📦 | Fetch fallback      |
| Job timeout  | ⌛ 🛑  | Operation timed out |


#### [Misc Useful Emojis](#misc-useful-emojis)

| Category          | Emoji    | Notes                       |
| ----------------- | -------- | --------------------------- |
| Networking        | 🌐 📡 🚦 | Requests, sockets           |
| File ops          | 📁 📂 📄 | File creation/loading       |
| Email             | ✉️ 📧    | SMTP events                 |
| Success highlight | 🎉 🌟    | Mark completed achievements |
| UX actions        | 🖱️ 📱   | Client events               |
| Data processing   | 📊 📈    | Analytics                   |

## [Example Log Messages](#example-log-messages)

```python
app.logger.info(f"🆕 User created: {user.username}")

app.logger.warning(
    f"🚫 Unauthorized delete attempt by {current_user.id} on {item.id}"
)

app.logger.error(
    f"💥 Database failure while saving order {order_id}"
)

app.logger.debug(
    f"🔍 Query details: {query} took {duration:.2f} ms"
)

app.logger.info(
    f"📥 Request from {request.remote_addr} → {request.path}"
)
```

## [Recommended Usage Patterns](#recommended-usage-patterns)

1. Use emojis sparingly in production logs.
2. For development, emojis are excellent for highlighting categories.
3. Use consistent emoji per event type.
4. Combine emojis with structured log fields (JSON) if using Loki/Grafana.
