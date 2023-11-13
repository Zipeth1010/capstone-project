from ibmcloudant.cloudant_v1 import CloudantV1,  IndexDefinition, IndexField, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import sys

def main(dict):
    if dict['params']['method'] == 'get':
        return get_reviews(dict)
    elif dict['params']['method'] == 'post':
        return post_review(dict)
    else:
        return {"statusCode": 405,"body": "Method Not Allowed"}

def get_reviews(dict):
    secret = {
        "COUCH_URL":"https://c70b7079-0862-4d2f-b8c6-e3750069f0eb-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY":"2oZBQ19trfU-56FTfwRiBt4KfW1drofTWQ8rpkKNCPrI",
        "COUCH_USERNAME" : "c70b7079-0862-4d2f-b8c6-e3750069f0eb-bluemix"
    }
    authenticator = IAMAuthenticator(secret["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(secret['COUCH_URL'])
    try:
        index_field = IndexField(id="desc")
        index = IndexDefinition(fields=[index_field])
        response1 = service.post_index(db='reviews',ddoc='json-index',name='getDealerbyId',index=index,type='json').get_result()
        response = service.post_find(db='reviews', 
        selector = {'dealership' : {'$eq' : int(dict['params']['dealerId'])}},
        fields = ["id", "name", "dealership", "review", "purchase", "purchase_date",
        "car_make", "car_model", "car_year"],
        sort = [{"id" : 'desc'}]).get_result()
        return { "result" : response['docs']}
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def post_review(dict):
    secret = {
        "COUCH_URL":"https://c70b7079-0862-4d2f-b8c6-e3750069f0eb-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY":"2oZBQ19trfU-56FTfwRiBt4KfW1drofTWQ8rpkKNCPrI",
        "COUCH_USERNAME" : "c70b7079-0862-4d2f-b8c6-e3750069f0eb-bluemix"
    }
    authenticator = IAMAuthenticator(secret["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(secret['COUCH_URL'])
    try:
        response1 = service.post_all_docs(db='reviews', include_docs=True).get_result()
        length = len(response1['rows'])
        review = dict['params']['review']
        review_doc = Document(review_id=length, name = review["name"], dealership=review["dealership"], 
        review=review['review'], purchase = review['purchase'], another=review['another'], 
        purchase_date=review['purchase_date'], car_make=review['car_make'], car_model=review['car_model'],
        car_year=review['car_year'])
        response2 = service.post_document(db='reviews', document=review_doc).get_result()
        return {"review": response2}
        
    except Exception as e:
        print(f"An error occured: {e}")
        return None
