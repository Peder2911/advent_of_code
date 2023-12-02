
variable "input" {
   type = string
}

output "raw" {
   value = var.input
}

output "result" {
   value = replace(
   replace(
   replace(
   replace(
   replace(
   replace(
   replace(
   replace(
   replace(
   var.input, 
   "one","one1one"),
   "two","two2two"),
   "three","three3three"),
   "four","four4four"),
   "five","five5five"),
   "six","six6six"),
   "seven","seven7seven"),
   "eight","eight8eight"),
   "nine","nine9nine")
}
