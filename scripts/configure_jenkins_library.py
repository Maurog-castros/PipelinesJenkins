#!/usr/bin/env python3
"""
configure_jenkins_library.py
Configura Jenkins para usar la shared library PipelinesJenkins
"""

import os
import sys
import requests

# Configuración
JENKINS_URL = "https://jenkins.maurocastro.cl"
JENKINS_USER = os.environ.get("JENKINS_USER", "mauro")
JENKINS_API_TOKEN = os.environ.get("JENKINS_API_TOKEN", "")
REPO_URL = "https://github.com/Maurog-castros/PipelinesJenkins"

def get_crumb(session):
    """Obtiene el crumb CSRF de Jenkins"""
    url = f"{JENKINS_URL}/crumbIssuer/api/json"
    resp = session.get(url)
    resp.raise_for_status()
    return resp.json().get("crumb", "")

def configure_library():
    """Configura la shared library en Jenkins"""
    
    # Crear sesión
    session = requests.Session()
    session.auth = (JENKINS_USER, JENKINS_API_TOKEN)
    
    print("=== Configurando Shared Library en Jenkins ===")
    print(f"URL: {JENKINS_URL}")
    print(f"Repo: {REPO_URL}")
    
    # Verificar conexión
    print("\nVerificando conexión...")
    try:
        resp = session.get(f"{JENKINS_URL}/api/json")
        resp.raise_for_status()
        print("✓ Conectado a Jenkins")
    except requests.exceptions.RequestException as e:
        print(f"✗ Error conectando: {e}")
        sys.exit(1)
    
    # Obtener crumb
    try:
        crumb = get_crumb(session)
    except Exception as e:
        print(f"✗ Error obteniendo crumb: {e}")
        sys.exit(1)
    
    # Configurar library vía REST API
    print("\nConfigurando Global Pipeline Library...")
    
    headers = {"Jenkins-Crumb": crumb}
    
    # Usar Jenkins Configuration as Code (si está disponible)
    config_yaml = f"""jenkins:
  globalLibraries:
    - name: 'PipelinesJenkins'
      defaultVersion: 'main'
      implicit: true
      allowVersionOverride: true
      retriever:
        - git:
            remote: '{REPO_URL}'
            credentialsId: ''
"""
    
    try:
        resp = session.post(
            f"{JENKINS_URL}/configuration-as-code/import",
            headers=headers,
            data=config_yaml.encode('utf-8'),
            params={'where': 'import'},
            timeout=30
        )
        
        if resp.status_code == 200:
            print("✓ Shared Library 'PipelinesJenkins' configurada")
        else:
            # Fallback: usar script API
            print(f"⚠ configuration-as-code falló (HTTP {resp.status_code}), intentando con script API...")
            
            groovy_script = """import jenkins.model.*
import org.jenkinsci.plugins.workflow.libs.*

def instance = Jenkins.getInstance()
def lib = new LibraryConfiguration(
    'PipelinesJenkins',
    new org.jenkinsci.plugins.workflow.libs.GitSCMSource(
        null, 'REPO_URL_PLACEHOLDER', 'main', '', true, null
    )
)
lib.setDefaultVersion('main')
lib.setImplicit(true)
lib.setAllowVersionOverride(true)

def libs = instance.getExtensionList('org.jenkinsci.plugins.workflow.libs.GlobalLibraries')[0]
def libraries = libs.getLibraries()

// Remove existing if exists
libraries = libraries.findAll { library -> library.name != 'PipelinesJenkins' }
libraries.add(lib)
libs.setLibraries(libraries)

instance.save()
""".replace('REPO_URL_PLACEHOLDER', REPO_URL)
            
            resp = session.post(
                f"{JENKINS_URL}/scriptText",
                headers=headers,
                data={
                    'script': groovy_script,
                    'sandbox': 'true'
                },
                timeout=30
            )
            
            if resp.status_code == 200:
                print("✓ Shared Library configurada vía script API")
            else:
                print(f"✗ Error: HTTP {resp.status_code}")
                print(resp.text[:500])
                sys.exit(1)
                
    except requests.exceptions.RequestException as e:
        print(f"✗ Error configurando: {e}")
        sys.exit(1)
    
    # Verificar configuración
    print("\n=== Configuración completada ===")
    print("\nPara verificar manualmente:")
    print(f"1. Ir a: {JENKINS_URL}/configure")
    print("2. Buscar 'Global Pipeline Libraries'")
    print("\nPara usar en un pipeline:")
    print("""
pipeline {
    agent any
    libraries {
        load 'PipelinesJenkins'
    }
    stages {
        stage('Deploy') {
            steps {
                script {
                    load 'vars/deployMinikube.groovy'
                    deployMinikube(host: '192.168.1.12', user: 'mauro')
                }
            }
        }
    }
}
""")

if __name__ == "__main__":
    if not JENKINS_API_TOKEN:
        print("Error: JENKINS_API_TOKEN no configurado")
        sys.exit(1)
    configure_library()
