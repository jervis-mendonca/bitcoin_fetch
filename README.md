# bitcoin_fetch

In this repo, I have added scripts pertaining to fetching the value of btc in eur and czk. I add a few comments below about kuberentes:

1) I create a helm chart directory 'bitcoin-microservice'
2) I create a 'values.yaml' file
3) I create a dockerfile
4) build a docker image : 'docker build -t bitcoin-microservice .'
5) In the templates folder of my helm chart directory, I create a deployment.yaml file
6) finally, I deploy my helm chart to my kubernetes cluster
