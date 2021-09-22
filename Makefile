.PHONY: docker-login-check
docker-login-check:
ifndef DOCKER_TOKEN
	$(error DOCKER_TOKEN is undefined)
endif

.PHONY: docker-push-check
docker-push-check:
ifndef APP_TAG
	$(error APP_TAG is undefined)
endif


.PHONY: docker-login
docker-login: docker-login-check
	docker login ghcr.io --username $(DOCKER_USERNAME) -p $(DOCKER_TOKEN) 2>/dev/null

.PHONY: docker-build
docker-build: docker-login
	docker build --file ./web-app/Dockerfile --tag ghcr.io/$(DOCKER_USERNAME)/$(DOCKER_REPO):$(APP_TAG) ./web-app


.PHONY: docker-retag-push
docker-retag-push: docker-push-check
	docker tag ghcr.io/$(DOCKER_USERNAME)/$(DOCKER_REPO):latest ghcr.io/$(DOCKER_USERNAME)/$(DOCKER_REPO):$(APP_TAG)
	docker push ghcr.io/$(DOCKER_USERNAME)/$(DOCKER_REPO):$(APP_TAG)
