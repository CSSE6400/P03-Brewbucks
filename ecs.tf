resource "aws_ecs_cluster" "brewbucks" {
  name = "brewbucks"
}

resource "aws_ecs_task_definition" "brewbucks-frontend" {
  family = "brewbucks-frontend"
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu = 1024
  memory = 2048
  execution_role_arn = data.aws_iam_role.lab.arn
  depends_on = [docker_image.brewbucks-frontend]

  container_definitions = <<DEFINITION
 [ 
   { 
    "image": "${docker_registry_image.brewbucks-frontend.name}", 
    "cpu": 1024, 
    "memory": 2048, 
    "name": "brewbucks-frontend", 
    "networkMode": "awsvpc", 
    "portMappings": [ 
      { 
       "containerPort": 80, 
       "hostPort": 80 
      } 
    ], 
    "environment": [ 
      { 
       "name": "BASE_URL", 
       "value": "http://${aws_lb.brewbucks.dns_name}" 
      } 
    ],
    "logConfiguration": { 
      "logDriver": "awslogs", 
      "options": { 
       "awslogs-group": "/brewbucks/frontend", 
       "awslogs-region": "us-east-1", 
       "awslogs-stream-prefix": "ecs", 
       "awslogs-create-group": "true" 
      } 
    } 
   } 
 ] 
 DEFINITION 
}

resource "aws_ecs_task_definition" "brewbucks" {
  family                   = "brewbucks"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = data.aws_iam_role.lab.arn
  depends_on               = [docker_image.brewbucks]

  container_definitions = <<DEFINITION
 [ 
   { 
    "image": "${docker_registry_image.brewbucks.name}", 
    "cpu": 1024, 
    "memory": 2048, 
    "name": "brewbucks", 
    "networkMode": "awsvpc", 
    "portMappings": [ 
      { 
       "containerPort": 80, 
       "hostPort": 80 
      } 
    ], 
    "environment": [ 
      { 
       "name": "SQLALCHEMY_DATABASE_URI", 
       "value": "postgresql://${local.database_username}:${local.database_password}@${aws_db_instance.database.address}:${aws_db_instance.database.port}/${aws_db_instance.database.db_name}" 
      } 
    ], 
    "logConfiguration": { 
      "logDriver": "awslogs", 
      "options": { 
       "awslogs-group": "/brewbucks/api", 
       "awslogs-region": "us-east-1", 
       "awslogs-stream-prefix": "ecs", 
       "awslogs-create-group": "true" 
      } 
    } 
   } 
 ] 
 DEFINITION 
}

resource "aws_ecs_service" "brewbucks-frontend" {
  name            = "brewbucks-frontend"
  cluster         = aws_ecs_cluster.brewbucks.id
  task_definition = aws_ecs_task_definition.brewbucks-frontend.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  depends_on      = [aws_ecs_task_definition.brewbucks-frontend]

  network_configuration {
    subnets          = data.aws_subnets.private.ids
    security_groups  = [aws_security_group.brewbucks.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.brewbucks-frontend.arn
    container_name   = "brewbucks-frontend"
    container_port   = 80
  }
  
}

resource "aws_ecs_service" "brewbucks" {
  name            = "brewbucks"
  cluster         = aws_ecs_cluster.brewbucks.id
  task_definition = aws_ecs_task_definition.brewbucks.arn  
  desired_count   = 1
  launch_type     = "FARGATE"
  depends_on      = [aws_ecs_task_definition.brewbucks]

  network_configuration {
    subnets          = data.aws_subnets.private.ids
    security_groups  = [aws_security_group.brewbucks.id]
    assign_public_ip = true
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.brewbucks.arn
    container_name   = "brewbucks"
    container_port   = 80
  }

}

resource "aws_security_group" "brewbucks" {
  name        = "brewbucks"
  description = "BrewBucks Security Group"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # ingress {
  #   from_port   = 22
  #   to_port     = 22
  #   protocol    = "tcp"
  #   cidr_blocks = ["0.0.0.0/0"]
  # }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}