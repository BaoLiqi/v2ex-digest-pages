copy:
	cp ../v2ex-digest/posts_v2/*_translate_v2.json ./posts_json
	cp -r posts_json/ public

build: copy
	npm run build
	rm -rf docs
	mv dist docs

git-commit: build
	git add .
	git commit -am "update data"
