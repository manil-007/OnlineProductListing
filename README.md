Mentioning the points as discussed:
1. For the data extraction, the user will input the data in two parts
   a. List of search products separated by semicolon
   b. Top 'n' products to be searched
2. After getting the user inputs, the api call will be made which will generate the data in the form of dict like
   {"searchedProductName": "Hair Oil", "GeneratedProductTitle": "To be generated", "GeneratedProductDescription": "To be generated", "keywords": "[list of    keywords]"}
3. At last the user will check and proceed with updating the listed product data or export the table data into excel sheel.

In the above second step, it will consist of mutiple steps:
1. The excel will be generated with the extracted product data.
2. The data will be grouped according to the searched product name.
3. The product title and description data will be combined to single data. 
4. The brand name will be extracted from the data and which will be removed from above combined data.
5. The noise and stop words will be removed from above data.
6. Using BERT algorithm, the keywords will be generated in the form of lists.
7. Now this list of keywords will be used to generate title and description using chatpGPT.

# Online Product Listing
OPL extracts information about the similar products and generates the best listing of the products.

## How to run
### Setup the virtual environment
`python3 -m venv venv` 
`pip install -r requierments.txt`

### Run as standalone executable
`python app.py -h` # run in headless mode

OR

`python app.py -u` # prints usage

### Run as centralised API
`python main.py -h` # Headless mode (preferred)

Use -v flag to run in verbose/debug mode
`python -v main.py -h`

OR

`python main.py` # Run with browser - use for debugging

### Run as centralised API in monitored mode
`pm2 start ecosystem.config.js`

#### Checks Status in monitored mode
`pm2 status`

#### Check Logs in monitored mode
`pm2 logs`

#### Monitoring centralised API in monitored mode
`pm2 monit`

#### Stopping centralised API in monitored mode
`pm2 stop "opl api"`

### Swagger UI
Swagger UI is available only in test / debug mode. Access URL - localhost:5000/api/v1/ui/ to test the API.

## Build and run containers
### Build the container
```bash 
docker build -t opl-api-img-04052023 . 
```

### Run the container
#### For development
```bash
docker run --rm -v $(pwd)/logs:/app/logs -v $(pwd)/config:/app/config -v $(pwd)/controllers:/apps/controllers:ro -v $(pwd)/utils:/apps/utils:ro -d -p 5000:5432 opl-api-img-04052023
```

#### For production
```bash
docker run --rm -v $(pwd)/logs:/app/logs -d p 5000:5432 opl-api-img-04052023
```

## References
- [Python REST APIs With Flask, Connexion, and SQLAlchemy](https://dassum.medium.com/python-rest-apis-with-flask-connexion-and-sqlalchemy-3c8c3292d9ce)
- [How to write README.md](https://medium.com/@saumya.ranjan/how-to-write-a-readme-md-file-markdown-file-20cb7cbcd6f)
- [Swagger YAML Editor](https://editor.swagger.io/)
- [Tokens checker](https://platform.openai.com/tokenizer)
- [OpenAI API Cookbook](https://github.com/openai/openai-cookbook)
- [Handling rate limits](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_handle_rate_limits.ipynb)
- [CORS Handling](https://auth0.com/blog/cors-tutorial-a-guide-to-cross-origin-resource-sharing/)
- [Git Branching and Merging](https://www.varonis.com/blog/git-branching#:~:text=To%20merge%20branches%20locally%2C%20use,branch%20into%20the%20main%20branch.)
- [Cannot do partial commit](https://stackoverflow.com/questions/5827944/git-error-on-commit-after-merge-fatal-cannot-do-a-partial-commit-during-a-mer)
- [How to replace master branch in Git, entirely, from another branch?](https://stackoverflow.com/questions/2862590/how-to-replace-master-branch-in-git-entirely-from-another-branch)
- [Nginx Beginner’s Guide](http://nginx.org/en/docs/beginners_guide.html)
- [Alpine, Slim, Stretch, Buster, Jessie, Bullseye — What are the Differences in Docker Images?](https://medium.com/swlh/alpine-slim-stretch-buster-jessie-bullseye-bookworm-what-are-the-differences-in-docker-62171ed4531d)
- [Stop using Alpine Docker images, instead use distroless images](https://medium.com/inside-sumup/stop-using-alpine-docker-images-fbf122c63010)
- [Smalled Docker images](https://learnk8s.io/blog/smaller-docker-images)
- [DORA Metrics](https://www.linkedin.com/pulse/my-experience-using-dora-other-metrics-fredrik-norm%C3%A9n)
- [Flow or DevOps Metrics](https://www.youtube.com/watch?v=84OvgV1CHOo)
- [Value Stream Managemet](https://www.leanix.net/en/wiki/vsm/value-stream-management)
- [DORA Metrics in detail](https://www.leanix.net/en/wiki/vsm/dora-metrics#:~:text=stream%20management%20efforts.-,What%20are%20DORA%20metrics%3F,change%20failure%20rate%20(CFR).)
- [Docker getting started](https://medium.com/free-code-camp/docker-tutorial-getting-started-with-python-redis-and-nginx-73ec94ca2f1)
- [Containerizing Python web apps with Docker, Flask, Nginx & uWSGI](https://www.youtube.com/watch?v=dVEjSmKFUVI)
- [Make your Python Docker images secure, fast & small](https://medium.com/vantageai/how-to-make-your-python-docker-images-secure-fast-small-b3a6870373a0)
https://github.com/joschan21?tab=repositories
https://github.com/hwchase17
https://levelup.gitconnected.com/16-system-design-concepts-i-wish-i-knew-before-the-interview-b8586e40a73b
https://automationpanda.com/2017/03/14/python-testing-101-pytest/
https://github.com/xtekky/gpt4free
https://github.com/JushBJJ/Mr.-Ranedeer-AI-Tutor
- [Developing inside containers](https://code.visualstudio.com/docs/devcontainers/containers)
