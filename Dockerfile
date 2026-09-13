# Memory Vault's own image: the fleet's pinned base, this agent's persona
# and skills, plus the agent-index usage reporter.
#
# Pinned by digest, exactly like the fleet's own runtime/stack.json and the
# sibling agents' Dockerfiles: a mutable tag would re-resolve on every pull
# and change a large unreviewed surface under a running agent that holds live
# credentials.
FROM public.ecr.aws/e1h7x4a2/plow-cloud-agents@sha256:bfd4980f361a551e62569f8c2eb717c1076d0b8be3a0499b869eaece151336a4

# Identity and skills. SOUL.md replaces the base's; first boot re-asserts
# root ownership, which is what the trailing chmod answers. Skills land at
# /opt/hermes/skills so the base runtime reconciles them into whichever home
# this image boots — a COPY under /var/lib/hermes/skills is shadowed by the
# agent-home volume after first create.
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
 && chmod 0644 /var/lib/hermes/SOUL.md /var/lib/hermes/config.yaml

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
