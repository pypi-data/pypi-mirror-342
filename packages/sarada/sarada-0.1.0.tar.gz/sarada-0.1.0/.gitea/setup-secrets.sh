#!/bin/bash
# This script helps set up the required secrets for Gitea Actions
# Run this script locally to upload secrets to your Gitea instance
# Also claude wrote this script, use it more as a reference and base for hacking than anything actually useful.

set -e

# Ensure token is provided
if [ -z "$GITEA_TOKEN" ]; then
  echo "Error: GITEA_TOKEN environment variable must be set"
  echo "Create a token at https://gitea.deepak.science/user/settings/applications"
  echo "Then run: export GITEA_TOKEN=your_token"
  exit 1
fi

# API URL from your Gitea instance
GITEA_API_URL="https://gitea.deepak.science/api/v1"
REPO_OWNER="$(git remote get-url origin | sed -E 's/.*[:/]([^/]+)\/[^/]+$/\1/')"
REPO_NAME="$(git remote get-url origin | sed -E 's/.*[:/][^/]+\/([^/.]+)(\.git)?$/\1/')"

echo "Setting up secrets for $REPO_OWNER/$REPO_NAME"

# Function to create/update a secret
create_secret() {
  local secret_name="$1"
  local secret_value="$2"
  local description="$3"

  echo "Setting up secret: $secret_name - $description"

  # Create payload
  local payload="{\"name\":\"$secret_name\",\"data\":\"$secret_value\"}"

  # Send to Gitea API
  curl -X PUT \
    -H "Authorization: token $GITEA_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    "$GITEA_API_URL/repos/$REPO_OWNER/$REPO_NAME/secrets/$secret_name"

  echo -e "\nDone!\n"
}

# Prompt for required secrets
read -r -p "Enter SSH_GITEA_SSH_KEY (private SSH key for Git operations): " -s SSH_KEY
echo
create_secret "SSH_GITEA_SSH_KEY" "$SSH_KEY" "SSH key for Git operations in CI"

read -r -p "Enter SSH_GITEA_KNOWN_HOSTS (content for known_hosts file): " KNOWN_HOSTS
create_secret "SSH_GITEA_KNOWN_HOSTS" "$KNOWN_HOSTS" "Known hosts for SSH connections"

read -r -p "Enter PYPI_USERNAME: " PYPI_USER
create_secret "PYPI_USERNAME" "$PYPI_USER" "PyPI username for publishing"

read -r -p "Enter PYPI_API_TOKEN: " -s PYPI_TOKEN
echo
create_secret "PYPI_API_TOKEN" "$PYPI_TOKEN" "PyPI API token for publishing"

read -r -p "Enter ATTIC_ENDPOINT (URL for Attic cache): " ATTIC_ENDPOINT
create_secret "ATTIC_ENDPOINT" "$ATTIC_ENDPOINT" "Attic cache endpoint URL"

read -r -p "Enter ATTIC_CACHE (name of Attic cache): " ATTIC_CACHE
create_secret "ATTIC_CACHE" "$ATTIC_CACHE" "Attic cache name"

read -r -p "Enter ATTIC_TOKEN (authentication token for Attic): " -s ATTIC_TOKEN
echo
create_secret "ATTIC_TOKEN" "$ATTIC_TOKEN" "Attic authentication token"

# Create GITEA_TOKEN secret for self-service PR creation
create_secret "GITEA_TOKEN" "$GITEA_TOKEN" "Gitea API token for automation"

echo "All secrets have been set up! Your Gitea Actions workflows should now work properly."
echo "Make sure to give execution permission to this script with: chmod +x .gitea/setup-secrets.sh"
