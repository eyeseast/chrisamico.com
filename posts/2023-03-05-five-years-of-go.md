---
title: Five years of Go
summary: After half a decade of regularly working in Go, there's a lot I've come to like about it, and a few things I still struggle with.
---

I'd never written a line of Go when I started at Gannett in 2018. I'd barely even looked at the language, and when I did it looked both verbose and intimidating. But my team's primary codebase was written in Go, and it was (at the time) the recommended approach to building web services in the company. After half a decade of regularly working in Go, there's a lot I've come to like about it, and a few things I still struggle with.

Before learning Go, I'd worked in Python, JavaScript and PHP, so much of my experience with Go is shaped by how it's different from those languages.

Despite my initial hesitation, Go was relatively easy to learn. It's a small language with great documentation. I went through [A tour of Go](https://go.dev/tour/) in a day (partially on my phone), and [Effective Go](https://go.dev/doc/effective_go.html) gave me a broad conceptual understanding of the language.

## Types are OK, actually

I'd never used a strongly typed, compiled language before Go. The first langauge I learned was Python, and I was used to writing functions that might handle any kind of data I passed in, and might return a different type depending on the situation. I'm not saying that's a good idea, but Python allows it.

```python
# totally valid, not very good python
def take_anything(*args, **kwargs):
    # a list
    if kwargs.get('format') == 'list':
        return list(args)

    # a string
    if kwargs.get('format') == 'string':
        return ''.join(args)

    # a tuple
    return args
```

Go won't compile anything like that, at least not without writing code that makes it very clear we're dealing with a container of unknown length, holding an unknown type. And if we want to use that type, we're going to have to deal with those unknowns.

Over time, I've come to appreciate that checking types at build time removes a whole class of bugs I'd otherwise find much later, when a user somehow passed in something I hadn't anticipated. Now I add type hints to Python and JavaScript out of habit.

## Keep your tools together

One of Go's selling points is that it compiles quickly. We had a large, multipackage codebase with lots of dependencies, and yet it compiled in a second or two. Go's compiler is fast enough that it's normal to use `go run main.go` in development -- letting Go build a binary and then run it -- rather than compiling first and running separately.

Alongside the compiler, Go includes a code formatter (`go fmt`), test suite (`go test`) and package manager (`go mod`) in its default toolset. I wrote a very long post about how I install Python. My version of that for Go is one line:

```sh
brew install go
```

I've come to love tools like Black and Prettier because it removes the mental overhead of formatting -- and deciding _how_ to format -- my code. I write fast and the formatting cleans it up. But Black and Prettier are third-party tools that need to be installed, and a team has to agree to use them. Go has `go fmt` by default.

## Easier, if not easy, async

Python was (arguably) late to async. Node.js had it from the beginning, but promises significantly improved the experience. Go has channels and [goroutines](https://go.dev/tour/concurrency/1) built into the language in a way I immediately liked. I didn't use it often, but when I needed to parallelize a process, it was easier to reason about than a lot of other tools I've used. [Sharing by communicating](https://go.dev/doc/effective_go#concurrency) is a pattern I understand.

## Go is better now than five years ago

Using `go mod` is great, but it's also relatively new. When I started writing Go, we used `dep` and other tools to manage dependencies. Every package lived on a system-level `$GOPATH`, alongside our code. Modules and tools to manage different versions of dependencies didn't arrive until Go 1.11.

[Generics](https://go.dev/doc/tutorial/generics) are another big addition to Go, and it's a new enough part of the language that I've never actually used it. I probably could've refactored a lot of my codebase to use generics, but I never made the time. When I was first learning Go, I kept looking for something like Python's `itertools` in the standard library. I _think_ generics will fill that hole.

Another small feature I love: [`embed`](https://pkg.go.dev/embed@go1.20.1). Let's say I need a large SQL query that I'd rather write in its own file. I often write code like this in Python:

```python
import pathlib

SQL = (pathlib.Path('.') / 'query.sql').read_text()
```

Or in Node.js:

```js
import "fs" from "node:fs"
import "path" from "node:path"

const SQL = fs.readFileSync(path.resolve('./query.sql'))
```

In both cases, I'm reading a file, synchronously, at runtime. Yes, it's only doing that once, but it's still a thing the code has to do at runtime. Go can use the `embed` package to do it at build time.

```go
import _ "embed"

//go:embed query.sql
var sql string

print(sql)
```

## It's a weird syntax

Even after five years with Go, I still find myself looking up basic things, like how to read files or use parts of the standard library. There are great resources, like [Go by Example](https://gobyexample.com/), but it's still not an intuitive language.

Little things like capitalizing variables to export, or using curly braces where other languages use parentheses, or returning errors still force me to stop and remember how the language works. It's just different enough from every other language I work in that I have to think about it every time.

All that said, I like it and expect to keep using, even if it's not part of my regular job.
