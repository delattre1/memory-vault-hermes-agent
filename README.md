# Memory Vault

The restaurant. The recipe. The movie you swore you'd watch. You saved
the reel and lost all three. Share the link like a text to a friend —
it opens the post, keeps them, and when Saturday comes, you just ask.

A vault for the posts you'd lose: places, recipes, films, products,
gifts, nights out. You don't file anything. You send the link. It
reads the post and remembers. Later you ask across everything you
saved — not the feed, not Saves.

## Install

One repo, Docker Compose, and a Plow line. You need Git, Docker Compose, and Python 3.

```sh
git clone https://github.com/plow-pbc/plow-agents.git
export PATH="$PWD/plow-agents/bin:$PATH"

git clone https://github.com/jeanjacintho/memory-vault-hermes-agent.git
cd memory-vault-hermes-agent

plow-agents login                 # text the printed “Plow Activate: …” code
plow-agents lines                 # pick a line whose STATUS is free
plow-agents mint ln_xxx           # writes ./plow-credentials — do this before the first up
docker compose up --build -d
docker compose logs -f agent      # wait for: plow-init: configured ... as cht_
```

If you have no assistant line yet: `plow-agents login --new-line`, then `lines` and `mint`.

Text the line you minted. Share a post the way you'd send it to a friend.

To open the post in your own browser, run [Latch](https://howto.plow.co/latch) on the Mac this agent should drive. In Latch: **Agents → can’t use OAuth? create a static credential**. Put `DOMO_DEVICE_UID` and `DOMO_MCP_TOKEN` in the **volume** dotenv at `/var/lib/hermes/.env` inside the container (`KEY=value` at column 0) — not the repo `.env`, which compose does not mount — then `docker compose restart`. Chat works without Latch; fetching the live page does not.

```sh
docker compose down          # stop, keep memory
docker compose down -v       # DELETES sessions and memory_store.db — only a new setup
plow-agents revoke           # retire the line in plow-credentials
```

`plow-credentials` is gitignored. Do not commit it.

## License

MIT. See [LICENSE](LICENSE).
