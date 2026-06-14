# PipelinesJenkins

Repositorio centralizado para pipelines de Jenkins versionados.

## Estructura

```
PipelinesJenkins/
├── README.md          # Este archivo
├── vars/              # Shared Library de Jenkins (Groovy)
│   ├── deployMinikube.groovy
│   └── notifyClawCode.groovy
└── scripts/           # Scripts reutilizables (bash, python)
    └── validate_deps.sh
```

## Shared Library (`vars/`)

Los archivos `.groovy` en `vars/` son funciones reutilizables que pueden ser llamadas desde cualquier pipeline:

### `deployMinikube.groovy`
Despliega en Minikube con validación de proxy inverso.

### `notifyClawCode.groovy`
Notifica a ClawCode (WhatsApp) sobre el estado del pipeline.

## Uso en Jenkins

### 1. Configurar Global Pipeline Libraries
En Jenkins → **Manage Jenkins** → **Configure System** → **Global Pipeline Libraries**

- Name: `PipelinesJenkins`
- Default version: `main`
- Retrieval method: Modern SCM
- SCM: GitHub (o tu repositorio)

### 2. Usar en un pipeline

```groovy
pipeline {
    agent any
    libraries {
        load 'PipelinesJenkins'
    }
    
    stages {
        stage('Deploy') {
            steps {
                deployMinikube(
                    host: '192.168.1.12',
                    user: 'mauro'
                )
            }
        }
    }
}
```

## Autenticación

Para acceder a Jenkins API, usar:
- User: `mauro`
- API Token: Generar en `/user/mauro/configure`

## Repositorios relacionados

- [Terraform](https://github.com/.../Terraform) — Infraestructura
- [LabFull](https://github.com/.../LabFull) — Aplicación principal
