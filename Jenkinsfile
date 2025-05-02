pipeline {
    // Consider specifying the agent label used in your EC2 config
    // agent { label 'aws-ec2-agent' }
    agent any

    stages {
        stage('Clone') {
            steps {
                echo "Cloning repository..."
                checkout scm
            }
        }

        stage('Set up Python 3.11') { // Stage name updated for clarity
            steps {
                echo "Setting up Python 3.11 virtual environment..."
                sh '''
                    # Create venv using the installed python3.11
                    python3.11 -m venv venv

                    # Activate the new environment
                    source venv/bin/activate

                    # Upgrade pip within the venv
                    pip install --upgrade pip

                    # Install dependencies from your committed requirements.txt
                    # This should now work as numpy 2.x is compatible with Python 3.11
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pytest') {
            steps {
                echo "Running tests..."
                sh '''
                    # Activate the virtual environment (created with Python 3.11)
                    source venv/bin/activate

                    # Run pytest
                    pytest test/ --maxfail=1
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline completed with status: ${currentBuild.currentResult}"
        }
        failure {
            echo "Build failed. Please check the console output for errors."
        }
    }
}
