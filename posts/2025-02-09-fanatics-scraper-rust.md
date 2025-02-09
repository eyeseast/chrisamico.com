---
title: Writing a little scraper in Rust
summary: Some things we have to learn the hard way.
---

A couple years ago, I wrote a [scraper](https://github.com/eyeseast/fanatics) to check prices on [BJJ Fanatics](https://bjjfanatics.com/), a site that uses [mattress-like pricing gimmicks](https://www.reddit.com/r/bjj/comments/15z437v/systematically_buying_bjj_fanatics_instructionals/) and where I spend significantly more time and money than I should. I wrote it in [Deno](https://deno.com/), because it was a new runtime and I wanted to learn how it handled the sorts of things I might do in [NodeJS](https://nodejs.org/en) or [Python](https://www.python.org/). It has been [running](https://github.com/eyeseast/fanatics/actions) without issue ever since.

[Deno 2](https://deno.com/blog/v2.0), however, had enough breaking changes that I was going to have to rewrite most of it to make any updates, so I decided it was a good time to try something new. And while I could just knock this out in a language I already know -- Python and Node are obvious choices here -- a small project like this is a good way to learn something new. I decided to rewrite it in Rust.

Scraping involves several different domains -- parsing HTML, CSS selectors, HTTP, sometimes asynchronous programming -- and even a single-file script deals with a handful of common programming tasks.

Things the original `scrape.ts` script does:

- read command-line arguments
- read the `urls.csv` file
- parse that file as CSV
- for each row, fetch a URL
- parse the resulting HTML and extract a price from a common selector
- write results to the `prices.csv` file, also in CSV format

When `prices.csv` changes, we run `update_readme.ts`:

- read the `prices.csv` file and parse as CSV
- build a string in Markdown format by looping through the CSV
- writing a new `README.md` file

That's a lot. A big part of learning a new language or framework is figuring out how to find things, and understanding typical ways to solve common problems. Nothing on that list is novel or complicated, but every language will handle it in a slightly different way.

Python can do all of that without leaving the [standard library](https://docs.python.org/3/library/). Node needs at least a CSV package -- [good luck choosing one](https://www.npmjs.com/search?q=csv). What does a Rust need?

Reading arguments from the command line is [in the standard library](https://doc.rust-lang.org/stable/std/env/fn.args.html), as is [reading a file](https://doc.rust-lang.org/stable/std/fs/struct.File.html#method.open).

The [csv crate](https://crates.io/crates/csv) handles reading and writing, and integrates with [serde](https://serde.rs/) to serialize and deserialize structs. So far, so good.

How do I make HTTP requests? The [Rust cookbook](https://rust-lang-nursery.github.io/rust-cookbook/web/clients/requests.html) suggests the [reqwest crate](https://docs.rs/reqwest/0.12.12/reqwest/index.html), so I went with that. I'm using blocking requests for now, though it was slower than I expected. I might look at using its asynchronous client.

I searched "scraping in Rust" and found a crate called [scraper](https://docs.rs/scraper/0.22.0/scraper/), so I used that to extract prices. There are [other ways](https://rust-lang-nursery.github.io/rust-cookbook/web/scraping.html), but this worked.

Finally, I wrote the resulting files ot `stdout`, because it's easy enough to just redirect into a file or print the results to the terminal for debugging. Simple string formatting is enough to write the `README` file with current prices.

The last piece is wrapping this all in a Github Action, which will run on a schedule and conditionally commit results. This turned out to be easier than I expected. Rust's toolchain is [included in Github's standard runners](https://users.rust-lang.org/t/github-actions-for-rust/116704/2), so there's no setup beyond calling `rustup update` and `cargo build --release`.

Was this harder than it needed to be? Absolutely. But sometimes that's the whole point. I'm tempted to make another version in [Go](https://go.dev/), just for fun.
