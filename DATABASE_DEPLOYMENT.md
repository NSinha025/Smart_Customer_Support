# Database Deployment Options

## Current Setup
Your app uses **SQLite** database (`customer_support.db`) which:
- ✅ Works great for development
- ✅ No setup required
- ✅ Auto-creates with sample data
- ⚠️  May not persist on free hosting (ephemeral storage)

## 🎯 Quick Fix: Commit Database to Git

If you want the database to deploy with your code:

```bash
# 1. Remove db/*.db from .gitignore
# Edit .gitignore and delete these lines:
# db/*.db
# db/*.sqlite  
# db/*.sqlite3

# 2. Generate the database locally
python3 -c "from db.database_setup import create_database; create_database()"

# 3. Commit the database
git add db/customer_support.db
git commit -m "Add production database with sample data"
git push

# 4. Deploy as normal
```

**Result:** Your database will now deploy with your code and persist across deployments.

## 📊 Understanding Ephemeral vs Persistent Storage

| Platform | File System | Database Persistence |
|----------|-------------|---------------------|
| **Render** | Ephemeral* | Resets on sleep/restart |
| **Railway** | Ephemeral* | Resets on redeploy |
| **Fly.io** | Ephemeral | Resets unless using volumes |
| **PythonAnywhere** | Persistent | ✅ Files persist |

*Can add persistent volumes (may require paid plan)

## 🚀 For Production: Migrate to PostgreSQL

For a real production app, upgrade to PostgreSQL:

### Why PostgreSQL?
- ✅ Better for concurrent users
- ✅ Hosted database services (free tiers available)
- ✅ True persistence
- ✅ Backups and reliability

### Quick Migration Steps:

1. **Install PostgreSQL adapter:**
```bash
pip install psycopg2-binary
pip freeze > requirements.txt
```

2. **Create free PostgreSQL database:**
   - **Render:** Built-in PostgreSQL (free tier: 90 days)
   - **Railway:** Free PostgreSQL with $5 credit
   - **Supabase:** Free PostgreSQL, 500MB
   - **ElephantSQL:** Free tier, 20MB

3. **Update database connection in code** (I can help with this if needed)

4. **Migrate data:**
```bash
# Export from SQLite
sqlite3 db/customer_support.db .dump > data.sql

# Import to PostgreSQL (adjust connection details)
psql $DATABASE_URL < data.sql
```

## ✅ Recommended Approach

**For quick deployment/testing:**
- Commit the SQLite database to Git (easiest)

**For production app:**
- Use managed PostgreSQL database
- Keep SQLite for local development

## Need Help Migrating?

Let me know and I can:
1. Update the code to support PostgreSQL
2. Create migration scripts
3. Set up database environment variables
