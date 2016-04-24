define JSON_BODY
{
  "consumer_key": "CONSUMER KEY",
  "consumer_secret": "CONSUMER SECRET",
  "access_token_key": "ACCESS TOKEN KEY",
  "access_token_secret": "ACCESS TOKEN SECRET"
}
endef


dependencies:
	STATIC_DEPS=true pip install -Ur requirements.txt -t .
	mkdir nltk_data
	python -m nltk.downloader -d nltk_data punkt


prepare: dependencies
	rm -f lambda_bundle.zip
	rm -f lambda_haiku.zip
	zip -r lambda_haiku *
	make clean

clean:
	rm -rf nltk_data      
	git clean -fd

export JSON_BODY
credentials_file:
	@echo "$$JSON_BODY" > twitter_credentials.json
