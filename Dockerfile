# Memory Vault's own image: the fleet's pinned base, this agent's persona
# and skills, plus the agent-index usage reporter.
#
# Pinned by digest, exactly like the fleet's own runtime/stack.json and the
# sibling agents' Dockerfiles: a mutable tag would re-resolve on every pull
# and change a large unreviewed surface under a running agent that holds live
# credentials.
FROM public.ecr.aws/e1h7x4a2/plow-cloud-agents:base-51f83158a70a383f03a4d03dbd8b6ea102cf0361@sha256:253d7ed3409effa7fa59113d93b4b79bb731d8264cdaf4cd60294924d0110a2e

# Boot recomposes $HOME/SOUL.md from this seed. COPY to the home is
# shadowed by the volume and then overwritten; the vault identity has
# to live here or the generic "Plow assistant" seed wins.
COPY runtime/SOUL.md /opt/hermes/plow-seed/SOUL.md

# plow-init seeds an absent home from plow-seed/config.yaml. Copying
# runtime/config.yaml only into /var/lib/hermes is not enough (agent-home
# shadows it): holographic memory, Latch, group sessions and the
# toolset-minus-web have to be stamped onto the seed.
COPY runtime/config.yaml /tmp/mv-runtime-config.yaml
COPY image/merge_mv_seed_config.py /opt/plow/merge_mv_seed_config.py
RUN /opt/hermes/.venv/bin/python3 /opt/plow/merge_mv_seed_config.py \
      /opt/hermes/plow-seed/config.yaml /tmp/mv-runtime-config.yaml \
 && grep -q 'provider: holographic' /opt/hermes/plow-seed/config.yaml \
 && grep -q 'latch:' /opt/hermes/plow-seed/config.yaml \
 && grep -q 'group_sessions_per_user: false' /opt/hermes/plow-seed/config.yaml

# Identity and skills. Home COPY is the first-boot volume fill; first boot
# re-asserts root ownership, which is what the trailing chmod answers.
# Skills land at /opt/hermes/skills so the base runtime reconciles them
# into whichever home this image boots — a COPY under /var/lib/hermes/skills
# is shadowed by the agent-home volume after first create.
COPY runtime/SOUL.md /var/lib/hermes/SOUL.md
COPY runtime/config.yaml /var/lib/hermes/config.yaml
COPY LICENSE /usr/share/doc/memory-vault/
COPY mv-ingest/ /opt/hermes/skills/mv-ingest/
COPY mv-recall/ /opt/hermes/skills/mv-recall/
COPY mv-act/    /opt/hermes/skills/mv-act/
COPY mv-learn/  /opt/hermes/skills/mv-learn/

RUN find /opt/hermes/skills -mindepth 1 -type d -exec chmod 0755 {} + \
 && find /opt/hermes/skills -mindepth 1 -type f ! -perm -u+x -exec chmod 0644 {} + \
 && find /opt/hermes/skills -mindepth 1 -type f -perm -u+x -exec chmod 0755 {} + \
 && chmod 0644 /var/lib/hermes/SOUL.md /var/lib/hermes/config.yaml \
      /opt/hermes/plow-seed/SOUL.md

# The usage reporter, fetched at build from the commit vendor/client.pin
# names and checked against the hash beside it. Fetched rather than
# committed because plow-pbc/agent-index-client owns that file; pinned
# rather than tracked from a branch because this runs inside an agent
# holding a live credential, and a moving reference would substitute
# unreviewed code under it. The checksum is the second half: a sha in a URL
# is only as good as the host serving it. Same pattern as
# life-assistant-hermes-agent and the-plow-times-hermes-agent.
#
# Root-owned under /opt/plow: everything under $HERMES_HOME belongs to the
# agent's uid in a running container, so scheduling code from there would run
# whatever a turn last wrote.
COPY vendor/client.pin /opt/plow/agent-index-client.pin
RUN set -eu; \
    sha="$(sed -n 's/^sha=//p' /opt/plow/agent-index-client.pin)"; \
    want="$(sed -n 's/^sha256=//p' /opt/plow/agent-index-client.pin)"; \
    path="$(sed -n 's/^path=//p' /opt/plow/agent-index-client.pin)"; \
    curl -fsS --max-time 60 -o /opt/plow/agent-index-client.py \
      "https://raw.githubusercontent.com/plow-pbc/agent-index-client/${sha}/${path}"; \
    got="$(sha256sum /opt/plow/agent-index-client.py | cut -d' ' -f1)"; \
    [ "$got" = "$want" ] || { echo "agent-index client is $got, pin says $want" >&2; exit 1; }; \
    chmod 0644 /opt/plow/agent-index-client.py

COPY image/s6-overlay/ /etc/s6-overlay/
COPY image/cont-init.d/02-copy-plow-credentials /etc/cont-init.d/02-copy-plow-credentials
RUN chmod 0755 /etc/cont-init.d/02-copy-plow-credentials

# Hermes' billing wall concatenates the HTTP body, the provider name, a
# billing URL and `/model`. Pin one user-facing line and fail the build if
# the base digest moved those functions.
COPY image/hermes/billing_user_message.py /opt/hermes/agent/billing_user_message.py
COPY image/hermes/patch_billing_user_message.py /opt/plow/patch_billing_user_message.py
RUN /opt/hermes/.venv/bin/python3 /opt/plow/patch_billing_user_message.py \
      /opt/hermes/agent/conversation_loop.py \
 && chmod 0644 /opt/hermes/agent/billing_user_message.py
