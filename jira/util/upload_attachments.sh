#!/bin/bash


###################    Variables section         ###################
# Jira version variables
JIRA_VERSION_FILE="/media/atl/jira/shared/jira-software.version"
SUPPORTED_JIRA_VERSIONS=(8.0.3 7.13.6)
JIRA_VERSION=$(sudo su jira -c "cat ${JIRA_VERSION_FILE}")
echo "Jira Version: ${JIRA_VERSION}"

DATASETS_AWS_BUCKET="https://centaurus-datasets.s3.amazonaws.com/jira"
ATTACHMENTS_TAR="attachments.tar.gz"
ATTACHMENTS_DIR="attachments"
DATASETS_SIZE="large"
ATTACHMENTS_TAR_URL="${DATASETS_AWS_BUCKET}/${JIRA_VERSION}/${DATASETS_SIZE}/${ATTACHMENTS_TAR}"
TMP_DIR="/tmp"
EFS_DIR="/media/atl/jira/shared/data"
###################    End of variables section  ###################

# Check if Jira version is supported
if [[ ! "${SUPPORTED_JIRA_VERSIONS[@]}" =~ "${JIRA_VERSION}" ]]; then
  echo "Jira Version: ${JIRA_VERSION} is not officially supported by DCAPT."
  echo "Supported Jira Versions: ${SUPPORTED_JIRA_VERSIONS[@]}"
  echo "If you want to force apply an existing datasets to your Jira, use --force flag with version of dataset you want to apply:"
  echo "e.g. ./upload_attachments --force 8.0.3"
  echo "!!! Warning !!! This may broke your Jira instance."
  # Check if --force flag is passed into command
  if [[ "$1" == "--force" ]]; then
    # Check if passed Jira version is in list of supported
    if [[ "${SUPPORTED_JIRA_VERSIONS[@]}" =~ "$2" ]]; then
      ATTACHMENTS_TAR_URL="${DATASETS_AWS_BUCKET}/$2/${DATASETS_SIZE}/${ATTACHMENTS_TAR}"
      echo "Force mode. Dataset URL: ${ATTACHMENTS_TAR_URL}"
    else
      echo "Correct dataset version was not specified after --force flag."
      echo "Available datasets: ${SUPPORTED_JIRA_VERSIONS[@]}"
      exit 1
    fi
  else
    # No force flag
    exit 1
  fi
fi

echo "!!! Warning !!!"
echo    # move to a new line
echo "This script restores attachments into Jira DC created with AWS Quickstart defaults."
echo "You can review or modify default variables in 'Variables section' of this script."
echo    # move to a new line
echo "Variables:"
echo "EFS_DIR=${EFS_DIR}"
echo "ATTACHMENTS_TAR_URL=${ATTACHMENTS_TAR_URL}"
echo    # move to a new line
read -p "I confirm that variables are correct and want to proceed (y/n)?  " -n 1 -r
echo    # move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Script was canceled."
    exit 1
fi


echo "Step1: Download msrcync"
# https://github.com/jbd/msrsync
cd ${TMP_DIR}
if [[ -s msrsync ]]; then
  echo "msrsync already downloaded"
else
  sudo su jira -c "wget https://raw.githubusercontent.com/jbd/msrsync/master/msrsync && chmod +x msrsync"
fi

echo "Step2: Download attachments"
sudo su -c "rm -rf ${ATTACHMENTS_TAR}"
sudo su jira -c "wget ${ATTACHMENTS_TAR_URL}"

echo "Step3: Untar attachments to tmp folder"
sudo su -c "rm -rf ${ATTACHMENTS_DIR}"
sudo su jira -c "tar -xzvf ${ATTACHMENTS_TAR}"
if [[ $? -ne 0 ]]; then
  echo "Untar failed!"
  exit 1
fi
echo "Counting total files number:"
sudo su jira -c "find ${ATTACHMENTS_DIR} -type f -print | wc -l"
echo "Deleting ${ATTACHMENTS_TAR}"
sudo su -c "rm -rf ${ATTACHMENTS_TAR}"

echo "Step4: Copy attachments to EFS"
sudo su jira -c "time ./msrsync -P -p 100 -f 3000 ${ATTACHMENTS_DIR} ${EFS_DIR}"
sudo su -c "rm -rf ${ATTACHMENTS_DIR}"