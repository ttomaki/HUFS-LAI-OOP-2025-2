#!/bin/bash

# Usage: ./oop-ass2-grade.sh <git_url> <student_id>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <git_url> <student_id>"
    echo "Example: $0 https://github.com/hist0613/HUFS-LAI-OOP-2025-2 2025122"
    exit 1
fi

GIT_URL="$1"
STUDENT_ID="$2"

# Extract branch name if URL contains /tree/
if [[ "$GIT_URL" =~ /tree/([^/]+)$ ]]; then
    BRANCH="${BASH_REMATCH[1]}"
    # Remove /tree/branch from URL to get base repository URL
    REPO_URL="${GIT_URL%/tree/*}"
    echo "Cloning repository: $REPO_URL (branch: $BRANCH)"
    git clone -b "$BRANCH" "$REPO_URL" test
else
    echo "Cloning repository: $GIT_URL"
    git clone "$GIT_URL" test
fi

if [ $? -ne 0 ]; then
    echo "Error: Failed to clone repository"
    exit 1
fi

# Create target directory structure
TARGET_DIR="test/submissions/$STUDENT_ID/assignment2"
mkdir -p "$TARGET_DIR"

# Copy grader.py from the cloned repository
SOURCE_GRADER="HUFS-LAI-OOP-2025-2/submissions/2025122/assignment2/grader.py"
if [ -f "$SOURCE_GRADER" ]; then
    cp "$SOURCE_GRADER" "$TARGET_DIR/"
    echo "Copied grader.py to $TARGET_DIR/"
else
    echo "Error: grader.py not found at $SOURCE_GRADER"
    exit 1
fi

# Change to target directory and run grader.py
cd "$TARGET_DIR"
echo "Running grader.py in $TARGET_DIR"
python3 grader.py

# Clean up: remove the test directory
cd ~  # Go back to workspace root
rm -rf test
echo "Cleaned up test directory"
