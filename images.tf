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
