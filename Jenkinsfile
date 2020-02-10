pipeline {
    agent none
    stages {
        stage ("Install dependencies") {
            agent { 
                docker { image 'python:3.8-slim-buster' } 
            }
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip &&\
                                pip install -r requirements.txt
                    pylint --disable=R,C,W1203,W1202 app.py 
                '''  
            }
        }
	    
        stage('Building Image') {
            
            steps {
                script {                
                    docker.withRegistry('https://registry.hub.docker.com/repository/docker/dipandocker/caseservice', 'static-dockerhub') {
                        def customImage = docker.build("dipandocker/caseservice")
                        /* Push the container to the custom Registry */
                        customImage.push()
                    }
                }	
            }
        }
    }
}
