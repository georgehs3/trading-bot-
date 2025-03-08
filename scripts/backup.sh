#!/bin/bash

set -e  # Stop script execution if any command fails

echo "📦 Starting Daily Backup Process..."

# Load environment variables
source .env

# Define backup directory and file name
BACKUP_DIR="/var/backups/trading_bot"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
POSTGRES_BACKUP_FILE="$BACKUP_DIR/postgres_backup_$TIMESTAMP.sql"
MONGO_BACKUP_FILE="$BACKUP_DIR/mongo_backup_$TIMESTAMP.gz"

# Ensure backup directory exists
mkdir -p $BACKUP_DIR

# PostgreSQL Backup
echo "🔄 Backing up PostgreSQL Database..."
pg_dump $DATABASE_URL > $POSTGRES_BACKUP_FILE

# MongoDB Backup
echo "🔄 Backing up MongoDB Database..."
mongodump --uri="$MONGO_URI" --archive=$MONGO_BACKUP_FILE --gzip

# Upload to Oracle Cloud Object Storage
echo "☁️ Uploading Backup to Oracle Cloud..."
oci os object put --bucket-name trading-bot-backups --file $POSTGRES_BACKUP_FILE
oci os object put --bucket-name trading-bot-backups --file $MONGO_BACKUP_FILE

# Cleanup old backups (keep last 7 days)
echo "🧹 Cleaning up old backups..."
find $BACKUP_DIR -type f -mtime +7 -exec rm {} \;

echo "✅ Backup Process Completed Successfully!"

