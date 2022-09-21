pipeline {
    agent any
    

    stages {
        stage('checkout'){
            steps {
                checkout([$class: 'GitSCM',
         branches: [[name: '*/main']],
         userRemoteConfigs: [[url: 'https://github.com/shimizra/Research-based-computer-networks.git/']]])
            }
        }
        stage('Hello') {
            steps {
                echo 'Hello World!!!!!'
            }
        }
    }
}
