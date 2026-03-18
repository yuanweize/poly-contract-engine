#!/bin/bash
set -e

# Change down to src so latexmk can properly resolve local modules/ paths without hassle
cd src

# Extract the primary tenant name from data.json to use as the output file name
# Since jq is not guaranteed, we use a more precise awk block grabbing the first name after "tenants" array
TENANT_NAME=$(awk '
    /"tenants":/ {in_tenants=1}
    in_tenants && /"name":/ {
        match($0, /"name": *"([^"]+)"/, m)
        if (m[1] != "") { print m[1]; exit }
    }
' ../data.json | tr ' ' '_')

if [ -z "$TENANT_NAME" ]; then
    # Fallback if standard awk regex grouping doesn't work out of the box (BSD awk)
    TENANT_NAME=$(awk '/"tenants":/,/\]/' ../data.json | grep '"name":' | head -n 1 | awk -F'"' '{print $4}' | tr ' ' '_')
fi

if [ -z "$TENANT_NAME" ]; then
    TENANT_NAME="Unknown_Tenant"
fi

JOB_NAME="Contract_$TENANT_NAME"

echo "Building Contract for: $TENANT_NAME"

# Build using latexmk
# -outdir pushes the final PDF and aux files directly into the dist folder
latexmk -lualatex -interaction=nonstopmode -synctex=1 -jobname=$JOB_NAME -outdir=../dist main.tex

# Clean up auxiliary files from the dist directory, leaving only the PDF
echo "Cleaning compilation artifacts..."
cd ../dist
rm -f *.aux *.log *.out *.toc *.fls *.fdb_latexmk *.synctex.gz

echo "Build complete! Check dist/${JOB_NAME}.pdf"
