PYTHON = .venv/bin/python3

run:
	fastapi run

create-db:
	$(PYTHON) scripts/create_db.py

dev:
	PYDEVD_DISABLE_FILE_VALIDATION=1 debugpy --listen 0.0.0.0:4444 -m fastapi dev --host=0.0.0.0

debug:
	$(MAKE) create-db
	$(MAKE) dev

clean-docker:
	@dangling_images=$$(docker images -f "dangling=true" -q); \
    if [ -n "$$dangling_images" ]; then \
        docker rmi -f $$dangling_images; \
    else \
        echo "No dangling images to remove."; \
    fi

up:
	ENV=local docker compose up -d --build

start:
	ENV=local docker compose up --watch --build

down:
	docker compose down

build:
	ENV=local docker compose up -d --build


db.link:
	gel instance link kb-docker -H localhost -P 3460 -u usal -b main --tls-security insecure

db.restore:
	gel branch wipe -I kb-docker main
	gel restore -I kb-docker -b main "$(word 2, $(MAKECMDGOALS))"
