#!/bin/bash

# Database Deployment Setup Script
# This script helps prepare your database for deployment

echo "🗄️  Database Deployment Setup"
echo "=============================="
echo ""

# Check if database exists
if [ -f "db/customer_support.db" ]; then
    echo "✅ Database already exists at: db/customer_support.db"
    
    # Show database info
    echo ""
    echo "📊 Database contents:"
    echo "-------------------"
    sqlite3 db/customer_support.db "SELECT COUNT(*) || ' customers' FROM customers;"
    sqlite3 db/customer_support.db "SELECT COUNT(*) || ' orders' FROM orders;"
    sqlite3 db/customer_support.db "SELECT COUNT(*) || ' logistics entries' FROM logistics;"
    echo ""
else
    echo "❌ Database not found. Creating new database..."
    python3 -c "from db.database_setup import create_database; create_database()"
    echo ""
fi

echo "📋 Deployment Options:"
echo "---------------------"
echo ""
echo "Option 1: Commit database to Git (Quick & Simple)"
echo "  → Database will deploy with your code"
echo "  → Good for: Testing, demos, small apps"
echo "  → Run: ./deploy_with_db.sh"
echo ""
echo "Option 2: Auto-generate on each deploy"
echo "  → Database creates automatically on startup"
echo "  → Good for: Development, testing with fresh data"
echo "  → No action needed - already configured!"
echo ""
echo "Option 3: Use managed PostgreSQL (Production)"
echo "  → Best for: Real production apps"
echo "  → See: DATABASE_DEPLOYMENT.md for migration guide"
echo ""

read -p "Do you want to commit the database to Git? (y/n): " answer

if [ "$answer" = "y" ]; then
    echo ""
    echo "🔧 Preparing database for Git..."
    
    # Check if .gitignore excludes db files
    if grep -q "db/\*\.db" .gitignore; then
        echo "📝 Updating .gitignore to include database..."
        # Create backup
        cp .gitignore .gitignore.backup
        
        # Remove db/*.db exclusion
        sed -i.tmp '/^db\/\*\.db$/d' .gitignore
        sed -i.tmp '/^db\/\*\.sqlite$/d' .gitignore
        sed -i.tmp '/^db\/\*\.sqlite3$/d' .gitignore
        rm .gitignore.tmp
        
        echo "✅ Updated .gitignore"
    fi
    
    echo ""
    echo "📦 Git commands to run:"
    echo "  git add db/customer_support.db"
    echo "  git add .gitignore"
    echo "  git commit -m 'Add production database'"
    echo "  git push"
    echo ""
    echo "Would you like me to run these commands? (y/n): "
    read run_git
    
    if [ "$run_git" = "y" ]; then
        git add db/customer_support.db
        git add .gitignore
        git commit -m "Add production database with sample data"
        echo ""
        echo "✅ Database committed! Push to deploy:"
        echo "   git push origin main"
    fi
else
    echo ""
    echo "✅ Database will auto-generate on deployment"
    echo "   No changes needed - database creates automatically!"
fi

echo ""
echo "🚀 Ready to deploy! Check DEPLOYMENT.md for platform-specific instructions."
