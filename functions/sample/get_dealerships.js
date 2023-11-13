const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

function main(params) {
  const secret = {
    COUCH_URL: "",
    COUCH_USERNAME: "",
    IAM_API_KEY: "",
  };
  return new Promise(function (resolve, reject) {
    const authenticator = new IamAuthenticator({
      apikey: secret["IAM_API_KEY"],
    });
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator,
    });
    cloudant.setServiceUrl(secret["COUCH_URL"]);
    if (params["params"]["state"]) {
      const selector = {
        state: { $eq: params["params"]["state"] },
      };
      cloudant
        .postFind({ db: "dealerships", selector: selector })
        .then((response) => {
          result = response.result["docs"];
          if (result.length === 0) {
            reject({
              statusCode: 404,
              "Content-Type": "application/json",
              body: "No dealerships in that state!",
            });
          }
          resolve({
            statusCode: 200,
            "Content-Type": "application/json",
            body: result,
          });
        });
    } else {
      cloudant
        .postAllDocs({ db: "dealerships", includeDocs: true })
        .then((response) => {
          const dealerships = [];
          for (let dealership of response.result.rows) {
            dealerships.push(dealership["doc"]);
          }
          if (dealerships.length === 0) {
            reject({
              statusCode: 404,
              "Content-Type": "application/json",
              body: "The database is empty!",
            });
          }
          resolve({
            statusCode: 200,
            headers: { "Content-Type": "application/json" },
            body: dealerships,
          });
        });
    }
  });
}
