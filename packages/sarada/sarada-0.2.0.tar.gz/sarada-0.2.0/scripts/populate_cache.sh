#!/usr/bin/env bash
set -Eeuo pipefail

CACHE_PATH=${CACHE_PATH:-"/tmp/nixcache"}

banner() {
  echo "========================================================"
  echo "  $*"
  echo "========================================================"
}

banner "List what we start with"

nix-store --query --requisites --include-outputs "$(nix eval .\#devShells.x86_64-linux.default.drvPath --raw)" >dependencies.txt
nix-store --query --requisites --include-outputs "$(nix eval .\#packages.x86_64-linux.default.drvPath --raw)" >>dependencies.txt
# nix-store --query --requisites --include-outputs "$(nix eval .\#checks.x86_64-linux.formatting.drvPath --raw)" >>dependencies.txt
# nix-store --query --requisites --include-outputs "$(nix eval .\#checks.x86_64-linux.test-check.drvPath --raw)" >>dependencies.txt
nix-store --query --requisites --include-outputs "$(nix eval .\#formatter.x86_64-linux.drvPath --raw)" >>dependencies.txt

sort -o dependencies.txt -u dependencies.txt

banner "list obtained paths to cache"

wc -l dependencies.txt

banner "filter out our matches"

echo "Using filter"
cat scripts/populate_cache_exclude_patterns.txt

grep -vf scripts/populate_cache_exclude_patterns.txt dependencies.txt >filtered_dependencies.txt

echo "Count our filtered"
wc -l filtered_dependencies.txt

xargs <filtered_dependencies.txt -r nix copy --to "file://${CACHE_PATH}" --no-substitute
