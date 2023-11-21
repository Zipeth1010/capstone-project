function main(params) {
  const secret = {
    COUCH_URL:
      "https://c70b7079-0862-4d2f-b8c6-e3750069f0eb-bluemix.cloudantnosqldb.appdomain.cloud",
    COUCH_USERNAME: "c70b7079-0862-4d2f-b8c6-e3750069f0eb-bluemix",
    IAM_API_KEY: "2oZBQ19trfU-56FTfwRiBt4KfW1drofTWQ8rpkKNCPrI",
  };
  const authenticator = new IamAuthenticator({ apikey: secret["IAM_API_KEY"] });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(secret["COUCH_URL"]);
  app.get("/dealerships", async (req, res) => {
    try {
      const { state } = req.query;
      if (!state) {
        cloudant
          .postAllDocs({ db: "dealerships", includeDocs: true })
          .then((response) => {
            const dealerships = [];
            for (let dealership of response.result.rows) {
              dealerships.push(dealership["doc"]);
            }
            if (dealerships.length === 0) {
              return res
                .status(404)
                .json({
                  "Content-Type": "application/json",
                  body: "The database is empty!",
                });
            }
            return res
              .status(200)
              .json({
                headers: { "Content-Type": "application/json" },
                body: dealerships,
              });
          });
      }
      const query = {
        selector: {
          state: { $eq: state },
        },
      };
      const result = cloudant
        .postFind({ db: "dealerships", selector: selector })
        .then((response) => {
          result = response.result["docs"];
          if (result.length === 0) {
            return res
              .status(404)
              .json({ message: "No dealerships in that State!" });
          }
          return res.status(200).json({
            "Content-Type": "application/json",
            body: result,
          });
        });
    } catch (error) {
      console.error("Error:", error.message);
      res.status(500).json({ error: "Internal Server Error" });
    }
  });
}
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
