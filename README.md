The inverse of JQ: give it some data, and it will give you
a JQ address to find that data:

```
$ qj "This is delicious" cakes.json
.cakes.sweet["Extreme Chocolate"].variations[3] = "This is delicious"
```

```
$ jq cakes.json '.cakes.sweet["Extreme Chocolate"].variations[3]'
"This is delicious"
```
