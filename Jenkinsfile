pipeline {
  agent any
  environment {
    AWS_DEFAULT_REGION = 'ap-south-1'
    S3_BUCKET = 'data-pipeline-bucket-worship7'
    MONGODB_URI = 'mongodb://localhost:27017'
    MONGODB_DB = 'data_pipeline_db'
    MONGODB_COLLECTION = 'processed_data'
  }
  stages {
    stage('Checkout') {
      steps {
        echo 'Using Jenkinsfile pasted in job (no Git for now)'
      }
    }
    stage('Build Docker Image') {
      steps {
        sh 'docker build -t data-pipeline:latest .'
      }
    }
    stage('Run Pipeline') {
      steps {
        sh '''
          docker run --rm \
            -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
            -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
            -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
            -e BUCKET_NAME=$S3_BUCKET \
            -e MONGODB_URI=$MONGODB_URI \
            -e MONGODB_DB=$MONGODB_DB \
            -e MONGODB_COLLECTION=$MONGODB_COLLECTION \
            data-pipeline:latest
        '''
      }
    }
  }
}