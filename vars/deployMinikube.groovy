// Shared Library: deployMinikube.groovy
// Despliega en Minikube con validación de proxy inverso

def call(Map config = [:]) {
    def host = config.host ?: '192.168.1.12'
    def user = config.user ?: 'mauro'
    def profile = config.profile ?: 'labfull'
    def publicUrl = config.publicUrl ?: 'https://labfull.maurocastro.cl'
    
    echo "=== Desplegando en Minikube ==="
    echo "Host: ${host}, User: ${user}, Profile: ${profile}"
    
    // Validar herramientas
    sh '''
        set -eu
        echo "Validando dependencias..."
        docker --version
        kubectl version --client=true
        curl --version | head -1
    '''
    
    // Desplegar
    sh """
        set -eu
        echo "Iniciando despliegue en ${host}..."
        
        # Sincronizar código
        git fetch origin \${BRANCH_NAME ?: 'main'}
        
        # Construir imágenes Docker
        docker build -t labfull-backend:demo ./backend-fastapi
        docker build -t labfull-frontend:demo ./app-web
        
        # Aplicar manifiestos Kubernetes
        kubectl apply -f ./k8s/
        
        # Esperar despliegue
        kubectl rollout status deployment/labfull-backend --timeout=120s
        kubectl rollout status deployment/labfull-frontend --timeout=120s
    """
    
    // Validar proxy inverso
    echo "Validando proxy inverso en ${publicUrl}..."
    sh """
        curl -fkSs "${publicUrl}" | grep -qi "LabFull" || error("Validación de proxy inverso fallida")
        curl -fkSs "${publicUrl}/api/health" | grep -qi '"status":"healthy"' || error("Health check falló")
    """
    
    echo "=== Despliegue completado ==="
}
