#!/bin/bash
# validate_deps.sh - Valida dependencias para Jenkins pipelines

set -euo pipefail

echo "=== Validando dependencias ==="

# Terraform
if command -v terraform &> /dev/null; then
    echo "✓ Terraform: $(terraform version | head -1)"
else
    echo "✗ Terraform no encontrado"
fi

# AWS CLI
if command -v aws &> /dev/null; then
    echo "✓ AWS CLI: $(aws --version)"
else
    echo "✗ AWS CLI no encontrado"
fi

# Docker
if command -v docker &> /dev/null; then
    echo "✓ Docker: $(docker --version)"
else
    echo "✗ Docker no encontrado"
fi

# SSH
if command -v ssh &> /dev/null; then
    echo "✓ SSH: $(ssh -V 2>&1 | head -1)"
else
    echo "✗ SSH no encontrado"
fi

# Kubectl
if command -v kubectl &> /dev/null; then
    echo "✓ Kubectl: $(kubectl version --client=true 2>&1 | head -1)"
else
    echo "✗ Kubectl no encontrado"
fi

echo "=== Validación completada ==="
