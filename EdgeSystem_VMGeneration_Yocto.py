#Script for generating Yocto VM
from artifactory import ArtifactoryPath
import os
#from configparser import ConfigParser

#-------------------------------------Fetch the user credentials for artifactory login------------------------------

uname = os.environ.get("BDUSR")
pwd = os.environ.get("BDPWD")

android_source_path = []
android_artifacts = []
yocto_source_path = []
yocto_artifacts = []

yocto_source_path = ArtifactoryPath(os.environ.get("YOCTO_SOURCE_PATH"),auth=(uname,pwd))
yocto_vm_path = ArtifactoryPath(os.environ.get("YOCTO_VM_PATH"),auth=(uname,pwd))

#--------------------------------------------Fetch the latest Image-------------------------------------------------
#----------------for yocto----------------
for i in yocto_source_path:
    a = str(i).split("/")[-1].strip()
    yocto_artifacts.append(a)
print(yocto_artifacts)

yocto_latest_release_path = ArtifactoryPath(str(yocto_source_path)+"/" +max(yocto_artifacts),auth=(uname,pwd))
for p in yocto_latest_release_path:
    yocto_wic_image=p

print(yocto_wic_image)

#--------------------------------------------Deploying Image-----------------------------------------------------------    
#----------------for yocto----------------
yocto_images = []
for path in yocto_vm_path:
    yocto_images.append(str(path).split("/")[-1].strip())
    
if "yocto_"+max(yocto_artifacts)+".qcow2" not in yocto_images:
    print("New Yocto Release found..")
    print("Creating VM")
    os.system("curl -u '{user}:{password}' -o yocto.wic.bz2 {release_path}".format(release_path=yocto_wic_image))
    os.system("bzip2 -d yocto.wic.bz2")
    os.system("qemu-img convert -f raw -O qcow2 {wic_image} {qcow_image}".format(wic_image="yocto.wic",qcow_image="yocto_"+max(yocto_artifacts)+".qcow2"))
    os.system("bzip2 -zk {qcow_image}".format(qcow_image="yocto_"+max(yocto_artifacts)+".qcow2"))
    os.system("curl -i -X PUT -u '{user}:{password}' -T {qcow_image} {destination}/{release}".format(user=uname,password=pwd,qcow_image="yocto_"+max(yocto_artifacts)+".qcow2.bz2",destination=yocto_vm_path,release="yocto_"+max(yocto_artifacts)+".qcow2.bz2"))   
else:
    print("No New Yocto Release found.. Aborting VM Generation") 
