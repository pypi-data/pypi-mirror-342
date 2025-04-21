#!/bin/bash

# Hardcoded source and target organizations
SOURCE_ORG="arot-devs"
TARGET_ORG="troph-team"

# Default branches
SOURCE_BRANCH="main"
DEST_BRANCH="integration"

# List of repositories to clone
REPOSITORIES=( "procslib" "aeslib" "trainlib" )
# REPOSITORIES=( "repo1" "repo2" "repo3" )  # Modify or extend this list as needed

# Temporary directory for cloning
TMP_DIR="/tmp/cloned_repos"
mkdir -p "$TMP_DIR"

for REPO in "${REPOSITORIES[@]}"; do
    SRC_REPO_URL="https://github.com/$SOURCE_ORG/$REPO"
    TARGET_REPO_URL="https://github.com/$TARGET_ORG/$REPO"
    REPO_DIR="$TMP_DIR/$REPO"
    
    echo "Processing repository: $REPO"
    
    # Check if the target repository exists
    if ! git ls-remote "$TARGET_REPO_URL" &>/dev/null; then
        echo "Target repository $TARGET_REPO_URL does not exist. Attempting to create it..."
        
        # Ensure GitHub CLI (gh) is installed
        if ! command -v gh &>/dev/null; then
            echo "GitHub CLI (gh) is not installed. Please install it and authenticate before retrying. Skipping..."
            continue
        fi
        
        # Create the repository using GitHub CLI
        gh repo create "$TARGET_ORG/$REPO" --private --confirm
        
        # Verify creation
        if ! git ls-remote "$TARGET_REPO_URL" &>/dev/null; then
            echo "Failed to create repository $TARGET_REPO_URL. Skipping..."
            continue
        fi
        echo "Repository $TARGET_REPO_URL created successfully."
    fi
    
    # Remove existing temp directory if it exists
    if [ -d "$REPO_DIR" ]; then
        echo "Removing existing directory $REPO_DIR"
        rm -rf "$REPO_DIR"
    fi
    
    # Clone the target repository
    echo "Cloning $TARGET_REPO_URL..."
    git clone "$TARGET_REPO_URL" "$REPO_DIR"
    cd "$REPO_DIR" || exit 1
    
    # Add the source repo as a remote and fetch changes
    echo "Adding source repo $SRC_REPO_URL as remote..."
    git remote add source_repo "$SRC_REPO_URL"
    git fetch source_repo
    
    # Checkout or create the destination branch
    echo "Switching to branch $DEST_BRANCH..."
    git checkout -B "$DEST_BRANCH"
    
    # Reset the repo to match the source repo
    echo "Resetting target repo to match source repo..."
    git reset --hard source_repo/$SOURCE_BRANCH
    
    # Perform a full-text replacement of the source organization with the target organization
    echo "Updating all occurrences of $SOURCE_ORG with $TARGET_ORG..."
    find . -type f -exec sed -i "s|$SOURCE_ORG|$TARGET_ORG|g" {} +
    
    # Commit changes if there are any
    if git status --porcelain | grep -q .; then
        echo "Committing updated files..."
        git add .
        git commit -m "Updating references from $SOURCE_ORG to $TARGET_ORG"
    fi
    
    # Push changes to the selected branch
    echo "Pushing changes to $TARGET_REPO_URL branch $DEST_BRANCH..."
    git push -f origin "$DEST_BRANCH"
    
    echo "Update complete for repository: $REPO"
    echo "--------------------------------------------------"
    cd "$TMP_DIR"
done

echo "All repositories processed successfully."
