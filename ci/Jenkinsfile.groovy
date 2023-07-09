@Library('pipeline-lib') _

pipeline {
	
	agent { label 'python' }
	
	stages {

		stage('Install dependencies') {
			steps {
				sh 'make dev_dependencies'
			}
		}

		stage('Lint') {
			steps {
				script {
					try {
						sh 'make lint'
					} catch (error) {
						unstable(message: "${STAGE_NAME} is unstable")
					}
				}
			}
		}

		stage('Test') { 
			steps {
				script {
					try {
						sh 'make test'
					} catch (error) {
						unstable(message: "${STAGE_NAME} is unstable")
					}
				}
			}
		}
		stage('Publish') {
			when { tag pattern: "v[0-9]*\\.[0-9]*\\.[0.9]", comparator: "REGEXP"} 
			steps {
				script {
					if (currentBuild.currentResult == 'SUCCESS') {
						withCredentials([string(credentialsId: 'PyPIToken', variable: 'TOKEN')]) {
							sh '''
							make dist
							. ./.venv/bin/activate
							python3 -m pip install --upgrade twine
							python3 -m twine upload dist/* \
								--username __token__ \
								--password $TOKEN \
							'''
						}
					} else {
						error('Publish aborted due to unstable build')
					}
				}
			}
		}
	}

	post {

		success {
			script {
				notifyGitHubBuildStatus('optical_dispersion_relations', 'success')
			}
		}

		unstable {
			script {
				notifyGitHubBuildStatus('optical_dispersion_relations', 'failure')
			}
		}

		failure {
			script {
				notifyGitHubBuildStatus('optical_dispersion_relations', 'error')
			}
		}

		cleanup {
			sh "make clean"
		}

	}
}
