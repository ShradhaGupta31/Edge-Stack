#Script for generating Android VM
from artifactory import ArtifactoryPath
import os
#from configparser import ConfigParser

#-------------------------------------Fetch the user credentials for artifactory login------------------------------

uname = os.environ.get("BDUSR")
pwd = os.environ.get("BDPWD")

android_source_path = []
android_artifacts = []

android_source_path = ArtifactoryPath(os.environ.get("ANDROID_SOURCE_PATH"),auth=(uname,pwd))
android_vm = ArtifactoryPath(os.environ.get("ANDROID_VM"),auth=(uname,pwd))
android_os_path = ArtifactoryPath(os.environ.get("ANDROID_OS_PATH"),auth=(uname,pwd))


#--------------------------------------------Fetch the latest Image-------------------------------------------------
#----------------for android----------------

for p in android_source_path:
    work_week = str(p).split("/")[-1].strip()
    ww = work_week.split("_")
    #print(ww)
    a=str(ww[0])
    b=a[2:]
    if b.isdigit(): 
        android_artifacts.append(b)
#print(android_artifacts)
android_latest_release = "ww"+ str(max(android_artifacts))
android_latest_release_path = os.environ.get("ANDROID_SOURCE_PATH") + android_latest_release + os.environ.get("ANDROID_SOURCE_PATH_SUBFOLDER")+ android_latest_release +os.environ.get("Android_IMG_IMAGE")   #Path of latest img image
#print(android_latest_release_path)
#print(android_latest_release)

#--------------------------------------------Deploying Image-----------------------------------------------------------
#----------------for android----------------
android_os_images = []

for path in android_os_path:
    os_files = str(path).split("/")[-1].strip()
    android_os_images.append(os_files)
  
if not "caas_"+android_latest_release+".img.tar.gz" in android_os_images:    
    print("New Android Release found..")
    print("Creating VM")
    os.system("curl -u '{user}:{password}' -o caas.img.tar.gz {release_path}".format(user=uname,password=pwd,release_path=android_latest_release_path))
    os.system("curl -i -X PUT -u '{user}:{password}' -T caas.img.tar.gz {destination}/{release}".format(user=uname,password=pwd,destination=android_os_path,release="caas_"+android_latest_release+".img.tar.gz"))
    os.system("tar -xf {img_image}".format(img_image="caas.img.tar.gz"))
    os.system("qemu-img convert -f raw -O qcow2 {img_image} {qcow_image}".format(img_image="caas.img",qcow_image="android_"+android_latest_release+".qcow2"))
    os.system("bzip2 -zk {qcow_image}".format(qcow_image="android_"+android_latest_release+".qcow2"))
    os.system("curl -i -X PUT -u '{user}:{password}' -T {qcow_image} {destination}/{release}".format(user=uname,password=pwd,qcow_image="android_"+android_latest_release+".qcow2.bz2",destination=android_vm,release="android_"+android_latest_release+".qcow2.bz2"))   
else:
    print("No New Android Release found.. Aborting VM Generation")
