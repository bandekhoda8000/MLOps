# Custom images with dependencies installed on:
Solution is to build the images locally and push it to a registry. After that you can set the base_image in the pipeline codes and use it.
*HACK*: You also can connect to minikubes docker daemon and build the image there. After that k8s would have that image locally and no need to pull it.
Caveat: Pulling images from a remote repository may be a threat because the container should be able to communicate with the outside world. Check it out

# Run this http://192.168.100.11:8080/arka/arka_ai/-/blob/main/ml_classification.py?ref_type=heads in pipeline 
# Resource and namespace management 


