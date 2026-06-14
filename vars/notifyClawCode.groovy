// Shared Library: notifyClawCode.groovy
// Notifica a ClawCode (WhatsApp) sobre el estado del pipeline

def call(Map config = [:]) {
    def webhookUrl = config.webhookUrl ?: env.OPENCLAW_WEBHOOK_URL
    def app = config.app ?: 'LabFull'
    def status = config.status ?: (currentBuild.result == 'SUCCESS' ? 'success' : 'failure')
    def message = config.message
    def nextBranch = config.nextBranch ?: 'aws-deploy'
    def approvalSignal = config.approvalSignal ?: '1'
    
    if (!webhookUrl) {
        echo "OPENCLAW_WEBHOOK_URL no configurado. Saltando notificación."
        return
    }
    
    def payload = [
        app: app,
        status: status,
        message: message ?: "${app} ${status == 'success' ? 'completó' : 'falló'} en la rama ${env.BRANCH_NAME ?: 'unknown'}",
        next_branch: nextBranch,
        approval_signal: approvalSignal,
        public_url: config.publicUrl ?: 'https://labfull.maurocastro.cl'
    ]
    
    echo "=== Notificando a ClawCode ==="
    sh """
        curl -fsS -X POST \\
            -H 'Content-Type: application/json' \\
            -d '${jsonOutput(payload)}' \\
            "${webhookUrl}"
    """
}

def jsonOutput(Map data) {
    def parts = []
    data.each { k, v ->
        parts.push("\"${k}\":\"${v}\"")
    }
    return '{' + parts.join(',') + '}'
}
