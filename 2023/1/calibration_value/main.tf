
variable "input" {
   type = string
}

locals {
   first_digit = regex("[0-9]", var.input)
   last_digit = regex("[0-9]", join("",reverse(split("",var.input))))
}

output "input" {
   value = var.input
}

output "result" {
   value = join("",[local.first_digit, local.last_digit])
}
