import os

token = os.environ["TF_API_TOKEN"]
tf_endpoint = "https://app.terraform.io/api/v2"
headers = {
    "Authorization": "Bearer %s" % (token),
    "Content-Type": "application/vnd.api+json",
}
