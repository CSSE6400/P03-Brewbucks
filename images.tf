resource "docker_image" "brewbucks" {
  name = "${aws_ecr_repository.brewbucks.repository_url}:latest"
  build {
    context = "./backend/."
  }
}

resource "docker_registry_image" "brewbucks" {
  name = docker_image.brewbucks.name
}

resource "aws_ecr_repository" "brewbucks" {
  name = "brewbucks"
}

resource "docker_registry_image" "brewbucks-frontend" {
  name = docker_image.brewbucks-frontend.name
}

resource "docker_image" "brewbucks-frontend" {
  name = "${aws_ecr_repository.brewbucks-frontend.repository_url}:latest"
  build {
    context = "./front-end/."
  }
}

resource "aws_ecr_repository" "brewbucks-frontend" {
  name = "brewbucks-frontend"
}