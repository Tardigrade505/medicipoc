var mysql = require('mysql');
var connection = mysql.createConnection({
    host: process.env.ENDPOINT,
    user: process.env.USERNAME,
    password: process.env.PASSWORD,
    port: "3306",
    debug: "true",
});

console.log(connection);
exports.handler = (event, context, callback) => {
    // context.callbackWaitsForEmptyEventLoop = false;
    // connection.query('show tables', function (error, results, fields) {
    //     if (error) {
    //         connection.destroy();
    //         throw error;
    //     } else {
    //         // connected!
    //         console.log(results);
    //         callback(error, results);
    //         connection.end(function (err) { callback(err, results);});
    //     }
    // });
    connection.query("CREATE DATABASE mydb3", function (err, result) {
    if (err) throw err;
    console.log("Database created");
  });
    // connection.connect(function(err) {
    //   if (err) {
    //       console.log("We failed to connect.");
    //       console.log(err);
    //       context.fail();
    //   } else {
    //       console.log("We succeeded in connecting!");
    //       context.succeed('Success');
    //   }
    // });
};

