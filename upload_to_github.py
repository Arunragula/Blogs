# Script to upload blogs to GitHub
import os

# Git commands to add, commit, and push changes
os.system("git add posts/")
os.system(f'git commit -m "🤖 Auto-generated blog for $(date +\'%Y-%m-%d\')"')
os.system("git push")
