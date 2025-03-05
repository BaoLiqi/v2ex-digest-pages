copy:
	cp ../v2ex-digest/posts_v2/*_translate_v2.json ./posts_json
	python3 merge_json.py

build: copy
	npm run build
	rm -rf docs
	mv dist docs

git-commit:
	git add .
	git commit -am "update data"
