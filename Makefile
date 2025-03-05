copy:
	cp ../v2ex-digest/posts_v2/*_translate_v2.json ./public/posts_json

build: copy
	npm run build
	rm -rf docs
	mv dist docs

git-commit: build
	git add .
	git commit -am "update data"
