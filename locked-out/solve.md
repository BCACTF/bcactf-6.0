i am sure there are lots of ways to solve this

but the way i did it is by shifting the window to what you need by doing soemthing like

```python
a +=              "x"
```

the spaces shift the window
and we build up `a` into a payload

then we shift the window again so that we can use `exec`
in a cheeky one liner like

`b =                2;exec(a)`
