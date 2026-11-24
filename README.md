[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/indonlol123/news-image-20261124-makefun/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/indonlol123/news-image-20261124-makefun/reward.svg)](https://make.fun/bounty/news-image-20261124)

# The World in a Day — 24 November 2026

One-page newspaper front page summing up the world's news of Tuesday
24 November 2026, for the [make.fun bounty](https://make.fun/bounty/news-image-20261124)
"Sum up 24 November's world news in one image".

Lead story: Nvidia reinstates Jensen Huang as chief executive, 11 days
after he resigned in an espionage scandal — shares jump 31% and lift
Wall Street to its best day since April 2024. Also on the page: the US
blacklisting Singapore chip firm Megaspeed, Iran's strikes on Gulf sites,
Russian jets entering South Korea's air defence zone, Ukraine sinking a
Russian warship off Libya, the Kyiv drone strike, the states suing SpaceX
over Grok, Mexico capturing "El Chapo Isidro", COP31 ending with no deal,
Spain's election polls, Bangladesh's 50-million-child vaccination drive,
and Alcaraz winning the ATP Finals.

## Run

```sh
python3 render.py          # rebuild entry.png (1024x1024, deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copy it to out/entry.png
```

`main.ts` (Node 22, stdlib only) copies the pre-rendered `entry.png` into
`$MAKEFUN_OUTPUT_DIR/entry.png`. No network, no randomness: every run writes
the same bytes (sha256 `7059a97218efec8415f8272c44dc00cd48bc6f3376fb88a9e1d859a27806d3f3`).

## Files

- `main.ts` — entry point
- `render.py` — draws `entry.png` with Pillow (Noto fonts)
- `entry.png` — the front page, 1024x1024 PNG
