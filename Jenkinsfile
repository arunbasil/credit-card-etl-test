pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                echo "Cloning repository..."
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                echo "Setting up Python virtual environment..."
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pytest') {
            steps {
                echo "Running tests and generating HTML report..."
                sh '''
                    source venv/bin/activate
                    mkdir -p test/logs reports
                    pytest tests/ \
                        --html=reports/report.html \
                        --self-contained-html \
                        --maxfail=1 \
                        --disable-warnings \
                        -q > test/logs/test_output.log
                '''
            }
        }

        stage('Upload Report to S3') {
            steps {
                echo "Uploading report.html to S3 bucket..."
                sh '''
                    aws s3 cp reports/report.html s3://your-s3-bucket-name/project-x/$(date +%F)/report.html
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'test/logs/test_output.log', fingerprint: true
                archiveArtifacts artifacts: 'reports/report.html', fingerprint: true
            }
        }

        stage('Publish Report to Jenkins') {
            steps {
                publishHTML([
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Pytest HTML Report'
                ])
            }
        }
    }

    post {
        always {
            echo "Pipeline completed with status: ${currentBuild.currentResult}"
        }
        failure {
            echo "Build failed. Please check the logs."
        }
    }
}
