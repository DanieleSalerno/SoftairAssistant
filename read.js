var AWS = require("aws-sdk")

const express = require('express')
const app = express()
const port=8383

app.use(express.static('public'))


//AWS.config.update(awsConfig)
let ddb=new AWS.DynamoDB({apiVersion: '2012-08-10',endpoint: 'http://localhost:4566'});
var params = {
    ExpressionAttributeValues:{
        ":v1":{
            S:"Vitality_0"
        }
    },
    KeyConditionExpression: 'player_id = :v1',

    TableName: 'GPS_data'
};
console.log("aisdaisdjaskdjasd")
ddb.query(params, function(err, data) {
    console.log(params)
    if (err) {
        console.log("Error", err);
    } else {
        console.log("aiaiaiaiaiaiaia")
        console.log("Success", data.Items);
        data.Items.forEach(function(element, index, array) {
            console.log(AWS.DynamoDB.Converter.output(element['player_id']));
            console.log(AWS.DynamoDB.Converter.output(element['longitude']));
            console.log(AWS.DynamoDB.Converter.output(element['latitude']));
        });
    }
});
