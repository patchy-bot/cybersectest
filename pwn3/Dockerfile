FROM ubuntu@sha256:aa772c98400ef833586d1d517d3e8de670f7e712bf581ce6053165081773259d AS app
RUN dpkg --add-architecture i386
RUN apt-get update && apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 && rm -rf /var/lib/apt/lists/*

FROM pwn.red/jail

COPY --from=app / /srv

COPY vuln /srv/app/run
COPY README.md /srv/app/README.md
