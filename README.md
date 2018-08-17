# S3 Bucket
1) Create hangman bucket: `aws s3 mb s3://hangman`
2) Upload Lambda zips:
    * `aws s3 cp hangman-router.zip s3://hangman`
    * `aws s3 cp hangman-help.zip s3://hangman`
    * `aws s3 cp hangman-register.zip s3://hangman`
    * `aws s3 cp hangman-status.zip s3://hangman` 

# Lambdas
Assumptions:
* IAM Role exists: arn:aws:iam::072566648870:role/service-role/hangman-api-role
* Zips have been uploaded to S3 Bucket `hangman`

https://docs.aws.amazon.com/lambda/latest/dg/with-userapp-walkthrough-custom-events-upload.html
## Router 
`aws create-function --region na-east-1 --function-name hangman-router --runtime python3.6 --role arn:aws:iam::072566648870:role/service-role/hangman-api-role --handler router.lambda_handler --code S3Bucket=hangman,S3Key=router`

## Help
`aws create-function --region na-east-1 --function-name hangman-help --runtime python3.6 --role arn:aws:iam::072566648870:role/service-role/hangman-api-role --handler router.lambda_handler --code S3Bucket=hangman,S3Key=help`

## Register
`aws create-function --region na-east-1 --function-name hangman-register --runtime python3.6 --role arn:aws:iam::072566648870:role/service-role/hangman-api-role --handler router.lambda_handler --code S3Bucket=hangman,S3Key=register`

## Status
`aws create-function --region na-east-1 --function-name hangman-status --runtime python3.6 --role arn:aws:iam::072566648870:role/service-role/hangman-api-role --handler router.lambda_handler --code S3Bucket=hangman,S3Key=status`