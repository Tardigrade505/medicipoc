// "use strict";
var AWS = require('aws-sdk');
const randomBytes = require('crypto').randomBytes;

// Get "Hello" Dynamo table name.  Replace DEFAULT_VALUE 
// with the actual table name from your stack.
console.log("HI")
const helloDBArn = process.env['BUDGET_DB'] || 'DEFAULT_VALUE';  //'Mark-HelloTable-1234567';
const helloDBArnArr = helloDBArn.split('/');
const helloTableName = helloDBArnArr[helloDBArnArr.length - 1];

// handleHttpRequest is the entry point for Lambda requests
exports.handleHttpRequest = function(request, context, done) {
    console.log("HERE")
  try {
    const account_id = request.pathParameters.account_id;
    let response = {
      headers: {},
      body: '',
      statusCode: 200
    };

    switch (request.httpMethod) {
      case 'GET': {
        console.log('GET');
        let dynamo = new AWS.DynamoDB.DocumentClient();
        var params = {
            TableName: helloTableName,
            KeyConditionExpression: 'account_id = :hkey',
            ExpressionAttributeValues: {
                ':hkey': account_id
            }
        };

        // Call DynamoDB to read the item from the table
        dynamo.query(params, function(err, data) {
          if (err) {
            console.log("Error", err);
            throw `Dynamo Scan Error (${err})`
          } else {
            console.log("Success", data.Items);
            response.body = JSON.stringify(data.Items);
            done(null, response);
          }
        });
        break;
      }
      case 'POST': {
        console.log('POST');
        console.log("Account ID: " + account_id)
        let bodyJSON = JSON.parse(request.body || '{}');
        console.log("JSON Body: " + bodyJSON)
        let dynamo = new AWS.DynamoDB.DocumentClient();
        let budget_id = byteToString(randomBytes(10))
        let params = {
          TableName: helloTableName,
          Item: {
            'account_id': account_id,
            'budget_id': budget_id,
            'name': bodyJSON['name'],
            'budget_value': bodyJSON['budget_value'],
            'actual_value': bodyJSON['actual_value'],
            'category': bodyJSON['category'],
            'expense_type': bodyJSON['expense_type']
          }
        };
        dynamo.put(params, function(error, data) {
          if (error) {
              throw `Dynamo Error (${error})`;
          } else {
              response.body = JSON.stringify(
                {
                    budget_id: budget_id,
                }
                )
                response.statusCode = 201
              done(null, response);
          }
        })
        break;
      }
    }
  } catch (e) {
    done(e, null);
  }
}

function byteToString(buffer) {
    return buffer.toString('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=/g, '');
}

