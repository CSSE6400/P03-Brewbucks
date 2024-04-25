terraform {
  cloud {
    organization = "BrewBucks"

    workspaces {
      name = "BrewBucks-Terraform"
    }
  }
}
