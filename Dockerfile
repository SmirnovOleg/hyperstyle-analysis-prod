FROM registry.jetbrains.team/p/paddle/docker/paddle-py-3-9:0.4.7

COPY . /hyperstyle-analysis-prod
WORKDIR /hyperstyle-analysis-prod

ENTRYPOINT ["java", "-jar", "/hyperstyle-analysis-prod.jar"]