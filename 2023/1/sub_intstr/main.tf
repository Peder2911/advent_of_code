
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
   "one","1"),
   "two","2"),
   "three","3"),
   "four","4"),
   "five","5"),
   "six","6"),
   "seven","7"),
   "eight","8"),
   "nine","9")
}
