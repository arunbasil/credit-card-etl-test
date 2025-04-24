pipeline {
    agent any // Use any available agent (ensure it has Python3, pip, git)

    stages {
        stage('Clone') {
            steps {
                echo "Cloning repository..."
                // Fetches the code from the SCM configured in the Jenkins job
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                echo "Setting up Python virtual environment..."
                sh '''
                    # Ensure python3 is available on the agent
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    # Installs dependencies from your committed requirements.txt
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pytest') {
            steps {
                echo "Running tests..."
                sh '''
                    # Activate the virtual environment within this shell step
                    source venv/bin/activate
                    # Run pytest on the 'test/' directory
                    # --maxfail=1 stops the run on the first failing test
                    # Removed report generation, quiet mode, and log redirection
                    pytest test/ --maxfail=1
                '''
            }
        }
        // Removed stages: 'Upload Report to S3', 'Archive Artifacts', 'Publish Report to Jenkins'
    }

    post {
        // Basic messages about the build outcome
        always {
            echo "Pipeline completed with status: ${currentBuild.currentResult}"
        }
        failure {
            echo "Build failed. Please check the console output for errors."
            // You could add notifications here (e.g., Slack, email) if desired
        }
    }
}