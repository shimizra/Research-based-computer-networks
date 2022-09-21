pipeline {
    agent any

    stage('checkout'){
    steps{
        script{
            
            checkout([$class: 'GitSCM', branches: [[name: 'main']], browser: [$class: 'GithubWeb', repoUrl: 'https://github.com/shimizra/Research-based-computer-networks.git'], extensions: [[$class: 'CloneOption', honorRefspec: true, noTags: true, reference: '', shallow: false], [$class: 'GitLFSPull'], [$class: 'LocalBranch', localBranch: 'main']], userRemoteConfigs: [[url: 'https://github.com/shimizra/Research-based-computer-networks.git']]])
            
        }
    }
}
    
    stages {
        stage('Hello') {
            steps {
                echo 'Hello World!!!!'
            }
        }
    }
}
