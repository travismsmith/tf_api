terraform {
  required_providers {
    http = {
      source = "hashicorp/http"
      version = "~>3.2.1"
    }
    random = {
      source = "hashicorp/random"
      version = "~>3.4.3"
    }
  }
}

locals {
  hello_world_local = "Hello World - Local"
}

data "http" "tf_version" {
  url = "https://checkpoint-api.hashicorp.com/v1/check/terraform"

  request_headers = {
    Accept = "application/json"
  }
}
