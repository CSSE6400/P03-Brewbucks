resource "aws_lb_target_group" "brewbucks" {
  name        = "brewbucks"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_security_group.brewbucks.vpc_id
  target_type = "ip"

  health_check {
    path                = "/api/v1/health"
    port                = "80"
    protocol            = "HTTP"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 10
  }
}

resource "aws_lb_target_group" "brewbucks-frontend" {
  name        = "brewbucks-frontend"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_security_group.brewbucks.vpc_id
  target_type = "ip"

  health_check {
    path                = "/"
    port                = "80"
    protocol            = "HTTP"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 10
  }
}

resource "aws_lb" "brewbucks-frontend" {
  name               = "brewbucks-frontend"
  internal           = false
  load_balancer_type = "application"
  subnets            = data.aws_subnets.private.ids
  security_groups    = [aws_security_group.brewbucks.id]
}

resource "aws_lb_listener" "brewbucks-frontend" {
  load_balancer_arn = aws_lb.brewbucks-frontend.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.brewbucks-frontend.arn
  }

}

resource "aws_lb" "brewbucks" {
  name               = "brewbucks"
  internal           = false
  load_balancer_type = "application"
  subnets            = data.aws_subnets.private.ids
  security_groups    = [aws_security_group.brewbucks.id]
}

resource "aws_lb_listener" "brewbucks" {
  load_balancer_arn = aws_lb.brewbucks.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.brewbucks.arn
  }
}
