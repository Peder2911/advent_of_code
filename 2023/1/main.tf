// HCL is a programming language. Just not my favorite one.

locals {
   input = split("\n",trimspace(file("./data")))
}

module "sub_intstr" {
   source = "./sub_intstr"
   for_each = {for i,v in local.input: i=>v}
   input = each.value
}

module "calibration_value" {
   source = "./calibration_value"
   for_each = {for i,v in local.input: i=>v}
   input = each.value
}

module "calibration_value_sub_intstr" {
   source = "./calibration_value"
   for_each = {for i,v in local.input: i=>v}
   input = module.sub_intstr[each.key].result
}

output "one" {
   value = sum([for v in values(module.calibration_value): parseint(v.result,10)] )
}

output "two" {
   value = sum([for v in values(module.calibration_value_sub_intstr): parseint(v.result,10)] )
}
