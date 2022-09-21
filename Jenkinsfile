pipeline {
    agent any
    

    stages {
        stage('checkout'){
            steps {
                checkout([
        $class: 'GitSCM', 
        branches: [[name: '*/main']], 
        doGenerateSubmoduleConfigurations: false, 
        extensions: [[$class: 'CleanCheckout']], 
        submoduleCfg: []
    ])
            }
        }
        stage('Hello') {
            steps {
                echo 'Hello World!!!!!'
            }
        }
    }
}
