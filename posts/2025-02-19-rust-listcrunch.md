---
title: Learning Rust by porting a small Python library
summary: How much can I learn from a one-file project? Lots.
---

I'm going down a rabbit hole on Rust. After converting my little [Fanatics scraper](https://chrisamico.com/blog/2025-02-09/fanatics-scraper-rust/), I wanted another small project that would let me solve all the novel problems that come up when learning a new language.

[ListCrunch](https://github.com/MuckRock/listcrunch) is a Python library for compressing lists into a short string representation. [Dylan Freedman](https://github.com/freedmand) wrote it as part of [DocumentCloud's](https://www.documentcloud.org) processing pipeline, and to the best of my knowledge, DocumentCloud is the only place it's used.

```python
from listcrunch import crunch, uncrunch

compressed_string = crunch([1, 1, 1, 1, 1, 1, 1, 1, 1, 2])
# Returns '1:0-8;2:9', meaning 1 appears in indices 0-8 (inclusive),
# and 2 occurs at index 9.

uncrunch('50:0-1,3-4;3:2,5;60:6;70:7-8')
# Returns ['50', '50', '3', '50', '50', '3', '60', '70', '70']
```

I wrote a [typescript utility](https://github.com/MuckRock/documentcloud-frontend/blob/main/src/lib/utils/pageSize.ts#L49-L78) to unpack a [page spec](https://www.documentcloud.org/help/api/#page-spec) into an array of sizes, so I'm familiar with the format.

Now there's a [Rust version](https://github.com/eyeseast/listcrunch).

```rust
use listcrunch::crunch;

fn main() {
    let pages = vec!["595.0x842.0", "595.0x842.0", "595.0x842.0", "595.0x842.0", "595.0x842.0", "595.0x842.0", "595.0x842.0"];
    let compressed_string = crunch(&pages);

    println!("page_spec = {compressed_string}");
    assert_eq!(compressed_string, "595.0x842.0:0-6");
}
```

## Staying in the standard library

The Python version of List Crunch works entirely within the standard library. In fact, it only has one import -- [`collections.defaultdict`](https://docs.python.org/3/library/collections.html#collections.defaultdict) -- and the whole module is one file.

Rust needs three imports -- `HashMap` and two traits -- but it also has everything it needs in the standard library.

The biggest difference is Rust's type system, which is both stricter and more nuanced than Python's. Nothing surprising here. It forced me to think about the difference between a `String` and a `&str`, and to be more explicit about the places I was allocating memory. The borrow checker never bit me.

## Keep your friends close and your tests closer

Something I really like about Rust: In a small project like this, I can have a tests module sitting right next to my code. I'm sure there's a point where this gets unweildy, but it's a nice default.

After some googling, I figured out that I could [include](https://github.com/eyeseast/listcrunch/blob/main/src/lib.rs#L1) the project's `README.md` as inline documentation with one line: `#![doc = include_str!("../README.md")]`. That also meant tests would run against any code blocks in the README file.

Python's testable docstrings are one of its best features, and having them in Rust made the language feel just that much more familiar. And having one command (`cargo test`) capture unit tests and doctests with no other configuration is wonderful.

## Batteries included

This already feels like a misty-eyed love letter to Rust, but I really enjoyed this little project.

Having one tool, Cargo, that handles building, testing, formatting and dependencies just saves so much headache.

I've done two small projects now, and I've barely left the standard library. There's a whole ecosystem I've hardly touched.
