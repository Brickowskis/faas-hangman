## Setup
1) Create Lambda function "params" with:
    * Runtime: Python 3.6
    * Handler: lambda-params.lambda_handler
2) Create API Gateway resource as:
    * Configure as proxy resource: Y
    * Resource name: params
    * Resource path: {params+}
3) Configure "ANY" method to use "params" Lambda function
4) Click on "Test" within "ANY" method configuration to test functionality

##Test Request:  
```Endpoint request body after transformations: {"resource":"/{param+}","path":"/testPath","httpMethod":"GET","headers":{"TestHeader":" TestValue"},"queryStringParameters":{"testQuery":"testResponse"},"pathParameters":{"param":"testPath"},"stageVariables":null,"requestContext":{"path":"/{param+}","accountId":"072566648870","resourceId":"msqj06","stage":"test-invoke-stage","requestId":"6bfe9b58-9fcd-11e8-95eb-890558f8370e","identity":{"cognitoIdentityPoolId":null,"cognitoIdentityId":null,"apiKey":"test-invoke-api-key","cognitoAuthenticationType":null,"userArn":"arn:aws:iam::072566648870:user/nsstrunks","apiKeyId":"test-invoke-api-key-id","userAgent":"aws-internal/3 aws-sdk-java/1.11.347 Linux/4.9.110-0.1.ac.201.71.329.metal1.x86_64 Java_HotSpot(TM)_64-Bit_Server_VM/25.172-b31 java/1.8.0_172","accountId":"072566648870","caller":"AIDAJJQ3VPYOHGUT72NRE","sourceIp":"test-invoke-source-ip","accessKey":"ASIARBZKPGATMUVFXZPO","cognitoAuthenticationProvider":null,"user":"AIDAJJQ3VPYOHGUT72NRE"},"resourcePath":"/{param+}"```

##Test Response:
```{
  "resource": "/{param+}",
  "path": "/testPath",
  "httpMethod": "GET",
  "headers": {
    "TestHeader": " TestValue"
  },
  "queryStringParameters": {
    "testQuery": "testResponse"
  },
  "pathParameters": {
    "param": "testPath"
  },
  "stageVariables": null,
  "requestContext": {
    "path": "/{param+}",
    "accountId": "072566648870",
    "resourceId": "msqj06",
    "stage": "test-invoke-stage",
    "requestId": "6bfe9b58-9fcd-11e8-95eb-890558f8370e",
    "identity": {
      "cognitoIdentityPoolId": null,
      "cognitoIdentityId": null,
      "apiKey": "test-invoke-api-key",
      "cognitoAuthenticationType": null,
      "userArn": "arn:aws:iam::072566648870:user/nsstrunks",
      "apiKeyId": "test-invoke-api-key-id",
      "userAgent": "aws-internal/3 aws-sdk-java/1.11.347 Linux/4.9.110-0.1.ac.201.71.329.metal1.x86_64 Java_HotSpot(TM)_64-Bit_Server_VM/25.172-b31 java/1.8.0_172",
      "accountId": "072566648870",
      "caller": "AIDAJJQ3VPYOHGUT72NRE",
      "sourceIp": "test-invoke-source-ip",
      "accessKey": "ASIARBZKPGATMUVFXZPO",
      "cognitoAuthenticationProvider": null,
      "user": "AIDAJJQ3VPYOHGUT72NRE"
    },
    "resourcePath": "/{param+}",
    "httpMethod": "GET",
    "extendedRequestId": "LnjOPF9QoAMF4QA=",
    "apiId": "t13oueund6"
  },
  "body": null,
  "isBase64Encoded": false
}```