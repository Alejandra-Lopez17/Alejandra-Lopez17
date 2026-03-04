#!/bin/bash

# Define color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

files=$(find . -not -path "*/venv/*" -not -path "*/notebooks/*" -not -path "*/*.egg-info/*" \( -name "*.typ" -o -name "*.txt" -o -name "*.sh" -o -name "*.md" -o -name "*.yml" \))

# Flag to track if we found any non-compliant files
non_compliant=false

for file in $files; do
  echo "Checking $file"

  # Check for tabs
  if grep -q $'\t' "$file"; then
    echo -e "${RED}Error: Tabs found in file!${NC}"
    non_compliant=true
  else
    echo -e "${GREEN}Tabs: OK${NC}"
  fi

  # Check for trailing spaces
  if grep -q " $" "$file"; then
    echo -e "${RED}Error: Trailing spaces found in file!${NC}"
    non_compliant=true
  else
    echo -e "${GREEN}Trailing spaces: OK${NC}"
  fi

  # Check for an empty line at the end of the file
  if [ "$(tail -c 1 "$file" | wc -l)" -eq 0 ]; then
    echo -e "${RED}Error: No newline at the end of file!${NC}"
    non_compliant=true
  else
    echo -e "${GREEN}Newline at end: OK${NC}"
  fi

  echo
done

echo
echo

if [ "$non_compliant" = true ]; then
  echo -e "${RED}Code compliance check failed.${NC}"
  exit 1
else
  echo -e "${GREEN}All .typ, .txt, and .sh files are compliant!${NC}"
  exit 0
fi
