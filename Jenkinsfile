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

        stage('Set up Python 3.11') {
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
                    # (This now includes pytest-html)
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pytest & Generate Reports') { // Updated stage name
            steps {
                echo "Running tests and generating reports..."
                sh '''
                    source venv/bin/activate
                    # Run pytest, generating both JUnit XML and self-contained HTML
                    # --maxfail=1 stops the run on the first failing test
                    pytest test/ --maxfail=1 --junitxml=report.xml --html=report.html --self-contained-html
                '''
            }
        }
    }

    post {
        // This block runs regardless of the build status
        always {
            script {
                // --- Publish Reports ---

                // Try to publish JUnit results (for Jenkins UI integration)
                // allowEmptyResults: true prevents failure if report.xml doesn't exist (e.g., setup failed)
                try {
                    junit allowEmptyResults: true, testResults: 'report.xml'
                } catch (err) {
                    echo "Failed to publish JUnit results: ${err}"
                }

                // Try to publish HTML report (for easy viewing)
                try {
                    publishHTML([
                        allowMissing: true, // Don't fail if report.html is missing
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.', // Relative to workspace root
                        reportFiles: 'report.html',
                        reportName: 'Pytest HTML Report' // Name for the link in Jenkins UI
                    ])
                } catch (err) {
                    echo "Failed to publish HTML report: ${err}"
                }

                // --- Send Email ---
                // Define email details
                def recipientList = "arunbasil83@gmail.com" // <<< CHANGE THIS TO YOUR DESIRED RECIPIENT(S)
                def emailSubject = "[Jenkins] ${currentBuild.fullDisplayName} - ${currentBuild.currentResult}"
                def reportLink = "${env.BUILD_URL}HTML_Report/" // Link to the published HTML report index
                def consoleLink = "${env.BUILD_URL}console"

                // Build the email body
                def emailBody = """
                <html><body>
                <h2>Build Result: ${currentBuild.currentResult}</h2>
                <p>Check console output at: <a href="${consoleLink}">${consoleLink}</a></p>
                """

                // Add link to HTML report if it was likely generated (build didn't fail before tests)
                if (currentBuild.currentResult != 'ABORTED' && currentBuild.currentResult != 'FAILURE' || manager.logContains("test session starts")) {
                     emailBody += "<p>View Pytest HTML Report: <a href=\"${reportLink}\">${reportLink}</a></p>"
                }

                // Add test summary from JUnit results (if available)
                // Note: TEST_COUNTS might not be populated if JUnit step failed or ran after emailext
                // It's generally more reliable to parse report.xml if needed, but this is simpler.
                emailBody += """
                <hr>
                <p><i>(This summary relies on JUnit processing completing before email sending)</i></p>
                <p><b>Test Summary:</b></p>
                <p>\${TEST_COUNTS, var="total"} total tests run.</p>
                <p>\${TEST_COUNTS, var="fail"} failures.</p>
                <p>\${TEST_COUNTS, var="skip"} skipped.</p>
                </body></html>
                """

                // Customize subject further for failures
                if (currentBuild.currentResult == 'FAILURE') {
                   emailSubject = "[FAILURE] ${currentBuild.fullDisplayName}"
                } else if (currentBuild.currentResult == 'UNSTABLE') {
                   emailSubject = "[UNSTABLE] ${currentBuild.fullDisplayName}"
                }

                // Send the email using the configured Extended E-mail Notification settings
                try {
                    emailext (
                        subject: emailSubject,
                        body: emailBody,
                        to: recipientList,
                        mimeType: 'text/html'
                        // Add attachments, replyTo, etc. as needed:
                        // attachLog: true,
                        // attachmentsPattern: 'report.html'
                    )
                    echo "Email notification sent to ${recipientList}."
                } catch (err) {
                    echo "Failed to send email notification: ${err}"
                }
            } // end script block
        } // end always block

        // You could add more specific blocks if needed, e.g.:
        // failure {
        //     echo "Specific actions only on failure..."
        // }
        // success {
        //     echo "Specific actions only on success..."
        // }
    } // end post block
}
