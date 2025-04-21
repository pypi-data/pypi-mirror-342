#!/bin/bash

# Paths and repository URLs
DEV_REPO="https://github.com/arot-devs/procslib"
TROPH_REPO="https://github.com/troph-team/procslib"
TMP_DIR="/tmp/procslib_troph"

# Clone the troph-team repository
if [ -d "$TMP_DIR" ]; then
    echo "Removing existing temp directory"
    rm -rf "$TMP_DIR"
fi
echo "Cloning troph-team repo..."
git clone "$TROPH_REPO" "$TMP_DIR"
cd "$TMP_DIR" || exit 1

# Add the dev_repo as a remote and fetch its changes
echo "Adding and fetching from dev_repo..."
git remote add dev_repo "$DEV_REPO"
git fetch dev_repo

# Reset the troph-team repo to match dev_repo
echo "Resetting troph-team repo to match dev_repo..."
git checkout -b main
git reset --hard dev_repo/main

# Update CHANGELOG.md to replace DEV_REPO mentions with TROPH_REPO
CHANGELOG_FILE="CHANGELOG.md"
if [ -f "$CHANGELOG_FILE" ]; then
    echo "Updating $CHANGELOG_FILE to replace $DEV_REPO with $TROPH_REPO..."
    sed -i "s|$DEV_REPO|$TROPH_REPO|g" "$CHANGELOG_FILE"
fi

# Commit updated CHANGELOG.md if changes were made
if git status --porcelain | grep -q "$CHANGELOG_FILE"; then
    echo "Committing updated $CHANGELOG_FILE..."
    git add "$CHANGELOG_FILE"
    git commit -m "updating changelog to match repo"
fi

# Force push the reset state to the troph-team repo
echo "Force pushing changes to troph-team..."
git push -f origin main

echo "Update complete. The troph-team repo now matches the arot-devs repo, with CHANGELOG.md updated."
