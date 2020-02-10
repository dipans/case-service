pipeline {
    agent { docker { image 'python:3.8-slim-buster' } }
    stages {
        stage ("Install dependencies") {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip &&\
                                pip install -r requirements.txt
                    
                '''  
            }
        }
        stage('Linting') {
            steps {
            sh '''
                . venv/bin/activate
                pylint --disable=R,C,W1203,W1202 app.py 
            '''
            }
        }
	    
        stage('Building Image') {
            steps {
                script {
                    def dockerHome = tool 'default-docker'
                    env.PATH = "${dockerHome}/bin:${env.PATH}"
                    docker.build("dipandocker/case-service")
                }	
            }
        }
    }
}