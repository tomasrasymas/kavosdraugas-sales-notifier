# Python project: coffee sales alert
### How I know that my favourite coffee is on sale! A tool that alerts me when sales are happening!

I am using this tool to track sales on [kavosdraugas.lt](https://www.kavosdraugas.lt/) e-commerce site. 

This tool runs only OSX (`launchctl` and `osascript` are used) only.

### How to run?
1. Fill `products.json` file putting URLs of products you want to track.
```json
[
    {
        "url": "https://www.kavosdraugas.lt/p/kavos-draugo-pupeles-caprissimo-fragrante-1kg/"
    },
    {
        "url": "https://www.kavosdraugas.lt/p/kavos-pupeles-cafe-liegeois-venezia-corsato-1kg/"
    }
]
```
2. Run `./install.sh`, provide path to Python interpreter
3. Wait for sales notifications!

More in my [blog post](https://medium.com/@tomas.rasymas/python-project-coffee-sales-alert-b9e76f386b05)
