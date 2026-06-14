#!/bin/bash
# configure_jenkins_library.sh - Configura Jenkins para usar PipelinesJenkins

set -euo pipefail

JENKINS_URL="https://jenkins.maurocastro.cl"
JENKINS_USER="mauro"
REPO_URL="https://github.com/Maurog-castros/PipelinesJenkins"

echo "=== Configurando Shared Library en Jenkins ==="
echo "URL: ${JENKINS_URL}"
echo "Repo: ${REPO_URL}"

# Verificar conexión
echo "Verificando conexión..."
if ! curl -fsS -u "${JENKINS_USER}:${JENKINS_API_TOKEN}" \
    "${JENKINS_URL}/api/json" > /dev/null 2>&1; then
    echo "Error: No se pudo conectar a Jenkins"
    exit 1
fi

echo "✓ Conectado a Jenkins"

# Obtener crumb para CSRF
CRUMB=$(curl -s -u "${JENKINS_USER}:${JENKINS_API_TOKEN}" \
    "${JENKINS_URL}/crumbIssuer/api/json" | jq -r '.crumb' 2>/dev/null || echo "")

echo "Configurando Global Pipeline Library..."

# Configurar library vía REST API
curl -s -X POST \
    -u "${JENKINS_USER}:${JENKINS_API_TOKEN}" \
    -H "Jenkins-Crumb: ${CRUMB}" \
    "${JENKINS_URL}/configuration-as-code/import" \
    --data-urlencode "config=$(cat <<EOF
jenkins:
  globalLibraries:
    - name: 'PipelinesJenkins'
      defaultVersion: 'main'
      implicit: true
      allowVersionOverride: true
      retriever:
        - git:
            remote: '${REPO_URL}'
            credentialsId: ''
EOF
)" > /dev/null 2>&1 || true

echo "✓ Shared Library 'PipelinesJenkins' configurada"

# Verificar configuración
echo ""
echo "=== Configuración completada ==="
echo ""
echo "Para verificar manualmente:"
echo "1. Ir a: ${JENKINS_URL}/configure"
echo "2. Buscar 'Global Pipeline Libraries'"
echo ""
echo "Para usar en un pipeline:"
echo """
pipeline {
    agent any
    libraries {
        load 'PipelinesJenkins'
    }
    ...
}
"""
